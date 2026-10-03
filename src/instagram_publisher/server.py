"""MCP server exposing the Instagram post queue as tools."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

from .config import Config
from .instagram import InstagramClient, InstagramError
from .queue import PostQueue, QueueError

mcp = FastMCP("instagram-publisher")

_config: Config | None = None
_client: InstagramClient | None = None


def config() -> Config:
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config


def queue() -> PostQueue:
    return PostQueue(config().posts_dir, config().public_media_base_url)


def client() -> InstagramClient:
    global _client
    if _client is None:
        cfg = config()
        _client = InstagramClient(cfg.access_token, cfg.user_id, cfg.api_version)
    return _client


def _publish_queued(name: str) -> dict:
    q = queue()
    post = q.load(name)
    urls = q.media_urls(post)
    result = client().publish(urls, post.caption)
    record = {
        "media_id": result.media_id,
        "permalink": result.permalink,
        "published_at": datetime.now(timezone.utc).isoformat(),
        "caption": post.caption,
        "media_urls": urls,
    }
    dest = q.mark_published(post, record)
    return {**record, "moved_to": str(dest)}


@mcp.tool()
def list_pending_posts() -> list[dict]:
    """List the posts waiting in the queue (posts/pending), with caption, media,
    schedule and any problems that would stop them from publishing."""
    return [p.summary() for p in queue().list_pending()]


@mcp.tool()
def preview_post(name: str) -> dict:
    """Show exactly what would be sent to Instagram for one pending post,
    including the public media URLs, without publishing anything."""
    q = queue()
    post = q.load(name)
    info = post.summary()
    try:
        info["media_urls"] = q.media_urls(post)
    except QueueError as exc:
        info["warnings"].append(str(exc))
    return info


@mcp.tool()
def publish_post(name: str) -> dict:
    """Publish a pending post from the queue to Instagram, then move it to
    posts/published. Always confirm with the user before calling this."""
    try:
        return _publish_queued(name)
    except (QueueError, InstagramError) as exc:
        return {"error": str(exc)}


@mcp.tool()
def publish_due_posts() -> list[dict]:
    """Publish every pending post whose publish_at time has passed."""
    results = []
    for post in queue().list_pending():
        if post.is_due():
            try:
                results.append({"name": post.name, **_publish_queued(post.name)})
            except (QueueError, InstagramError) as exc:
                results.append({"name": post.name, "error": str(exc)})
    return results


@mcp.tool()
def publish_now(media_urls: list[str], caption: str = "") -> dict:
    """Publish directly without the queue. media_urls are public https:// URLs:
    one JPEG image (photo post), one MP4/MOV video (reel), or 2-10 items (carousel).
    Always confirm with the user before calling this."""
    try:
        result = client().publish(media_urls, caption)
        return {"media_id": result.media_id, "permalink": result.permalink}
    except InstagramError as exc:
        return {"error": str(exc)}


@mcp.tool()
def account_status() -> dict:
    """Check the access token and show the connected account and how many
    posts are left in Instagram's 24-hour publishing limit."""
    try:
        c = client()
        return {**c.get_account(), "publishing_limit": c.get_publishing_limit()}
    except InstagramError as exc:
        return {"error": str(exc)}


@mcp.tool()
def refresh_access_token() -> dict:
    """Extend the long-lived access token by 60 days. Returns the new token,
    which must be saved to INSTAGRAM_ACCESS_TOKEN."""
    try:
        body = client().refresh_token()
        return {"access_token": body.get("access_token"), "expires_in_seconds": body.get("expires_in")}
    except InstagramError as exc:
        return {"error": str(exc)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--publish-due",
        action="store_true",
        help="publish scheduled posts that are due and exit (for cron) instead of running the MCP server",
    )
    args = parser.parse_args()
    if args.publish_due:
        print(json.dumps(publish_due_posts(), indent=2))
    else:
        mcp.run()


if __name__ == "__main__":
    main()
