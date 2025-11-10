"""Scene manager: loads scene config and manages active scene (stub)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .config_loader import Scene, load_scenes


@dataclass
class ActiveScene:
    name: str
    tracks: List[Scene]


class SceneManager:
    def __init__(self, config_path: str | None = None) -> None:
        self._config_path = config_path
        self._scenes = load_scenes(config_path) if config_path else {}
        self.active: ActiveScene | None = None

    def list_scenes(self) -> list[str]:
        return list(self._scenes.keys())

    def activate(self, name: str) -> None:
        if name not in self._scenes:
            raise KeyError(f"Scene {name} not found")
        # placeholder: set active scene
        self.active = ActiveScene(name=name, tracks=self._scenes[name])
