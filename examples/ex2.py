import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

info = """
Resizable = True
Draggable = False
Maximizable = False
Minimizable = False
Closable = False
TitleBar = False
"""


T,B,L,R = 0,1,2,3
C = Qt.CursorShape
assets = os.path.join(os.path.dirname(__file__), "assets")


class Window(QWidget):

    cursor = {
        (T, L): C.SizeFDiagCursor,
        (T, None): C.SizeVerCursor,
        (T, R): C.SizeBDiagCursor,
        (None, L): C.SizeHorCursor,
        (None, R): C.SizeHorCursor,
        (B, L): C.SizeBDiagCursor,
        (B, None): C.SizeVerCursor,
        (B, R): C.SizeFDiagCursor,
        (None, None): C.ArrowCursor
    }

    def __init__(self, parent=None, app=None):
        super().__init__(parent=parent)
        self.app = app
        self.setMouseTracking(True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.direction = [None, None]
        self.last_position = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.titleBar = TitleBar(parent=self)
        self.titleBar.show()
        self.layout.addWidget(self.titleBar)
        self.show()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.last_position = event.globalPos()
        event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.NoButton:
            self.hover(event)
        elif event.buttons() == Qt.MouseButton.LeftButton:
            self.drag(event)
        event.accept()
        super().mouseMoveEvent(event)

    def drag(self, event):
        dpos = event.globalPos() - self.last_position
        dx, dy = dpos.x(), dpos.y()
        args = {
            (T, L): (dx, dy, -dx, -dy),
            (T, None): (0, dy, 0, -dy),
            (T, R): (0, dy, dx, -dy),
            (None, L): (dx, 0, -dx, 0),
            (None, R): (0, 0, dx, 0),
            (B, L): (dx, 0, -dx, dy),
            (B, None): (0, 0, 0, dy),
            (B, R): (0, 0, dx, dy),
            (None, None): (0, 0, 0, 0),
        }
        self.grow(*args[self.direction])
        self.last_position = event.globalPos()

    def grow(self, x1, y1, x2, y2):
        point = self.position() + QPoint(x1, y1)
        size = self.size().grownBy(QMargins(0, 0, x2, y2))
        self.setGeometry(QRect(point, size))

    def hover(self, event):
        pos = event.pos()
        x, y, h, w = pos.x(), pos.y(), self.height(), self.width()
        ver = T if y < 6 else B
        if h - y >= 6:
            ver = None
        horiz = L if x < 6 else R
        if w - x >= 6:
            horiz = None
        direction = ver, horiz
        if direction != self.direction:
            self.setCursor(self.cursor[direction])
            self.direction = direction
        event.accept()

    def sizeHint(self):
        return QSize(self.height(), self.width())

    minimumSizeHint = sizeHint


class TitleBar(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.window = parent
        self.setMaximumHeight(15)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.icon = QLabel(self)
        self.layout.addWidget(self.icon)
        self.title = QLabel("title", self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.title)
        self.layout.addStretch(1)
        self.minimize = MinButton(parent=self)
        self.maximize = MaxButton(parent=self)
        self.exit = CloseButton(parent=self)
        self.layout.addWidget(self.minimize)
        self.layout.addWidget(self.maximize)
        self.layout.addWidget(self.exit)
        self.setIcon(os.path.join(assets, "icon.png"))
        self.show()

    def sizeHint(self):
        return QSize(44, 33)

    def minimumSizeHint(self):
        return self.sizeHint()

    def setIcon(self, path):
        icon = QPixmap(path)
        self.icon.setPixmap(icon)

    def setTitle(self, title):
        self.title.setText(title)


class MinButton(QPushButton):

    def __init__(self, text="m", parent=None):
        super().__init__(text, parent)
        self.window = parent
        self.setProperty('MinButton','1')
        self.clicked.connect(self.window.setMinimumSize)
        self.setStyleSheet("background-color: green; border-radius: 25; padding: 2px; margin: 2px; width: 8px; height: 8px;")
        self.show()

class MaxButton(QPushButton):

    def __init__(self, text="M", parent=None):
        super().__init__(text, parent)
        self.window = parent
        self.setProperty('MaxButton','1')
        self.clicked.connect(self.window.setMaximumSize)
        self.setStyleSheet("background-color: yellow; border-radius: 25; padding: 2px; margin: 2px; width: 8px; height: 8px;")
        self.show()

class CloseButton(QPushButton):

    def __init__(self, text="X", parent=None):
        super().__init__(text, parent)
        self.window = parent
        self.setProperty('CloseButton','1')
        self.clicked.connect(self.window.destroy)
        self.setStyleSheet("background-color: red; border-radius: 25; padding: 2px; margin: 2px; width: 8px; height: 8px;")
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
