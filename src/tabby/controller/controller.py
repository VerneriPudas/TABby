#from src.tabby.ui.ui_interface import start_gui
from src.tabby.core.scene_manager import SceneManager
from src.tabby.core.audio_engine import AudioEngine
from src.tabby.ui.gui import start_gui

def main():
    print("Hello, world! This is the soundscape manager (placeholder).")
    scene_manager = SceneManager() # No parameters -> default config path
    audio_engine = AudioEngine()
    #print(f"Loaded scenes: {scene_manager.list_scenes()}")
    start_gui(scene_manager, audio_engine)


