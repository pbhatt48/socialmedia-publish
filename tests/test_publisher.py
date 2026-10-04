import json
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs

import httpx
import pytest

from instagram_publisher.instagram import InstagramClient, InstagramError
from instagram_publisher.queue import PostQueue, QueueError


class FakeInstagram:
    """Records requests and answers like graph.instagram.com."""

    def __init__(self):
        self.calls = []
        self.next_id = 100

    def __call__(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path.split("/", 2)[-1]
        params = dict(request.url.params)
        if request.method == "POST":
            params.update({k: v[0] for k, v in parse_qs(request.content.decode()).items()})
        self.calls.append((request.method, path, params))
        if path == "me":
            return httpx.Response(200, json={"user_id": "42", "username": "me"})
        if path.endswith("/media") or path.endswith("/media_publish"):
            self.next_id += 1
            return httpx.Response(200, json={"id": str(self.next_id)})
        if params.get("fields") == "status_code,status":
            return httpx.Response(200, json={"status_code": "FINISHED"})
        if params.get("fields") == "permalink":
            return httpx.Response(200, json={"permalink": "https://www.instagram.com/p/abc/"})
        return httpx.Response(400, json={"error": {"message": "unexpected"}})

    def posts(self, suffix):
        return [p for m, path, p in self.calls if m == "POST" and path.endswith(suffix)]


@pytest.fixture
def fake():
    return FakeInstagram()


@pytest.fixture
def ig(fake):
    return InstagramClient(
        "token", http=httpx.Client(transport=httpx.MockTransport(fake)), poll_interval=0
    )


def test_single_image_post(ig, fake):
    result = ig.publish(["https://example.com/a.jpg"], "hello")
    assert result.media_id == "102"
    assert result.permalink == "https://www.instagram.com/p/abc/"
    (container,) = fake.posts("/media")
    assert container["image_url"] == "https://example.com/a.jpg"
    assert container["caption"] == "hello"
    assert fake.posts("/media_publish") == [{"creation_id": "101", "access_token": "token"}]
    assert all(path.startswith("42/") for m, path, _ in fake.calls if m == "POST")


def test_video_becomes_reel(ig, fake):
    ig.publish(["https://example.com/clip.mp4"], "")
    (container,) = fake.posts("/media")
    assert container["media_type"] == "REELS"
    assert container["video_url"] == "https://example.com/clip.mp4"


def test_carousel(ig, fake):
    ig.publish(["https://example.com/a.jpg", "https://example.com/b.mp4"], "two")
    a, b, parent = fake.posts("/media")
    assert a["is_carousel_item"] == "true" and "caption" not in a
    assert b["media_type"] == "VIDEO"
    assert parent["media_type"] == "CAROUSEL"
    assert parent["children"] == "101,102"
    assert parent["caption"] == "two"


def test_rejects_non_https(ig):
    with pytest.raises(InstagramError, match="public https"):
        ig.publish(["/tmp/a.jpg"])


def test_api_error_message():
    transport = httpx.MockTransport(
        lambda r: httpx.Response(400, json={"error": {"message": "Invalid OAuth access token"}})
    )
    client = InstagramClient("bad", user_id="1", http=httpx.Client(transport=transport))
    with pytest.raises(InstagramError, match="Invalid OAuth"):
        client.get_account()


def make_post(root, name, files=(), **meta):
    folder = root / "pending" / name
    folder.mkdir(parents=True)
    for f in files:
        (folder / f).write_bytes(b"x")
    if meta:
        (folder / "post.json").write_text(json.dumps(meta))
    return folder


def test_queue_discovers_local_media_and_caption(tmp_path):
    folder = make_post(tmp_path, "trip", files=["2.jpg", "1.jpg", "notes.md"])
    (folder / "caption.txt").write_text("Beach day\n")
    q = PostQueue(tmp_path, "https://cdn.example.com/posts")
    post = q.load("trip")
    assert post.caption == "Beach day"
    assert post.media == ["1.jpg", "2.jpg"]
    assert q.media_urls(post) == [
        "https://cdn.example.com/posts/pending/trip/1.jpg",
        "https://cdn.example.com/posts/pending/trip/2.jpg",
    ]


def test_local_media_without_public_url_is_an_error(tmp_path):
    make_post(tmp_path, "p", files=["a.jpg"])
    q = PostQueue(tmp_path)
    with pytest.raises(QueueError, match="PUBLIC_MEDIA_BASE_URL"):
        q.media_urls(q.load("p"))


def test_rejects_path_traversal(tmp_path):
    make_post(tmp_path, "p", files=["a.jpg"])
    with pytest.raises(QueueError):
        PostQueue(tmp_path).load("../pending")


def test_schedule_and_mark_published(tmp_path):
    past = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()
    future = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    make_post(tmp_path, "due", caption="c", media="https://x.com/a.jpg", publish_at=past)
    make_post(tmp_path, "later", caption="c", media="https://x.com/a.jpg", publish_at=future)
    make_post(tmp_path, "unscheduled", caption="c", media="https://x.com/a.jpg")
    q = PostQueue(tmp_path)
    assert [p.name for p in q.list_pending() if p.is_due()] == ["due"]

    dest = q.mark_published(q.load("due"), {"media_id": "1"})
    assert not (tmp_path / "pending" / "due").exists()
    assert json.loads((dest / "result.json").read_text()) == {"media_id": "1"}


def test_server_tools_register():
    import asyncio

    from instagram_publisher.server import mcp

    names = {t.name for t in asyncio.run(mcp.list_tools())}
    assert {"list_pending_posts", "preview_post", "publish_post", "publish_due_posts",
            "publish_now", "account_status", "refresh_access_token"} <= names
