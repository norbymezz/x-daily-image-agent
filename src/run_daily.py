from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from generate_image import get_daily_image
from learner import propose_learning
from post_to_x import publish_to_x
from validate_image import validate_image


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_config() -> dict[str, Any]:
    path = Path("config.json")
    if not path.exists():
        path = Path("config.example.json")
    return read_json(path, {})


def load_memory() -> dict[str, Any]:
    return read_json(Path("memory.json"), {})


def append_log(logs_dir: Path, event: dict[str, Any]) -> None:
    log_path = logs_dir / "run_log.json"
    data = read_json(log_path, [])
    if not isinstance(data, list):
        data = []
    data.append(event)
    write_json(log_path, data)


def used_hashes_from_log(logs_dir: Path) -> set[str]:
    data = read_json(logs_dir / "run_log.json", [])
    hashes: set[str] = set()
    if isinstance(data, list):
        for event in data:
            if not isinstance(event, dict):
                continue
            image_hash = event.get("metadata", {}).get("sha256")
            if image_hash:
                hashes.add(image_hash)
    return hashes


def main() -> None:
    config = load_config()
    memory = load_memory()
    logs_dir = Path(config["logs_dir"])

    image_path, source = get_daily_image(config)
    ok, errors, metadata = validate_image(image_path, config, used_hashes_from_log(logs_dir))

    publish_result = None
    if ok:
        publish_result = publish_to_x(image_path, config).to_dict()
        if not publish_result["ok"]:
            ok = False
            errors.append(publish_result.get("error") or "publication failed")

    event = {
        "date": datetime.now().isoformat(timespec="seconds"),
        "mode": config.get("post_mode", "draft"),
        "objective": "produce_one_daily_image_candidate_for_manual_x_posting",
        "source": source,
        "candidate_path": str(image_path),
        "valid": ok,
        "errors": errors,
        "metadata": metadata,
        "publish_result": publish_result,
        "memory_version": memory.get("version"),
    }

    append_log(logs_dir, event)
    suggestion = propose_learning(logs_dir, event)
    event["learner_suggestion_status"] = suggestion["status"]

    print(json.dumps(event, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
