"""
Audio engine implementation using the pyo library.
"""
# src/core/audio_engine_pyo.py
from __future__ import annotations
import platform
import threading
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Iterable
import soundfile as sf
from pathlib import Path

try:
    from pyo import Server, SfPlayer, SigTo, sndinfo
except Exception as e:
    raise ImportError("pyo is required for this module. Install it (pip install pyo).") from e


@dataclass
class Track:
    path: str
    volume: float = 1.0
    name: str | None = None
    player: SfPlayer | None = None
    vol_sig: SigTo | None = None
    play_start_time: float | None = None  # System time when .out() was called
    offset: float = 0.0                    # Current position in milliseconds
    is_paused: bool = False
    duration_ms: float = 0.0                  # Total length in milliseconds

    def __post_init__(self) -> None:
        if self.name is None:
            self.name = self.path
        # Get duration immediately using pyo's sndinfo
        info = sndinfo(self.path)
        if info:
            self.duration_ms = info[1] * 1000 # info[1] is duration in seconds


class AudioEngine:
    """
    Audio engine using pyo.

    Key methods:
      - play_tracks(list_of_dicts)  # each dict: {"path": "...", "volume": 0.8}
      - stop_all()
      - set_volume(track, volume)
      - set_main_volume(percent_int)
      - crossfade_scene(new_tracks, duration)
    """
    def __init__(self):
        system = platform.system().lower()

        common_args = dict(
            sr=44100,
            buffersize=1024,
            duplex=0,
        )
        server = Server(duplex=0)
        server.verbosity = 0
        if system == "windows": # Windows audio API kerfuffle
            host_apis = ["mme", "directsound", "asio", "wasapi", "wdm-ks"]
            for host_api in host_apis:
                try:
                    print(f"[AudioEngine] Trying backend: {host_api}")
                    server.reinit(winhost=host_api, **common_args)
                    server.boot().start()
                    print(f"[AudioEngine] Using backend: {host_api}")
                    break

                except Exception as e:
                    print(f"[AudioEngine] Backend {host_api} failed: {e}")

            if server is None:
                raise RuntimeError("No suitable Windows audio backend found for pyo.")

            self.server = server

        else:
            # Linux, macOS
            try:
                server.reinit(host="portaudio", **common_args)
                server.boot().start()
                print("[AudioEngine] Using PortAudio backend.")
            except Exception as e:
                raise RuntimeError("Cannot initialize PortAudio")
        
        # Store active tracks
        self.tracks: list[Track] = []
        
        # Master volume control
        self.master = SigTo(value=1.0, time=0.05)
        print("[AudioEngine] Audio engine initialized successfully.")

    def play_tracks(self, track_dicts: list[dict]):
        """
        Load & play a list of track definitions:
        """
        self.stop_all()

        for info in track_dicts:
            self._play_single_track(info["path"], info.get("volume", 1.0))

    def _play_single_track(self, path: str, volume: float):
        print(f"[AudioEngine] Playing track: {path} at volume {volume}")
        track = Track(path=path, volume=volume)

        track.vol_sig = SigTo(value=volume, time=0.05)

        # Loop=1 means infinite loop
        track.player = SfPlayer(path, loop=1, mul=track.vol_sig * self.master).out()
        
        # Set playback start time to now (in milliseconds)
        track.play_start_time = time.time() * 1000

        self.tracks.append(track)

    def set_master_volume(self, value: float):
        """
        value: 0.0 - 1.0
        """
        value = max(0.0, min(1.0, value))
        self.master.value = value

    def set_track_volume(self, index: int, value: float):
        """
        Change volume of a specific track.
        """
        if 0 <= index < len(self.tracks):
            value = max(0.0, min(1.0, value))
            self.tracks[index].vol_sig.value = value

    def stop_all(self):
        """
        Stop all tracks and clear state.
        """
        for t in self.tracks:
            if t.player is not None:
                t.player.stop()
        self.tracks.clear()

    def pause_track(self, index: int):
        """Pauses a specific track and saves the current position."""
        if 0 <= index < len(self.tracks):
            t = self.tracks[index]
            if t.player and not t.is_paused:
                # Calculate how long it's been playing since the last 'resume' (in milliseconds)
                current_ms = time.time() * 1000
                elapsed_ms = current_ms - t.play_start_time
                t.offset = (t.offset + elapsed_ms) % t.duration_ms
                
                t.player.stop()
                t.is_paused = True
                print(f"[AudioEngine] Paused {t.name} at {t.offset:.2f}ms")

    def resume_track(self, index: int):
        """Resumes a paused track from the saved offset."""
        if 0 <= index < len(self.tracks):
            t = self.tracks[index]
            if t.is_paused:
                # Re-create or re-trigger the player with the offset
                # SfPlayer's offset is in seconds, so convert from milliseconds
                offset_seconds = t.offset / 1000.0
                t.player = SfPlayer(t.path, 
                                   offset=offset_seconds, 
                                   loop=1, 
                                   mul=t.vol_sig * self.master).out()
                
                # Store the time when we resumed (in milliseconds)
                t.play_start_time = time.time() * 1000
                t.is_paused = False
                print(f"[AudioEngine] Resumed {t.name} from {t.offset:.2f}ms")

    def get_track_position(self, track: Track) -> Optional[float]:
        """Calculate current position in milliseconds."""
        if not track:
            return 0.0
        
        if track.is_paused:
            return track.offset
        
        # If playing, calculate time since the last 'resume'
        if track.play_start_time is not None:
            elapsed = (time.time() * 1000) - track.play_start_time
            current_milli_sec = track.offset + elapsed
            
            # Handle looping
            if track.duration_ms > 0:
                current_milli_sec = current_milli_sec % track.duration_ms
                
            return current_milli_sec
            
        return track.offset
    
    def resume_all(self):
        """Resumes all paused tracks."""
        for t in self.tracks:
            if t.is_paused:
                # Re-initialize player with the stored offset
                # SfPlayer's offset is in seconds, so convert from milliseconds
                offset_seconds = t.offset / 1000.0
                t.player = SfPlayer(t.path, offset=offset_seconds, loop=1, 
                                mul=t.vol_sig * self.master).out()
                # Store the time when we resumed (in milliseconds)
                t.play_start_time = time.time() * 1000
                t.is_paused = False

    def get_track_duration(self, track: Track) -> Optional[float]:
        """Returns duration in milliseconds."""
        return track.duration_ms if track else None