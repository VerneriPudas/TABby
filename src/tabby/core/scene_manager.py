"""Scene manager: loads scene config and manages active scene (stub)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict
import yaml
from pathlib import Path


@dataclass
class Scene:
    name: str
    tracks: List[Dict]
    description: str | None = None

class SceneManager:

    def switch_scene(self, name: str) -> list[dict]:
        """Activate a new scene by name and return its tracks."""
        self.activate(name)
        return self.get_active_scene_tracks()

    def __init__(self, config_path: str | None = None) -> None:
        self._config_path = config_path
        self._scenes: Dict[str, Scene] = self.load_scenes(config_path) if config_path else self.load_scenes(None)
        self._validate_and_normalize_scenes()
        self.active: Scene | None = None

    def _validate_and_normalize_scenes(self) -> None:
        """Ensure all scenes and tracks have required fields and types."""
        for scene_name, scene in self._scenes.items():
            # Ensure scene has a name
            if not scene.name:
                scene.name = scene_name
            # Ensure tracks is a list (empty list is valid)
            if not isinstance(scene.tracks, list):
                scene.tracks = []
            # Normalize each track (if any)
            for track in scene.tracks:
                if not isinstance(track, dict):
                    continue
                # Ensure path exists and is a string
                if 'path' not in track or not isinstance(track['path'], str):
                    track['path'] = ''
                # Ensure volume is a float between 0.0 and 1.0
                try:
                    v = float(track.get('volume', 1.0))
                    if not (0.0 <= v <= 1.0):
                        v = 1.0
                    track['volume'] = v
                except Exception:
                    track['volume'] = 1.0

    def list_scenes(self) -> list[str]:
        return list(self._scenes.keys())

    def activate(self, name: str) -> None:
        if name not in self._scenes:
            raise KeyError(f"Scene {name} not found")
        # Set active scene
        self.active = self._scenes[name]

    def get_scene_description(self, name: str) -> str | None:
        """Return the description of a scene, or None if not present."""
        scene = self._scenes.get(name)
        if not scene:
            return None
        return getattr(scene, 'description', None)
    
    def get_scene_attr(self, name: str, attr: str) -> any:
        """Generic method to get an attribute of a scene."""
        scene = self._scenes.get(name)
        if not scene:
            return None
        attr_value = getattr(scene, attr, None)
        return attr_value
        
    def get_scene_tracks(self, name: str) -> list[dict]:
        """Return the list of tracks (dicts) for a scene name."""
        scene = self._scenes.get(name)
        if not scene:
            return []
        return scene.tracks if isinstance(scene.tracks, list) else []

    def get_active_scene_tracks(self) -> list[dict]:
        """Return the list of tracks for the currently active scene."""
        if not self.active or not self.active.tracks:
            return []
        return self.active.tracks if isinstance(self.active.tracks, list) else []
    
    @staticmethod
    def load_scenes(path: str | None) -> Dict[str, Scene]:
        """Load scenes from a YAML file. Returns a dict mapping scene name to list of tracks.

        If path is None, attempt to load `config/scenes.yaml` relative to repository root.
        """
        p = Path(path) if path else Path(__file__).resolve().parents[3] / "config" / "scenes.yaml"
        if not p.exists():
            return {}
        with p.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        scenes: Dict[str, Scene] = {}
        for name, info in data.get("scenes", {}).items():
            if info:
                scenes[name] = Scene(
                    name=name if isinstance(name, str) else "Unnamed Scene",
                    tracks=info.get("tracks", []),
                    description=info.get("description")
                )
            else:
                scenes[name] = Scene(
                    name=name if isinstance(name, str) else "Unnamed Scene",
                    tracks=[],
                    description=None
                )
        return scenes