from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from QtFrameless.titleBar import TitleBar
from QtFrameless.style import stylesheet
from QtFrameless.cursor import Cursor

class FramelessWindow(QMainWindow):
    """A frameless MainWindow widget."""

    def __init__(self, parent=None, titleBar=None):
        """Construct new frameless Qt widget."""
        super().__init__(parent=parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setContentsMargins(2,2,2,2)
        self.setMouseTracking(True)
        self.setStyleSheet(stylesheet)
        self.resize(300,300)
        self.setObjectName('MainWindow')
        self.central = QWidget(parent=self)
        self.central.setMouseTracking(True)
        self.central.mouseMoveEvent = self.mouseMoveEvent
        self.layout = QVBoxLayout(self.central)
        self.layout.setContentsMargins(2,2,2,2)
        if titleBar is not None:
            self.titleBar = titleBar()
        else:
            self.titleBar = TitleBar(self)
        self.layout.addWidget(self.titleBar)
        self.layout.addStretch(1)
        self.main = QWidget(self)
        self.layout.addWidget(self.main)
        super().setCentralWidget(self.central)
        self._direction = None
        self._cgeom = None
        self._cpos = None
        self._pressed = None

    def setWindowTitle(self, title: str):
        self.titleBar.setWindowTitle(title)

    def setWindowIcon(self, icon: str):
        self.titleBar.setWindowIcon(icon)

    def setCentralWidget(self, widget):
        item = self.layout.takeAt(2)
        item.widget().deleteLater()
        self.layout.takeAt(1)
        self.layout.addWidget(widget)

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
            if self._direction["id"] == "standard":
                return
            r = Cursor.resize(self._cpos, pos, geom, self._cgeom, self._direction)
            min_width, min_height = self.minimumSizeHint().toTuple()
            if r[2] > min_width and r[3] > min_height:
                return self.setGeometry(*r)
        for i in range(len(Cursor.loc)):
            a = Cursor.loc[i]["range"](pos, geom)
            if i not in [0,1,4] and a == True:
                self.setCursor(Cursor.loc[i]["shape"])
                break


def execute():
    app = QApplication([])
    window = FramelessWindow()
    window.show()
    app.exec()
