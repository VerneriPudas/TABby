# 🧭 TABby, Tabletop Audio Buddy – Development Plan

## 📘 Overview

**Project Goal:**  
A lightweight, cross-platform soundscape manager for tabletop gaming or ambience use.

**Core Idea:**  
Users define *scenes* made up of layered audio tracks with configurable volumes and crossfades.  
The app can switch scenes smoothly via terminal commands or an optional minimal GUI.

**License:** MIT  
**Platforms:** Linux (Fedora) & Windows 10/11  
**Languages:** Python 3.12+  
**Versioning:** Semantic Versioning (vMAJOR.MINOR.PATCH)

---

## 🧰 Tech Stack

| Layer | Technology | Notes |
|-------|-------------|-------|
| **Language** | Python 3.12+ | Portable, simple to distribute |
| **Audio Backend** | `pygame.mixer` or `sounddevice` + `pydub` | Cross-platform playback, per-track volume control |
| **Config Format** | YAML (via `PyYAML`) | Human-friendly scene configuration |
| **CLI / UI** | `argparse`, `cmd2`, or `textual` | Command control (CLI first) |
| **Future GUI** | `PySide6` (Qt for Python) | Optional visual interface |
| **Packaging** | `PyInstaller` | Create standalone binaries for Windows and Linux |
| **Tests / CI** | `pytest`, GitHub Actions | Unit tests and cross-platform CI |

---

## 🧩 Architecture
Architecture plan — full architecture details live in architecture_plan.txt.


---

## 🪜 Development Phases

### **Phase 1 – Core CLI MVP**
> Goal: Implement all must-have features with command-line control.

**Features**
- [ ] Parse scenes from YAML config  
- [ ] Load multiple tracks per scene  
- [ ] Control individual track volume  
- [ ] Loop playback for ambient sounds  
- [ ] Crossfade between scenes (configurable duration)  
- [ ] Command-line interface (`list`, `play <scene>`, `stop`, `quit`)  
- [ ] Logging and error handling  
- [ ] Test on Linux (Fedora) and Windows  

**Deliverable:** `v0.1.0` – Fully functional CLI prototype.

---

### **Phase 2 – Stability & Usability**
> Goal: Improve reliability, testing, and configuration options.

**Features**
- [ ] Global settings file (crossfade time, default volume, etc.)  
- [ ] Persistent volume levels per scene  
- [ ] Enhanced error messages and fallback behavior  
- [ ] Unit tests for config parsing, playback, and crossfade  
- [ ] GitHub Actions CI for Linux + Windows builds  

**Deliverable:** `v0.2.0` – Stable CLI release.

---

### **Phase 3 – GUI Enhancement (Nice-to-Have)**
> Goal: Add an optional graphical interface without breaking CLI.

**Features**
- [ ] Simple scene/track list UI (PySide6)  
- [ ] Live volume sliders  
- [ ] Add/remove tracks from scenes  
- [ ] Save modified scenes to config  
- [ ] Hotkeys for quick scene switching  
- [ ] Visual indicators for active/fading scenes  

**Deliverable:** `v0.3.0` – GUI + CLI hybrid version.

---

### **Phase 4 – Community & Release**
> Goal: Polish, document, and publish for public use.

**Tasks**
- [ ] MIT License & Contributor Guide  
- [ ] Comprehensive README with screenshots and examples  
- [ ] PyPI package (`pip install soundscape-manager`)  
- [ ] GitHub Releases with Windows/Linux binaries  
- [ ] Version badges, feature roadmap, and changelog  

**Deliverable:** `v1.0.0` – Public open-source release.

---

## 🧪 Future Ideas

- [ ] Scene sequences / playlists  
- [ ] Randomized ambient variations  
- [ ] MIDI / hotkey triggers  
- [ ] Remote control (networked GM dashboard)  
- [ ] Plugin system for audio effects  

---

## 🐾 Working Title Suggestions

| Candidate | Concept |
|------------|----------|
| **TABby** (*Tabletop Audio Buddy*) | Friendly, memorable, mascot-ready |
| **Bardly** | Your personal bard for D&D sessions |
| **SounDruid** | A druid that shapes your soundscapes |
| **Mixie** | Whimsical and short, from “mix” |
| **EchoFox** | Modern, sleek, fox-themed mascot |

---

## 📦 Versioning

| Version | Milestone | Notes |
|----------|------------|-------|
| **v0.1.0** | CLI MVP | YAML scenes, playback, crossfade |
| **v0.2.0** | Stabilization | Testing, config improvements |
| **v0.3.0** | GUI Release | PySide6 interface |
| **v1.0.0** | Public Launch | MIT license, docs, GitHub release |

---

### ✨ Summary

A cross-platform soundscape companion app for tabletop gaming, built for creators and dungeon masters who want to bring immersive ambience to their sessions — simple, scriptable, and expandable.

---

