"""Audio engine: playback, volume, crossfade (stub implementations).

These are lightweight placeholders to be expanded. They avoid importing heavy audio libs
so the scaffold can be linted and tested quickly.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Track:
    path: str
    volume: float = 1.0


class AudioEngine:
    """Simple placeholder for audio operations."""

    def __init__(self) -> None:
        self._playing: List[Track] = []

    def play(self, track: Track) -> None:
        """Start playback of a track (placeholder)."""
        self._playing.append(track)

    def stop_all(self) -> None:
        """Stop everything (placeholder)."""
        self._playing.clear()

    def crossfade(self, from_track: Track, to_track: Track, duration: float) -> None:
        """Crossfade placeholder. Real implementation should use audio backend."""
        raise NotImplementedError("crossfade not implemented in scaffold")
