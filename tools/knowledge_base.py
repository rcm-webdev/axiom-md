import json
from pathlib import Path
from typing import Dict, List, Optional

from langchain.tools import tool

_KB_PATH = Path(__file__).parent.parent / "data" / "knowledge_base.json"

with open(_KB_PATH) as f:
    _KB: List[dict] = json.load(f)

# Build alias index at import time: lowercase alias → entry
_INDEX: Dict[str, dict] = {}
for entry in _KB:
    _INDEX[entry["condition"].lower()] = entry
    for alias in entry.get("aliases", []):
        _INDEX[alias.lower()] = entry


def _lookup(term: str) -> Optional[dict]:
    key = term.strip().lower()
    if key in _INDEX:
        return _INDEX[key]
    for alias in _INDEX:
        if alias in key or key in alias:
            return _INDEX[alias]
    return None


@tool
def query_knowledge_base(condition: str) -> str:
    """Look up clinical evidence for a condition from the local knowledge base.

    Returns a JSON object with summary, interventions, monitoring guidelines,
    and sources. Use this before searching PubMed to check if structured
    evidence already exists locally.
    """
    entry = _lookup(condition)
    if entry is None:
        return json.dumps({"error": f"Condition not found in knowledge base: {condition}"})
    return json.dumps(entry)
