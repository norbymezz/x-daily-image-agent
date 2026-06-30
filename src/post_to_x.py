from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import tweepy


@dataclass
class PublishResult:
    ok: bool
    mode: str
    image_path: str
    auth_mode: str | None = None
    media_id: str | None = None
    post_id: str | None = None
    post_url: str | None = None
    error: str | None = None
    response: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def env(name: str) -> str | None:
    value = os.getenv(name)
    return value if value else None


def oauth1_credentials_present() -> bool:
    required = [
        "X_API_KEY",
        "X_API_SECRET",
        "X_ACCESS_TOKEN",
        "X_ACCESS_TOKEN_SECRET",
    ]
    return all(env(name) for name in required)


def publish_with_oauth1(image_path: Path, text: str) -> PublishResult:
    """Publish one image using OAuth 1.0a user credentials.

    This is the shortest local Hello World path for a personal bot:
    API key + API secret + access token + access token secret.

    Tweepy still needs API v1.1 for media upload, then API v2 for create_tweet.
    The rest of the agent should not care about that platform detail.
    """
    api_key = env("X_API_KEY")
    api_secret = env("X_API_SECRET")
    access_token = env("X_ACCESS_TOKEN")
    access_token_secret = env("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        return PublishResult(
            ok=False,
            mode="live",
            auth_mode="oauth1",
            image_path=str(image_path),
            error="missing one of: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET",
        )

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api_v1 = tweepy.API(auth)
    client_v2 = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    media = api_v1.media_upload(filename=str(image_path))
    response = client_v2.create_tweet(text=text, media_ids=[media.media_id])

    post_id = None
    response_data = getattr(response, "data", None)
    if isinstance(response_data, dict):
        post_id = response_data.get("id")

    return PublishResult(
        ok=bool(post_id),
        mode="live",
        auth_mode="oauth1",
        image_path=str(image_path),
        media_id=str(media.media_id),
        post_id=str(post_id) if post_id else None,
        post_url=f"https://x.com/i/web/status/{post_id}" if post_id else None,
        response={"data": response_data} if response_data is not None else None,
        error=None if post_id else "tweet created no id returned",
    )


def publish_to_x(image_path: Path, config: dict[str, Any]) -> PublishResult:
    mode = os.getenv("POST_MODE", config.get("post_mode", "draft")).lower()
    text = os.getenv("POST_TEXT", config.get("post_text", ""))

    if mode != "live":
        return PublishResult(ok=True, mode=mode, image_path=str(image_path), auth_mode="none")

    try:
        if oauth1_credentials_present():
            return publish_with_oauth1(image_path, text=text)

        return PublishResult(
            ok=False,
            mode=mode,
            image_path=str(image_path),
            auth_mode="missing",
            error="local live mode needs OAuth 1.0a env vars: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET",
        )
    except Exception as exc:
        return PublishResult(ok=False, mode=mode, image_path=str(image_path), auth_mode="oauth1", error=str(exc))
