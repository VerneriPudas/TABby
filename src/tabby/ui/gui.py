import sys
from PySide6 import QtCore, QtWidgets, QtGui
from src.tabby.core.scene_manager import SceneManager
from src.tabby.core.audio_engine import AudioEngine, Track
from pathlib import Path

GUI_UPDATE_INTERVAL = 50  # milliseconds

class TrackWidget(QtWidgets.QWidget):
    """Widget for displaying a single track with volume slider and position info."""
    
    def __init__(self, track_dict: dict, audio_engine: AudioEngine | None = None, parent=None):
        super().__init__(parent)
        self.track_dict = track_dict
        self.audio_engine = audio_engine
        self.audio_track = None  # Will be set after audio engine plays tracks
        self.duration = None
        
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Track name label
        track_name = track_dict.get('name', track_dict.get('path', 'Unknown'))
        name_label = QtWidgets.QLabel(track_name)
        name_label.setMinimumWidth(150)
        
        # Volume slider
        self.volume_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(int(track_dict.get('volume', 1.0) * 100))
        self.volume_slider.setMaximumWidth(150)
        
        # Volume value display
        self.volume_label = QtWidgets.QLabel(f"{self.volume_slider.value()}%")
        self.volume_label.setMinimumWidth(40)
        
        # Connect slider to update label and track
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        
        # Position label (current position / total length)
        self.position_label = QtWidgets.QLabel(self._format_time(0)+ " / " + self._format_time(0))
        self.position_label.setMinimumWidth(100)
        
        # Timer to update position
        self.position_timer = QtCore.QTimer()
        self.position_timer.setInterval(GUI_UPDATE_INTERVAL)
        self.position_timer.timeout.connect(self.update_position)
        if audio_engine:
            self.position_timer.start()
        
        layout.addWidget(name_label)
        layout.addWidget(self.volume_slider)
        layout.addWidget(self.volume_label)
        layout.addWidget(self.position_label)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def set_audio_track(self, audio_track: Track) -> None:
        """Set the Track object from the audio engine."""
        self.audio_track = audio_track
        self.duration = self.audio_engine.get_track_duration(self.audio_track)
        self.update_position()
    
    def on_volume_changed(self, value: int) -> None:
        """Update volume display and track data."""
        self.volume_label.setText(f"{value}%")
        self.track_dict['volume'] = value / 100.0
    
    def update_position(self) -> None:
        """Update the position display from audio engine."""
        if not self.audio_engine or not self.audio_track:
            return
        
        # Pass the actual Track object, not an index or path
        current_ms = self.audio_engine.get_track_position(self.audio_track)
        
        if current_ms is not None and self.duration is not None:
            self.position_label.setText(f"{self._format_time(current_ms)}/ {self._format_time(self.duration)}")
    
    @staticmethod
    def _format_time(milliseconds: float) -> str:
        """Format milliseconds to MM:SS format."""
        seconds = int(milliseconds / 1000)
        minutes = seconds // 60
        secs = seconds % 60
        milliseconds_remainder = int(milliseconds % 1000)
        return f"{minutes}:{secs:02d}:{milliseconds_remainder:03d}"
    
    def stop_timer(self) -> None:
        """Stop the position update timer."""
        self.position_timer.stop()


class SceneMenuWidget(QtWidgets.QWidget):
    """Widget for displaying and managing the scene menu."""
    
    scene_selected = QtCore.Signal(str)  # Signal emitted when a scene is selected
    
    def __init__(self, scene_manager: SceneManager, parent=None):
        super().__init__(parent)
        self.scene_manager = scene_manager
        
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create list widget for scenes
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        
        # Populate scenes
        self.refresh_scenes()
        
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
    
    def refresh_scenes(self) -> None:
        """Refresh the scene list from the scene manager."""
        self.list_widget.clear()
        scenes = self.scene_manager.list_scenes()
        print(f"Loaded scenes: {scenes}")
        for scene in scenes:
            item = QtWidgets.QListWidgetItem(scene)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.list_widget.addItem(scene)
    
    def on_item_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        """Handle scene selection and emit signal."""
        scene_name = item.text()
        self.scene_selected.emit(scene_name)


class PlayerWidget(QtWidgets.QWidget):
    """Widget for playback control and master volume."""
    
    play_pressed = QtCore.Signal()
    pause_pressed = QtCore.Signal()
    master_volume_changed = QtCore.Signal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Play/Pause button
        self.play_pause_button = QtWidgets.QPushButton("Play")
        self.play_pause_button.setMaximumWidth(100)
        self.play_pause_button.clicked.connect(self.on_play_pause_clicked)
        self.is_playing = False
        
        # Master volume label
        master_vol_label = QtWidgets.QLabel("Master Volume:")
        master_vol_label.setMinimumWidth(100)
        
        # Master volume slider
        self.master_volume_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.master_volume_slider.setMinimum(0)
        self.master_volume_slider.setMaximum(100)
        self.master_volume_slider.setValue(100)
        self.master_volume_slider.setMaximumWidth(200)
        self.master_volume_slider.valueChanged.connect(self.on_master_volume_changed)
        
        # Master volume value display
        self.master_volume_label = QtWidgets.QLabel("100%")
        self.master_volume_label.setMinimumWidth(40)
        
        layout.addWidget(self.play_pause_button)
        layout.addSpacing(20)
        layout.addWidget(master_vol_label)
        layout.addWidget(self.master_volume_slider)
        layout.addWidget(self.master_volume_label)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def on_play_pause_clicked(self) -> None:
        """Toggle between play and pause states."""
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_pause_button.setText("Pause")
            self.play_pressed.emit()
        else:
            self.play_pause_button.setText("Play")
            self.pause_pressed.emit()
    
    def on_master_volume_changed(self, value: int) -> None:
        """Handle master volume slider changes."""
        percentage = value / 100.0
        self.master_volume_label.setText(f"{value}%")
        self.master_volume_changed.emit(percentage)


