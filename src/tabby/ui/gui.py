import sys
import src.tabby.core.scene_manager as scene_manager
from PySide6 import QtCore, QtWidgets, QtGui

class GUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create a list of scenes on the left
        menu_widget = QtWidgets.QListWidget()
        #scenes = scene_manager.SceneManager().list_scenes()
        scenes = ["Scene 1", "Scene 2", "Scene 3"]  # Placeholder until SceneManager is implemented
        print(f"Loaded scenes: {scenes}")
        for i, scene in enumerate(scenes):
            item = QtWidgets.QListWidgetItem(f"{scene} {i}")
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            menu_widget.addItem(scene)
            
        # Create a placeholder area on the right
        text_widget = QtWidgets.QLabel("placeholder")

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.addWidget(text_widget)
        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(content_layout)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(menu_widget, 1)
        layout.addWidget(main_widget, 4)
        self.setLayout(layout)

def start_gui() -> None:
    # raise NotImplementedError("GUI not implemented in scaffold")
    app = QtWidgets.QApplication()
    w = GUI()
    w.resize(800, 600)
    w.show()
    
    sys.exit(app.exec())
