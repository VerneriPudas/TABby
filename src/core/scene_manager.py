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

    def switch_scene(self, name: str) -> list[dict]:
        """Activate a new scene by name and return its tracks."""
        self.activate(name)
        return self.get_active_scene_tracks()

    def __init__(self, config_path: str | None = None) -> None:
        self._config_path = config_path
        self._scenes = load_scenes(config_path) if config_path else {}
        self._validate_and_normalize_scenes()
        self.active: ActiveScene | None = None

    def _validate_and_normalize_scenes(self) -> None:
        """Ensure all scenes and tracks have required fields and types."""
        for scene_name, scene_list in self._scenes.items():
            for scene in scene_list:
                # Ensure scene has a name
                if not hasattr(scene, 'name') or not scene.name:
                    scene.name = scene_name
                # Ensure scene has a description (optional, default None)
                if not hasattr(scene, 'description'):
                    scene.description = None
                # Ensure tracks is a list (empty list is valid)
                if not hasattr(scene, 'tracks') or not isinstance(scene.tracks, list):
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
        # placeholder: set active scene
        self.active = ActiveScene(name=name, tracks=self._scenes[name])

    def get_scene_description(self, name: str) -> str | None:
        """Return the description of a scene, or None if not present."""
        scenes = self._scenes.get(name)
        if not scenes or not scenes[0]:
            return None
        return getattr(scenes[0], 'description', None) if hasattr(scenes[0], 'description') else None

    def get_scene_tracks(self, name: str) -> list[dict]:
        """Return the list of tracks (dicts) for a scene name."""
        scenes = self._scenes.get(name)
        if not scenes or not scenes[0]:
            return []
        # scenes[0] is a Scene dataclass; expect .tracks to be a list of dicts
        return getattr(scenes[0], 'tracks', [])

    def get_active_scene_tracks(self) -> list[dict]:
        """Return the list of tracks for the currently active scene."""
        if not self.active or not self.active.tracks or not self.active.tracks[0]:
            return []
        return getattr(self.active.tracks[0], 'tracks', [])