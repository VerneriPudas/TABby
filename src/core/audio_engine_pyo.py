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

try:
    from pyo import Server, SfPlayer, SigTo, Mix
except Exception as e:
    raise ImportError("pyo is required for this module. Install it (pip install pyo).") from e


@dataclass
class Track:
    path: str
    volume: float = 1.0
    player: SfPlayer | None = None
    vol_sig: SigTo | None = None


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

    def play_tracks(self, track_dicts: list[dict]):
        """
        Load & play a list of track definitions:
        """
        self.stop_all()

        for info in track_dicts:
            self._play_single_track(info["path"], info.get("volume", 1.0))

    def _play_single_track(self, path: str, volume: float):
        track = Track(path=path, volume=volume)

        track.vol_sig = SigTo(value=volume, time=0.05)

        # Loop=1 means infinite loop
        track.player = SfPlayer(path, loop=1, mul=track.vol_sig * self.master).out()

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
