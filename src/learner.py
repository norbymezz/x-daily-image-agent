from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def append_json_list(path: Path, item: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_json(path, [])
    if not isinstance(existing, list):
        existing = []
    existing.append(item)
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")


def propose_learning(logs_dir: Path, event: dict[str, Any]) -> dict[str, Any]:
    source = event.get("source", "unknown")
    valid = bool(event.get("valid"))
    errors = event.get("errors", [])

    if valid and source == "input_image":
        observation = "A prepared input image was selected and validated."
        candidate = "Input-folder workflow is viable for daily manual curation."
    elif valid and source == "placeholder":
        observation = "No input image was available; placeholder preserved the daily cycle."
        candidate = "Placeholder generation prevents schedule failure but should not count as final creative output."
    else:
        observation = "Daily image candidate failed validation."
        candidate = "Validation errors should modify either the input image constraints or the source image pool."

    suggestion = {
        "date": datetime.now().isoformat(timespec="seconds"),
        "observation": observation,
        "candidate_learning": candidate,
        "event_ref": {
            "source": source,
            "valid": valid,
            "errors": errors,
            "image_sha256": event.get("metadata", {}).get("sha256"),
        },
        "status": "pending_curator_review",
    }

    append_json_list(logs_dir / "learner_suggestions.json", suggestion)
    return suggestion
