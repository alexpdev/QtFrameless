from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from QtFrameless.window import FramelessWindow
import pytest

@pytest.fixture(scope="package")
def app():
    app = QApplication([])
    return app


def test_frameless_window(app):
    window = FramelessWindow()
    assert window.titleBar


def test_frameless_window_subclass(app):
    class Win(FramelessWindow):
        def __init__(self, parent=None):
            super().__init__(parent=parent)
            self.textedit = QTextEdit()
            self.setCentralWidget(self.textedit)

    win = Win()
    assert win.textedit
