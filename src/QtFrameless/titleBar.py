import os
from .qt_api import QLabel, QWidget, QSizePolicy, QHBoxLayout, QPixmap, Qt
from .button import TitleBarCloseButton, TitleBarMaxButton, TitleBarMinButton

icon = os.path.join(os.path.dirname(__file__), "home.png")


class TitleBar(QWidget):
    """Custom titlebar for a frameless QMainWindow."""

    def __init__(self, parent=None):
        """Construct for titlebar."""
        super().__init__(parent=parent)
        self.setObjectName("TitleBarWidget")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.label = QLabel()
        self.label.setText("TitleBar")
        self.setMaximumHeight(40)
        self.closeButton = TitleBarCloseButton(parent=self)
        self.minimizeButton = TitleBarMinButton(parent=self)
        self.maximizeButton = TitleBarMaxButton(parent=self)
        sizePolicy = QSizePolicy()
        sizePolicy.setHorizontalPolicy(QSizePolicy.Policy.Fixed)
        self.closeButton.setSizePolicy(sizePolicy)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        if os.path.exists(icon):
            pix = QPixmap(icon)
        else:
            pix = QPixmap(25,25)
        self.icon = QLabel()
        self.icon.setPixmap(pix)
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
            return
        pos = event.position().toPoint()
        difx, dify = (pos - self._cpos).toTuple()
        geom = self.window().geometry()
        x, y, w, h = geom.x(), geom.y(), geom.width(), geom.height()
        new_coords = x+difx, y+dify, w, h
        self.window().setGeometry(*new_coords)

    def mouseReleaseEvent(self, event):
        self._pressed = False
        self._cpos = None

    def setMenuBar(self, menubar):
        """Set the menu bar in the title bar."""
        self.menuBar = menubar
        self.layout.insertWidget(1, menubar)
