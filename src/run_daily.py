from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import shutil

from generate_image import get_daily_image
from validate_image import validate_image
from learner import propose_learning


def load_config() -> dict:
    path = Path('config.json')
    if not path.exists():
        path = Path('config.example.json')
    return json.loads(path.read_text(encoding='utf-8'))


def append_log(logs_dir: Path, event: dict) -> None:
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / 'posted_log.json'
    data = []
    if log_path.exists():
        data = json.loads(log_path.read_text(encoding='utf-8'))
    data.append(event)
    log_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def main() -> None:
    config = load_config()
    image_path = get_daily_image(config)
    ok, errors = validate_image(image_path, config)
    logs_dir = Path(config['logs_dir'])
    event = {
        'date': datetime.now().isoformat(timespec='seconds'),
        'candidate_path': str(image_path),
        'valid': ok,
        'errors': errors,
        'mode': 'draft_only'
    }
    if ok:
        out_dir = Path(config['output_dir'])
        out_dir.mkdir(parents=True, exist_ok=True)
        final_path = out_dir / f"daily_{datetime.now().strftime('%Y%m%d_%H%M%S')}{image_path.suffix.lower()}"
        if image_path.resolve() != final_path.resolve():
            shutil.copy2(image_path, final_path)
        event['output_path'] = str(final_path)
    append_log(logs_dir, event)
    propose_learning(logs_dir, event)
    print(json.dumps(event, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
