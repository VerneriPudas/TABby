"""Command-line interface for soundscape-manager."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.core.scene_manager import SceneManager
from src.core.audio_engine import AudioEngine, Track


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="soundscape-manager")
    parser.add_argument("--list", action="store_true", help="List available scenes")
    parser.add_argument("--activate", metavar="SCENE", help="Activate a named scene")
    parser.add_argument("--config", metavar="PATH", help="Path to scenes.yaml config file")
    parser.add_argument("--main-volume", type=int, metavar="PERCENT", help="Set main volume (0-100)")
    return parser

def parse_args(argv=None):
    parser = build_parser()
    return parser.parse_args(argv)

def load_scene_manager(config_path: str) -> SceneManager:
    try:
        return SceneManager(config_path)
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        sys.exit(2)

def list_scenes(manager: SceneManager) -> None:
    scenes = manager.list_scenes()
    if not scenes:
        print("No scenes found in config.")
    else:
        print("Available scenes:")
        for name in scenes:
            desc = manager.get_scene_description(name)
            if desc:
                print(f"- {name}: {desc}")
            else:
                print(f"- {name}")

def play_scene(manager: SceneManager, scene_name: str, main_volume: int | None = None) -> None:
    try:
        tracks = manager.switch_scene(scene_name)
    except KeyError:
        print(f"Scene '{scene_name}' not found.", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"Error activating scene: {e}", file=sys.stderr)
        sys.exit(4)

    try:
        engine = AudioEngine()
        if main_volume is not None:
            engine.set_main_volume(main_volume)
            print(f"Set main volume to {main_volume}%")
        print(f"Activating scene '{scene_name}'...")
        if not tracks:
            print("(No tracks in this scene.)")
        else:
            engine.play_tracks(tracks)
        interactive_playback_loop(engine, manager)
    except Exception as e:
        print(f"Audio error: {e}", file=sys.stderr)
        sys.exit(4)

def interactive_playback_loop(engine: AudioEngine, manager: SceneManager) -> None:
    print("\nPlayback started. Type a number (0-100) to change main volume, 'list' to show tracks, 'change <scene>' to switch scene, or 'q' to quit.")
    try:
        while True:
            user_input = input("main volume (0-100), list, change <scene>, q=quit: ").strip()
            if user_input.lower() == 'q':
                print("Stopping all sounds.")
                engine.stop_all()
                break
            elif user_input.lower() == 'list':
                print("Tracks in current scene:")
                tracks = manager.get_active_scene_tracks()
                for idx, track in enumerate(tracks):
                    path = track.get('path')
                    volume = float(track.get('volume', 1.0))
                    print(f"  {idx+1}. {path} (volume={volume})")
            elif user_input.lower().startswith('change '):
                new_scene = user_input[7:].strip()
                if not new_scene:
                    print("Please specify a scene name after 'change'.")
                    continue
                try:
                    engine.stop_all()
                    tracks = manager.switch_scene(new_scene)
                    print(f"Switched to scene '{new_scene}'.")
                    if not tracks:
                        print("(No tracks in this scene.)")
                    else:
                        engine.play_tracks(tracks)
                except KeyError:
                    print(f"Scene '{new_scene}' not found.")
                except Exception as e:
                    print(f"Error changing scene: {e}")
            else:
                try:
                    vol = int(user_input)
                    if 0 <= vol <= 100:
                        engine.set_main_volume(vol)
                        print(f"Main volume set to {vol}%.")
                    else:
                        print("Please enter a value between 0 and 100.")
                except ValueError:
                    print("Invalid input. Enter a number (0-100), 'list', 'change <scene>', or 'q' to quit.")
    except KeyboardInterrupt:
        print("\nStopping all sounds.")
        engine.stop_all()



def main(argv: list[str] | None = None) -> None:
    ns = parse_args(argv)
    config_path = ns.config or str(Path(__file__).resolve().parents[2] / "config" / "scenes.yaml")
    manager = load_scene_manager(config_path)
    if ns.list:
        list_scenes(manager)
    if ns.activate:
        play_scene(manager, ns.activate, ns.main_volume)


if __name__ == "__main__":
    main()
