from PySide6.QtWidgets import QLabel, QWidget, QSizePolicy, QHBoxLayout
from PySide6.QtGui import QPixmap
from QtFrameless.button import TopBarButton
from QtFrameless.cursor import Cursor


class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel()
        self.setProperty("topBar", "true")
        self.setContentsMargins(0,0,0,0)
        pix = QPixmap("icon.png")
        self.icon = QLabel()
        self.icon.setPixmap(pix)
        self.label.setText("TitleBar")
        self.setMaximumHeight(50)
        self.closeButton = TopBarButton("close", parent=self)
        self.minimizeButton = TopBarButton("min", parent=self)
        self.maximizeButton = TopBarButton("max",parent=self)
        sizePolicy = QSizePolicy()
        sizePolicy.setHorizontalPolicy(QSizePolicy.Policy.Fixed)
        self.closeButton.setSizePolicy(sizePolicy)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(3,3,3,3)
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

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        rect = self.window().rect()
        for i in range(len(Cursor.loc)):
            if i not in [5,3,2] and Cursor.loc[i]["range"](pos, rect):
                self._direction = Cursor.loc[i]
                self._cgeom = self.window().geometry()
                self._cpos = pos
                self._pressed = True
                break

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
            return window.setGeometry(*r)
        for i in range(len(Cursor.loc)):
            a = Cursor.loc[i]["range"](pos, geom)
            if i not in [5,3,2] and a == True:
                self.setCursor(Cursor.loc[i]["shape"])
                break
