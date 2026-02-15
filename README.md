# TABby - Soundscape Manager

A lightweight, cross-platform soundscape and ambient audio manager built with Python. Create and manage scenes containing multiple audio tracks with individual volume controls, crossfading, and playback management.

## Features

### Core Functionality
- **Scene Management** - Create and organize soundscapes with YAML configuration
- **Multi-track Playback** - Play multiple audio tracks simultaneously with independent volume control
- **Audio Engine** - Built on pyo library for low-latency, cross-platform audio
- **Pause/Resume** - Pause individual tracks or entire scenes with position tracking
- **Master Volume Control** - Global volume management for all playback

### User Interface (PySide6/Qt)
- **Scene Menu** - Browse and select from available soundscapes
- **Track List** - View all tracks in selected scene with:
  - Individual volume sliders
  - Real-time playback position tracking
  - Total track duration display
- **Player Controls** - Play/Pause buttons and master volume slider
- **Scene Details** - View scene descriptions and metadata

## Architecture

### Project Structure
```
src/tabby/
├── core/
│   ├── audio_engine.py      # Pyo-based audio playback engine
│   ├── scene_manager.py     # Scene loading and management
│   └── config_loader.py     # Configuration utilities
├── ui/
│   ├── gui.py               # Main GUI components (Qt/PySide6)
│   └── main_menu.qss        # UI styling
└── utils/
    └── logger.py

config/
└── scenes.yaml              # Scene definitions and track configuration

assets/
└── skrunkli.png             # Application icon
```

### Key Components

**AudioEngine** - Manages playback via pyo
- Multi-track playback with synchronized timing
- Per-track and master volume control
- Pause/resume with position tracking (in milliseconds)
- Track duration caching

**SceneManager** - Handles scene configuration
- Loads scenes from YAML
- Tracks scene metadata (name, description)
- Manages active scene state

**GUI** - Qt-based interface with:
- TrackWidget: Individual track display with volume and position
- SceneMenuWidget: Scene selection and browsing
- PlayerWidget: Playback controls and master volume

## Installation & Usage

### Requirements
- Python 3.8+
- PySide6 (Qt framework)
- pyo (audio engine)
- soundfile (audio file metadata)
- PyYAML (configuration)

### Running the Application
```bash
python -m tabby
```

## Scene Configuration

Scenes are defined in `config/scenes.yaml`:

```yaml
scenes:
  forest:
    description: "Night forest with crickets and distant owl"
    tracks:
      - path: "assets/forest-ambience.mp3"
        volume: 0.4
        name: "Forest Ambience"
      - path: "assets/cricket-sounds.mp3"
        volume: 0.6
        name: "Crickets"
  
  calm:
    description: "Silent scene with no sound"
    tracks: []
```

## Development Notes

- Audio timing is tracked in milliseconds internally
- Position tracking uses system time + elapsed calculations
- All conversions to pyo (which uses seconds) are handled in AudioEngine
- GUI updates position display at 100ms intervals for smooth UX

See `docs/DEVELOPMENT_PLAN.md` for architecture and design decisions.
