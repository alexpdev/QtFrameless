import os
from QtFrameless.qt_api import QLabel, QWidget, QSizePolicy, QHBoxLayout, QPixmap
from QtFrameless.button import TitleBarButton

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
        self.maximizeButton = TitleBarButton("max", parent=self)
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

    def setWindowTitle(self, title: str) -> None:
        """Sets the title bar label."""
        self.label.setText(title)

    def setWindowIcon(self, icon: str) -> None:
        """Sets the window icon."""
        pixmap = QPixmap(icon)
        self.icon.setPixmap(pixmap)

    def mouseDoubleClickEvent(self, _):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mousePressEvent(self, event):
        self._pressed = True
        self._cpos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if not self._pressed:
            return super().mouseMoveEvent(event)
        pos = event.position().toPoint()
        difx, dify = (pos - self._cpos).toTuple()
        geom = self.window().geometry()
        x, y, w, h = geom.x(), geom.y(), geom.width(), geom.height()
        new_coords = x+difx, y+dify, w, h
        self.window().setGeometry(*new_coords)

    def mouseReleaseEvent(self, event):
        self._pressed = False
        self._cpos = None
