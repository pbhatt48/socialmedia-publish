"""Thin client for the Instagram API with Instagram Login (graph.instagram.com)."""
from __future__ import annotations

import time
from dataclasses import dataclass

import httpx

VIDEO_EXTENSIONS = (".mp4", ".mov")
MAX_CAROUSEL_ITEMS = 10
MAX_CAPTION_LENGTH = 2200


class InstagramError(RuntimeError):
    pass


def is_video(url: str) -> bool:
    return url.split("?", 1)[0].lower().endswith(VIDEO_EXTENSIONS)


@dataclass
class PublishResult:
    media_id: str
    permalink: str | None


class InstagramClient:
    def __init__(
        self,
        access_token: str,
        user_id: str | None = None,
        api_version: str = "v23.0",
        http: httpx.Client | None = None,
        poll_interval: float = 5.0,
        poll_timeout: float = 300.0,
    ):
        if not access_token:
            raise InstagramError("INSTAGRAM_ACCESS_TOKEN is not set")
        self.access_token = access_token
        self._user_id = user_id
        self.base_url = f"https://graph.instagram.com/{api_version}"
        self.http = http or httpx.Client(timeout=60)
        self.poll_interval = poll_interval
        self.poll_timeout = poll_timeout

    # -- low level -----------------------------------------------------------

    def _request(self, method: str, path: str, params: dict | None = None) -> dict:
        params = {**(params or {}), "access_token": self.access_token}
        url = path if path.startswith("https://") else f"{self.base_url}/{path.lstrip('/')}"
        if method == "GET":
            resp = self.http.get(url, params=params)
        else:
            resp = self.http.post(url, data=params)
        try:
            body = resp.json()
        except ValueError:
            body = {}
        if resp.status_code >= 400 or "error" in body:
            err = body.get("error", {})
            msg = err.get("error_user_msg") or err.get("message") or resp.text
            raise InstagramError(f"Instagram API error ({resp.status_code}): {msg}")
        return body

    # -- account -------------------------------------------------------------

    @property
    def user_id(self) -> str:
        if not self._user_id:
            self._user_id = str(self.get_account()["user_id"])
        return self._user_id

    def get_account(self) -> dict:
        return self._request("GET", "me", {"fields": "user_id,username,account_type,media_count"})

    def get_publishing_limit(self) -> dict:
        body = self._request(
            "GET", f"{self.user_id}/content_publishing_limit", {"fields": "quota_usage,config"}
        )
        data = (body.get("data") or [{}])[0]
        return {
            "posts_used_last_24h": data.get("quota_usage"),
            "max_posts_per_24h": (data.get("config") or {}).get("quota_total"),
        }

    def refresh_token(self) -> dict:
        """Extend a long-lived token by another 60 days (token must be >24h old)."""
        return self._request(
            "GET",
            "https://graph.instagram.com/refresh_access_token",
            {"grant_type": "ig_refresh_token"},
        )

    # -- publishing ----------------------------------------------------------

    def _create_container(self, params: dict) -> str:
        return self._request("POST", f"{self.user_id}/media", params)["id"]

    def _wait_until_ready(self, container_id: str) -> None:
        deadline = time.monotonic() + self.poll_timeout
        while True:
            status = self._request("GET", container_id, {"fields": "status_code,status"})
            code = status.get("status_code")
            if code in ("FINISHED", "PUBLISHED"):
                return
            if code in ("ERROR", "EXPIRED"):
                raise InstagramError(
                    f"Media container {container_id} failed: {status.get('status') or code}"
                )
            if time.monotonic() > deadline:
                raise InstagramError(f"Timed out waiting for media container {container_id}")
            time.sleep(self.poll_interval)

    def _item_container(self, url: str, *, carousel_item: bool, caption: str | None) -> str:
        params: dict = {}
        if is_video(url):
            params.update(media_type="REELS" if not carousel_item else "VIDEO", video_url=url)
        else:
            params["image_url"] = url
        if carousel_item:
            params["is_carousel_item"] = "true"
        elif caption:
            params["caption"] = caption
        return self._create_container(params)

    def publish(self, media_urls: list[str], caption: str = "") -> PublishResult:
        """Publish one image/video (single post or reel) or 2-10 items as a carousel."""
        if not media_urls:
            raise InstagramError("A post needs at least one image or video")
        if len(media_urls) > MAX_CAROUSEL_ITEMS:
            raise InstagramError(f"A carousel can hold at most {MAX_CAROUSEL_ITEMS} items")
        if len(caption) > MAX_CAPTION_LENGTH:
            raise InstagramError(f"Caption is longer than {MAX_CAPTION_LENGTH} characters")
        for url in media_urls:
            if not url.startswith("https://"):
                raise InstagramError(f"Media must be a public https:// URL, got: {url}")

        if len(media_urls) == 1:
            container_id = self._item_container(media_urls[0], carousel_item=False, caption=caption)
        else:
            children = [self._item_container(u, carousel_item=True, caption=None) for u in media_urls]
            for child in children:
                self._wait_until_ready(child)
            params = {"media_type": "CAROUSEL", "children": ",".join(children)}
            if caption:
                params["caption"] = caption
            container_id = self._create_container(params)

        self._wait_until_ready(container_id)
        media_id = self._request(
            "POST", f"{self.user_id}/media_publish", {"creation_id": container_id}
        )["id"]

        permalink = None
        try:
            permalink = self._request("GET", media_id, {"fields": "permalink"}).get("permalink")
        except InstagramError:
            pass
        return PublishResult(media_id=media_id, permalink=permalink)
