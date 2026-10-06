import json
from pathlib import Path
from typing import List

def load_kb(path: str = "kb.json") -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def get_steps(kb: dict, intent: str) -> List[str]:
    entry = kb.get(intent) or {}
    return entry.get("steps", [])