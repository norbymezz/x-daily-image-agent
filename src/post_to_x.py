from __future__ import annotations

import base64
import mimetypes
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import requests


API_BASE = "https://api.x.com"


@dataclass
class PublishResult:
    ok: bool
    mode: str
    image_path: str
    media_id: str | None = None
    post_id: str | None = None
    post_url: str | None = None
    error: str | None = None
    response: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def env_token() -> str | None:
    return os.getenv("X_BEARER_TOKEN") or os.getenv("X_ACCESS_TOKEN")


def infer_media_type(image_path: Path) -> str:
    media_type, _ = mimetypes.guess_type(str(image_path))
    return media_type or "image/png"


def upload_media(image_path: Path, token: str) -> str:
    media_bytes = image_path.read_bytes()
    payload = {
        "media": base64.b64encode(media_bytes).decode("ascii"),
        "media_category": "tweet_image",
        "media_type": infer_media_type(image_path),
        "shared": False,
    }
    response = requests.post(
        f"{API_BASE}/2/media/upload",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"media upload failed: {response.status_code} {response.text}")
    data = response.json()
    media_id = data.get("data", {}).get("id")
    if not media_id:
        raise RuntimeError(f"media upload returned no media id: {data}")
    return media_id


def create_post(media_id: str, token: str, text: str = "", made_with_ai: bool = True) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "text": text,
        "media": {"media_ids": [media_id]},
        "made_with_ai": made_with_ai,
    }
    response = requests.post(
        f"{API_BASE}/2/tweets",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"post create failed: {response.status_code} {response.text}")
    return response.json()


def publish_to_x(image_path: Path, config: dict[str, Any]) -> PublishResult:
    mode = os.getenv("POST_MODE", config.get("post_mode", "draft")).lower()
    text = os.getenv("POST_TEXT", config.get("post_text", ""))
    made_with_ai = bool(config.get("made_with_ai", True))

    if mode != "live":
        return PublishResult(ok=True, mode=mode, image_path=str(image_path))

    token = env_token()
    if not token:
        return PublishResult(ok=False, mode=mode, image_path=str(image_path), error="missing X_BEARER_TOKEN or X_ACCESS_TOKEN")

    try:
        media_id = upload_media(image_path, token)
        response = create_post(media_id, token, text=text, made_with_ai=made_with_ai)
        post_id = response.get("data", {}).get("id")
        post_url = f"https://x.com/i/web/status/{post_id}" if post_id else None
        return PublishResult(
            ok=True,
            mode=mode,
            image_path=str(image_path),
            media_id=media_id,
            post_id=post_id,
            post_url=post_url,
            response=response,
        )
    except Exception as exc:
        return PublishResult(ok=False, mode=mode, image_path=str(image_path), error=str(exc))
