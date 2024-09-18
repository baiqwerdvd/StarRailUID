import json
from pathlib import Path

EXCEL = Path(__file__).parent

with Path.open(EXCEL / "light_cone_ranks.json", encoding="utf8") as f:
    light_cone_ranks = json.load(f)
