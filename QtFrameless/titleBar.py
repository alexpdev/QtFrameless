import os
from QtFrameless.qt_api import QLabel, QWidget, QSizePolicy, QHBoxLayout, QPixmap
from QtFrameless.button import TitleBarButton
from QtFrameless.cursor import Cursor

icon = os.path.join(os.path.dirname(__file__), "home.png")

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel()
        self.setProperty("titleBar", "true")
        pix = QPixmap(icon)
        self.icon = QLabel()
        self.icon.setPixmap(pix)
        self.label.setText("TitleBar")
        self.setMaximumHeight(50)
        self.closeButton = TitleBarButton("close", parent=self)
        self.minimizeButton = TitleBarButton("min", parent=self)
        self.maximizeButton = TitleBarButton("max",parent=self)
        sizePolicy = QSizePolicy()
        sizePolicy.setHorizontalPolicy(QSizePolicy.Policy.Fixed)
        self.closeButton.setSizePolicy(sizePolicy)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.icon)
        self.layout.addStretch(1)
        self.layout.addWidget(self.label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.minimizeButton)
        self.layout.addWidget(self.maximizeButton)
        self.layout.addWidget(self.closeButton)
        self.setMouseTracking(True)
        self._pressed = False
        self._cpos = None
        self._cgeom = None
        self._direction = None

    def setWindowTitle(self, title: str) -> None:
        """Sets the title bar label."""
        self.label.setText(title)

    def setWindowIcon(self, icon: str) -> None:
        """Sets the window icon."""
        pixmap = QPixmap(icon)
        self.icon.setPixmap(pixmap)

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        rect = self.window().rect()
        direction = Cursor.match(pos, rect, exclusions=[5,3,2])
        self._direction = direction
        self._cgeom = self.window().geometry()
        self._cpos = pos
        self._pressed = True

    def mouseReleaseEvent(self, _):
        self._pressed = False
        self._cpos = None
        self._direction = None
        self._cgeom = None

    def mouseMoveEvent(self, event):
        window = self.window()
        geom = window.geometry()
        pos = event.position().toPoint()
        if self._pressed:
            r = Cursor.resize(self._cpos, pos, geom, self._cgeom, self._direction)
            min_width, min_height = window.minimumSizeHint().toTuple()
            if r[2] < min_width or r[3] < min_height: return
            return window.setGeometry(*r)
        direction = Cursor.match(pos, geom, [5,3,2])
        self.setCursor(direction["shape"])

    def mouseDoubleClickEvent(self, event):
        pos = event.position().toPoint()
        std = Cursor.loc[8]
        geom = self.window().geometry()
        if std["range"](pos, geom):
            if self.window().isMaximized():
                self.window().showNormal()
            else:
                self.window().showMaximized()
