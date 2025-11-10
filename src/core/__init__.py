"""Core package init."""

from .audio_engine import AudioEngine, Track  # re-export for convenience

__all__ = ["AudioEngine", "Track"]