class GUI(QtWidgets.QWidget):
    def __init__(self, scene_manager: SceneManager, audio_engine: AudioEngine):
        super().__init__()
        self.scene_manager = scene_manager
        self.audio_engine = audio_engine
        self.track_widgets = []  # Store track widgets for linking to audio tracks
        
        # Create scene menu widget
        self.scene_menu = SceneMenuWidget(scene_manager)
        self.scene_menu.scene_selected.connect(self.on_scene_selected)
            
        # Create a placeholder area on the right for scene details
        self.desc_widget = QtWidgets.QLabel("Selected scene details will appear here.")

        # Create a scrollable area for tracks
        self.tracks_container = QtWidgets.QWidget()
        self.tracks_layout = QtWidgets.QVBoxLayout()
        self.tracks_layout.setContentsMargins(0, 0, 0, 0)
        self.tracks_container.setLayout(self.tracks_layout)
        
        tracks_scroll = QtWidgets.QScrollArea()
        tracks_scroll.setWidget(self.tracks_container)
        tracks_scroll.setWidgetResizable(True)

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.addWidget(self.desc_widget)
        content_layout.addWidget(tracks_scroll)
        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(content_layout)

        # Create player widget
        self.player = PlayerWidget()
        self.player.play_pressed.connect(self.on_play_pressed)
        self.player.pause_pressed.connect(self.on_pause_pressed)
        self.player.master_volume_changed.connect(self.on_master_volume_changed)

        # Top layout: scene menu and main content
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.scene_menu, 1)
        top_layout.addWidget(main_widget, 4)
        top_widget = QtWidgets.QWidget()
        top_widget.setLayout(top_layout)

        # Main layout: top content and player at bottom
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(top_widget)
        main_layout.addWidget(self.player)
        self.setLayout(main_layout)
    
    def update_scene_list(self) -> None:
        """Update the scene list in the menu."""
        self.scene_menu.refresh_scenes()

    def on_scene_selected(self, scene_name: str) -> None:
        """Handle scene selection."""
        self.audio_engine.stop_all()
        self.display_scene(scene_name)

    def on_play_pressed(self) -> None:
        """Handle play button press: Resume if paused, otherwise start new."""
        # Check if we have tracks that are simply paused
        any_paused = any(t.is_paused for t in self.audio_engine.tracks)
        
        if any_paused:
            self.audio_engine.resume_all()
        else:
            # Fresh start for the scene
            active_tracks = self.scene_manager.get_active_scene_tracks()
            self.audio_engine.play_tracks(active_tracks)
            
            # Link track widgets to the new audio engine Track objects
            for i, track_widget in enumerate(self.track_widgets):
                if i < len(self.audio_engine.tracks):
                    track_widget.set_audio_track(self.audio_engine.tracks[i])
        
    def on_pause_pressed(self) -> None:
        """Pause all tracks via engine."""
        # We need to loop through and pause each one to save their offsets
        for i in range(len(self.audio_engine.tracks)):
            self.audio_engine.pause_track(i)

    def on_master_volume_changed(self, volume: float) -> None:
        """Handle master volume changes."""
        self.audio_engine.set_master_volume(volume)

    def display_scene(self, scene_name: str) -> None:
        desc = self.scene_manager.get_scene_description(scene_name)
        desc = f"Scene: {scene_name}\nDescription: {desc}"
        self.desc_widget.setText(desc)
        
        # Clear previous tracks
        while self.tracks_layout.count():
            child = self.tracks_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Get tracks from scene
        tracks = self.scene_manager.get_scene_tracks(scene_name)
        
        if not tracks:
            no_tracks_label = QtWidgets.QLabel("No tracks in this scene.")
            self.tracks_layout.addWidget(no_tracks_label)
            self.track_widgets = []
        else:
            self.track_widgets = []
            for track in tracks:
                track_widget = TrackWidget(track, self.audio_engine)
                self.track_widgets.append(track_widget)
                self.tracks_layout.addWidget(track_widget)
        
        # Add stretch to push tracks to top
        self.tracks_layout.addStretch()

        # Activate the scene in the manager (sets it as active but doesn't play)
        self.scene_manager.activate(scene_name)
        
        
def start_gui(scene_manager: SceneManager, audio_engine: AudioEngine) -> None:
    app = QtWidgets.QApplication()
    
    # Set application-level icon (for Windows taskbar and window)
    icon_path = Path(__file__).resolve().parents[2] / "assets" / "skrunkli.png"
    if icon_path.exists():
        app_icon = QtGui.QIcon(str(icon_path))
        app.setWindowIcon(app_icon)
    
    w = GUI(scene_manager, audio_engine)
    w.resize(800, 600)
    
    # Also set on window
    if icon_path.exists():
        w.setWindowIcon(app_icon)
    
    w.show()

    path = None # or "main_menu.qss" for testing
    p = Path(path) if path else Path(__file__).resolve().parent / "main_menu.qss"
    if not p.exists():
        print(f"Stylesheet not found at: {p}. Using default styles.")
        w.setStyleSheet("""
                        background-color: #262626;
                        color: #FFFFFF;
                        font-family: Titillium;
                        font-size: 18px;
                        """)
    else:
        with p.open("r", encoding="utf-8") as f:
            _style = f.read()
            w.setStyleSheet(_style)
    
    sys.exit(app.exec())
