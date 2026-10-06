import json
from pathlib import Path

def load_prompts(path: str = "prompts.json") -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))