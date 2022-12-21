from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

from QtFrameless.topwidget import TopBar
from QtFrameless.style import stylesheet
from QtFrameless.cursor import Cursor



class Window(QMainWindow):
    """Window object."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.central = QWidget(parent=self)
        self.central.setMouseTracking(True)
        self.central.mouseMoveEvent = self.mouseMoveEvent
        self.topBar = TopBar(self)
        self.setContentsMargins(3,3,3,3)
        self.layout.addWidget(self.topBar)
        self.layout.setContentsMargins(1,1,1,1)
        self.main = QWidget(self)
        self.resize(300,300)
        self.setStyleSheet(stylesheet)
        self.setMouseTracking(True)
        self.layout.addStretch(1)
        self.layout.addWidget(self.main)
        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)
        self.setObjectName('MainWindow')
        self._direction = None
        self._cgeom = None
        self._cpos = None
        self._pressed = None

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        rect = self.rect()
        for i in range(len(Cursor.loc)):
            if i not in [0, 1, 4] and Cursor.loc[i]["range"](pos, rect):
                self._direction = Cursor.loc[i]
                self._cgeom = self.geometry()
                self._cpos = pos
                self._pressed = True
                break

    def mouseReleaseEvent(self, _):
        self._pressed = False
        self._cpos = None
        self._direction = None
        self._cgeom = None

    def mouseMoveEvent(self, event):
        geom = self.geometry()
        pos = event.position().toPoint()
        if self._pressed:
            r = Cursor.resize(self._cpos, pos, geom, self._cgeom, self._direction)
            return self.setGeometry(*r)
        for i in range(len(Cursor.loc)):
            a = Cursor.loc[i]["range"](pos, geom)
            if i not in [0,1,4] and a == True:
                self.setCursor(Cursor.loc[i]["shape"])
                break


def execute():
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
