from __future__ import annotations

from pathlib import Path
from typing import Any
from PIL import Image


def validate_image(path: Path, config: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not path.exists():
        return False, [f'File not found: {path}']
    suffix = path.suffix.lower().lstrip('.')
    if suffix not in set(config['allowed_formats']):
        errors.append(f'Invalid format: {suffix}')
    max_bytes = int(config['max_size_mb'] * 1024 * 1024)
    if path.stat().st_size > max_bytes:
        errors.append('File too large')
    try:
        with Image.open(path) as img:
            w, h = img.size
            if w < config['min_width'] or h < config['min_height']:
                errors.append(f'Resolution too small: {w}x{h}')
    except Exception as exc:
        errors.append(f'Cannot open image: {exc}')
    return len(errors) == 0, errors
