"""File-based post queue.

    posts/
      pending/
        my-first-post/
          post.json      # optional: {"caption": "...", "media": [...], "publish_at": "..."}
          caption.txt    # optional: caption, used when post.json has none
          1.jpg 2.jpg    # media files, used (sorted by name) when post.json lists none
      published/
        2026-10-03_my-first-post/
          ...            # same files, plus result.json with the Instagram media id
"""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

MEDIA_EXTENSIONS = (".jpg", ".jpeg", ".mp4", ".mov")


class QueueError(ValueError):
    pass


@dataclass
class Post:
    name: str
    folder: Path
    caption: str
    media: list[str]  # https URLs or paths relative to the post folder
    publish_at: datetime | None = None
    warnings: list[str] = field(default_factory=list)

    def is_due(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return self.publish_at is not None and self.publish_at <= now

    def summary(self) -> dict:
        return {
            "name": self.name,
            "caption": self.caption,
            "media": self.media,
            "publish_at": self.publish_at.isoformat() if self.publish_at else None,
            "warnings": self.warnings,
        }


def _parse_time(value: str) -> datetime:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise QueueError(f"publish_at is not an ISO 8601 date/time: {value!r}") from exc
    if dt.tzinfo is None:
        dt = dt.astimezone()  # treat naive times as local time
    return dt


class PostQueue:
    def __init__(self, posts_dir: Path, public_media_base_url: str | None = None):
        self.posts_dir = posts_dir
        self.pending_dir = posts_dir / "pending"
        self.published_dir = posts_dir / "published"
        self.public_media_base_url = public_media_base_url

    def _folder(self, name: str) -> Path:
        folder = (self.pending_dir / name).resolve()
        if folder.parent != self.pending_dir.resolve() or not folder.is_dir():
            raise QueueError(f"No pending post named {name!r}")
        return folder

    def load(self, name: str) -> Post:
        folder = self._folder(name)
        meta: dict = {}
        if (folder / "post.json").is_file():
            try:
                meta = json.loads((folder / "post.json").read_text())
            except json.JSONDecodeError as exc:
                raise QueueError(f"{name}/post.json is not valid JSON: {exc}") from exc

        caption = meta.get("caption")
        if caption is None and (folder / "caption.txt").is_file():
            caption = (folder / "caption.txt").read_text().strip()

        media = meta.get("media")
        if isinstance(media, str):
            media = [media]
        if not media:
            media = sorted(
                p.name for p in folder.iterdir() if p.suffix.lower() in MEDIA_EXTENSIONS
            )

        post = Post(
            name=name,
            folder=folder,
            caption=caption or "",
            media=list(media),
            publish_at=_parse_time(meta["publish_at"]) if meta.get("publish_at") else None,
        )
        if not post.media:
            post.warnings.append("No media found (Instagram supports JPEG images and MP4/MOV videos)")
        for item in post.media:
            if not item.startswith("https://") and not (folder / item).is_file():
                post.warnings.append(f"Media file not found: {item}")
        if len(post.media) > 10:
            post.warnings.append("More than 10 media items; a carousel allows at most 10")
        return post

    def list_pending(self) -> list[Post]:
        if not self.pending_dir.is_dir():
            return []
        return [
            self.load(p.name)
            for p in sorted(self.pending_dir.iterdir())
            if p.is_dir() and not p.name.startswith(".")
        ]

    def media_urls(self, post: Post) -> list[str]:
        """Turn local media paths into the public URLs Instagram will download from."""
        urls = []
        for item in post.media:
            if item.startswith("https://"):
                urls.append(item)
                continue
            if not self.public_media_base_url:
                raise QueueError(
                    f"{post.name}/{item} is a local file, but Instagram can only fetch media "
                    "from a public URL. Set PUBLIC_MEDIA_BASE_URL, or use https:// URLs in post.json."
                )
            rel = (post.folder / item).relative_to(self.posts_dir.resolve()).as_posix()
            urls.append(f"{self.public_media_base_url}/{quote(rel)}")
        return urls

    def mark_published(self, post: Post, result: dict) -> Path:
        self.published_dir.mkdir(parents=True, exist_ok=True)
        dest = self.published_dir / f"{datetime.now().strftime('%Y-%m-%d')}_{post.name}"
        suffix = 1
        while dest.exists():
            suffix += 1
            dest = dest.with_name(f"{dest.name.rsplit('~', 1)[0]}~{suffix}")
        shutil.move(str(post.folder), dest)
        (dest / "result.json").write_text(json.dumps(result, indent=2) + "\n")
        return dest
