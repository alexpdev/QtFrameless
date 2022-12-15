import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

info = """
Resizable = False
Draggable = True
Maximizable = False
Minimizable = False
Closable = False
TitleBar = False
"""

class FramelessWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.label = QLabel("Hello world", self)
        self.offset = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.position().toPoint()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.position().toPoint() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FramelessWidget()
    win.setGeometry(300, 300, 300, 300)
    win.show()
    sys.exit(app.exec())
