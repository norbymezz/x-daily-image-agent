from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from PIL import Image


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_image(path: Path, config: dict[str, Any], used_hashes: set[str] | None = None) -> tuple[bool, list[str], dict[str, Any]]:
    errors: list[str] = []
    metadata: dict[str, Any] = {"path": str(path)}

    if not path.exists():
        return False, [f"file not found: {path}"], metadata

    suffix = path.suffix.lower().lstrip(".")
    metadata["format"] = suffix
    if suffix not in {fmt.lower().lstrip(".") for fmt in config["allowed_formats"]}:
        errors.append(f"invalid format: {suffix}")

    size_bytes = path.stat().st_size
    metadata["size_bytes"] = size_bytes
    max_bytes = int(config["max_size_mb"] * 1024 * 1024)
    if size_bytes > max_bytes:
        errors.append(f"file too large: {size_bytes} bytes")

    try:
        with Image.open(path) as img:
            width, height = img.size
            metadata["width"] = width
            metadata["height"] = height
            if width < config["min_width"] or height < config["min_height"]:
                errors.append(f"resolution too small: {width}x{height}")
    except Exception as exc:
        errors.append(f"cannot open image: {exc}")

    file_hash = sha256_file(path)
    metadata["sha256"] = file_hash
    if used_hashes and file_hash in used_hashes:
        errors.append("duplicate image hash")

    return len(errors) == 0, errors, metadata
