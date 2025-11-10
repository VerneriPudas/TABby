"""Config loader: parse YAML scenes into Python objects (simple implementation)."""
from __future__ import annotations

import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class Scene:
    name: str
    tracks: List[Dict]


def load_scenes(path: str | None) -> Dict[str, List[Scene]]:
    """Load scenes from a YAML file. Returns a dict mapping scene name to list of tracks.

    If path is None, attempt to load `config/scenes.yaml` relative to repository root.
    """
    p = Path(path) if path else Path(__file__).resolve().parents[2] / "config" / "scenes.yaml"
    if not p.exists():
        return {}
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    scenes: Dict[str, List[Scene]] = {}
    for name, info in data.get("scenes", {}).items():
        scenes[name] = [Scene(name=name, tracks=info.get("tracks", []))]
    return scenes
