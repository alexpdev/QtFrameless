import itertools
import random
from PySide6.QtWidgets import QApplication, QPlainTextEdit, QWidget, QPushButton, QVBoxLayout
from QtFrameless import FramelessWindow
import time

colors = [
    "#fff", "#0000ff", "#e8ec35", "#7d189e",
    "#400000", "#222222", "#F51",
    "#33AF11", "#AA1111"
]


class MainWindow(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Text Editor")
        self.central = QWidget(parent=self)
        self.textEdit = QPlainTextEdit(parent=self)
        self.layout = QVBoxLayout(self.central)
        self.setCentralWidget(self.central)
        self.layout.addWidget(self.textEdit)
        self.button = QPushButton("DISCO", parent=self)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.alternate_colors)

    def alternate_colors(self):
        for c1, c2, c3 in itertools.combinations(colors, 3):
            then = time.time()
            lst = [c1, c2, c3]
            random.shuffle(lst)
            self.setStyleSheet(f"""QWidget {{
                                background-color: {lst[0]};
                                border: 1px solid {lst[1]};
                                color: {lst[2]};}}""")
            app.processEvents()
            while time.time() - then < .25: pass

if "main" in __name__:
    app = QApplication([])
    window = MainWindow()
    window.show()
    window.textEdit.setPlainText("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
    app.exec()
