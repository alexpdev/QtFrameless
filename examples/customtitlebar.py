from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from QtFrameless import FramelessWindow

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QHBoxLayout(self)
        self.setup_menubar()
        self.button = QPushButton("CLOSE", self)
        self.button.clicked.connect(app.exit)
        self.layout.addWidget(self.menu_bar)
        self.layout.addWidget(self.button)
        self.setMaximumHeight(50)

    def setup_menubar(self):
        self.menu_bar = QMenuBar()
        self.file_menu = QMenu("File")
        self.options_menu = QMenu("Options")
        self.edit_menu = QMenu("Edit")
        self.menu_bar.addMenu(self.options_menu)
        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.edit_menu)
        self.save_action = QAction("Save")
        self.exit_action = QAction("Exit")
        self.about_action = QAction("About")
        self.copy_action = QAction("Copy")
        self.paste_action = QAction("Paste")
        self.cut_action = QAction("Cut")
        self.file_menu.addActions([self.save_action, self.exit_action])
        self.edit_menu.addActions(
            [self.copy_action, self.cut_action, self.paste_action])
        self.options_menu.addAction(self.about_action)

if "main" in __name__:
    app = QApplication([])
    window = FramelessWindow(titleBarClass=TitleBar)
    window.show()
    app.exec()
