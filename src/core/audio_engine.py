"""
Audio engine: pygame.mixer-based implementation for soundscape-manager.
Handles playback, per-track and main volume, and stopping all sounds.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional

try:
    import pygame
    from pygame import mixer
except ImportError:
    pygame = None
    mixer = None


@dataclass
class Track:
    """A single audio track to be played."""
    path: str
    volume: float = 1.0
    sound: Optional[object] = field(default=None, repr=False)  # pygame.mixer.Sound
    channel: Optional[object] = field(default=None, repr=False)  # pygame.mixer.Channel


class AudioEngine:
    """
    Minimal audio engine using pygame.mixer.
    Provides main volume, per-track volume, and basic playback control.
    """
    def __init__(self, num_channels: int = 8) -> None:
        if pygame is None or mixer is None:
            raise ImportError("pygame.mixer is required for AudioEngine. Please install pygame.")
        if not mixer.get_init():
            mixer.init()
        mixer.set_num_channels(num_channels)
        self._tracks: List[Track] = []
        self._channels: Dict[int, Track] = {}
        self.main_volume: float = 1.0

    def set_main_volume(self, percent: int) -> None:
        """Set the main volume (0-100)."""
        v = max(0, min(100, percent)) / 100.0
        self.main_volume = v
        for track in self._tracks:
            if track.channel is not None:
                track.channel.set_volume(track.volume * self.main_volume)

    def play(self, track: Track) -> None:
        """Load and play a single track (WAV/OGG/MP3)."""
        if not track.sound:
            track.sound = mixer.Sound(track.path)
        channel = mixer.find_channel()
        if channel is None:
            raise RuntimeError("No free audio channels available.")
        channel.set_volume(track.volume * self.main_volume)
        channel.play(track.sound)
        track.channel = channel
        self._tracks.append(track)
        self._channels[getattr(channel, 'get_id', lambda: id(channel))()] = track

    def play_tracks(self, tracks: List[dict]) -> None:
        """Play all tracks in the given list of track dicts."""
        for track in tracks:
            path = track.get('path')
            volume = float(track.get('volume', 1.0))
            print(f"  Playing: {path} (volume={volume})")
            try:
                self.play(Track(path=path, volume=volume))
            except Exception as e:
                print(f"    Error playing {path}: {e}")

    def stop_all(self) -> None:
        """Stop all playing tracks and clear state."""
        mixer.stop()
        self._tracks.clear()
        self._channels.clear()

    def set_volume(self, track: Track, volume: float) -> None:
        """Set volume for a specific track (0.0 to 1.0), affected by main volume."""
        if track.channel is not None:
            track.channel.set_volume(volume * self.main_volume)
        track.volume = volume

    def crossfade(self, from_track: Track, to_track: Track, duration: float) -> None:
        """Crossfade not implemented in POC."""
        raise NotImplementedError("crossfade not implemented in POC")
