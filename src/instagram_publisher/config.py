from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    """Minimal .env loader so the server works without extra dependencies."""
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass(frozen=True)
class Config:
    access_token: str
    user_id: str | None
    posts_dir: Path
    public_media_base_url: str | None
    api_version: str

    @classmethod
    def from_env(cls) -> "Config":
        _load_dotenv(Path(os.environ.get("ENV_FILE", ".env")))
        return cls(
            access_token=os.environ.get("INSTAGRAM_ACCESS_TOKEN", ""),
            user_id=os.environ.get("INSTAGRAM_USER_ID") or None,
            posts_dir=Path(os.environ.get("POSTS_DIR", "posts")).expanduser().resolve(),
            public_media_base_url=(os.environ.get("PUBLIC_MEDIA_BASE_URL") or "").rstrip("/") or None,
            api_version=os.environ.get("INSTAGRAM_API_VERSION", "v23.0"),
        )
