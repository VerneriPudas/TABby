import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hello, World!", "Hei maailma!", "Hola, Mundo!", "Bonjour, le monde!", "Hallo, Welt!"]

        self.button = QtWidgets.QPushButton("Click me")
        self.text = QtWidgets.QLabel("Hello, World!",
                                    alignment=QtCore.Qt.AlignCenter)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.text)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(300, 200)
    widget.setStyleSheet("""
        background-color: #262626;
        color: #FFFFFF;
        font-family: Titillium;
        font-size: 18px;
        """)
    widget.show()

    sys.exit(app.exec())
        
