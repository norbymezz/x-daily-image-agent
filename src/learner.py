from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


def propose_learning(logs_dir: Path, event: dict) -> None:
    logs_dir.mkdir(parents=True, exist_ok=True)
    path = logs_dir / 'learner_suggestions.json'
    existing = []
    if path.exists():
        existing = json.loads(path.read_text(encoding='utf-8'))
    existing.append({
        'date': datetime.now().isoformat(timespec='seconds'),
        'observation': 'Daily image pipeline executed.',
        'candidate_learning': event,
        'status': 'pending_curator_review'
    })
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding='utf-8')
