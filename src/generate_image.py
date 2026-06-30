from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


def find_candidate_image(source_dir: Path, allowed_formats: list[str]) -> Path | None:
    source_dir.mkdir(parents=True, exist_ok=True)
    allowed = {fmt.lower().lstrip(".") for fmt in allowed_formats}
    candidates = [p for p in source_dir.iterdir() if p.is_file() and p.suffix.lower().lstrip(".") in allowed]
    return sorted(candidates)[0] if candidates else None


def make_placeholder_image(output_dir: Path, config: dict[str, Any]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    width, height = config.get("placeholder_size", [1080, 1080])
    today = datetime.now().strftime("%Y-%m-%d")
    path = output_dir / f"draft_{today}.png"

    image = Image.new("RGB", (width, height), color=(18, 18, 22))
    draw = ImageDraw.Draw(image)
    text = f"x-daily-image-agent\n{today}"

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 64)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=20)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) // 2
    y = (height - text_h) // 2
    draw.multiline_text((x, y), text, fill=(235, 235, 235), font=font, spacing=20, align="center")
    image.save(path)
    return path


def get_daily_image(config: dict[str, Any]) -> tuple[Path, str]:
    source_dir = Path(config["source_dir"])
    output_dir = Path(config["output_dir"])
    candidate = find_candidate_image(source_dir, config["allowed_formats"])
    if candidate is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        stamped = output_dir / f"draft_{datetime.now().strftime('%Y-%m-%d')}_{candidate.name}"
        shutil.copy2(candidate, stamped)
        return stamped, "input_image"
    return make_placeholder_image(output_dir, config), "placeholder"
