import os
from QtFrameless.qt_api import QApplication, QMainWindow, QVBoxLayout, QWidget, Qt
from QtFrameless.titleBar import TitleBar
from QtFrameless.style import stylesheet
from QtFrameless.cursor import Cursor

class FramelessWindow(QMainWindow):
    """A frameless MainWindow widget."""

    def __init__(self, parent=None, titleBarClass=None):
        """Construct new frameless Qt widget."""
        super().__init__(parent=parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.setStyleSheet(stylesheet)
        self.setObjectName('MainWindow')
        self.setContentsMargins(4,4,4,4)
        self._central = QWidget(parent=self)
        self._central.setMouseTracking(True)
        self._central.mouseMoveEvent = self.mouseMoveEvent
        self._layout = QVBoxLayout(self._central)
        self._layout.setContentsMargins(0,0,0,0)
        if titleBarClass is not None:
            self.titleBar = titleBarClass()
        else:
            self.titleBar = TitleBar(self)
        self._layout.addWidget(self.titleBar)
        self._layout.addStretch(1)
        self._main = QWidget(self)
        self._layout.addWidget(self._main)
        self._direction = None
        self._cgeom = None
        self._cpos = None
        self._pressed = None
        super().setCentralWidget(self._central)

    def setTitleBar(self, titleBarClass):
        item = self._layout.takeAt(0)
        item.widget().deleteLater()
        self.titleBar = titleBarClass()
        self._layout.insertWidget(0, self.titleBar)

    def setStyleSheet(self, qss):
        if not isinstance(qss, str):
            if hasattr(qss, "read"):
                qss = qss.read()
            elif hasattr(qss, "readText"):
                qss = qss.readText()
        elif os.path.exists(qss):
            qss = open(qss, 'tr').read()
        qss = stylesheet + qss
        super().setStyleSheet(qss)

    def setWindowTitle(self, title: str):
        self.titleBar.setWindowTitle(title)

    def setWindowIcon(self, icon: str):
        self.titleBar.setWindowIcon(icon)

    def setCentralWidget(self, widget):
        item = self._layout.takeAt(2)
        item.widget().deleteLater()
        item.widget().destroy()
        self._layout.takeAt(1)
        widget.setContentsMargins(2,2,2,2)
        widget.mouseMoveEvent = self.mouseMoveEvent
        self._layout.addWidget(widget)

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        rect = self.rect()
        self._direction = Cursor.match(pos, rect, [0, 4, 1])
        if self.cursor().shape() != self._direction['shape']:
            self.setCursor(self._direction['shape'])
        self._cgeom = self.geometry()
        self._cpos = pos
        self._pressed = True

    def mouseReleaseEvent(self, _):
        self._pressed = False
        self._cpos = None
        self._direction = None
        self._cgeom = None

    def mouseMoveEvent(self, event):
        geom = self.geometry()
        pos = event.position().toPoint()
        if self._pressed and self._direction["id"] != "standard":
            r = Cursor.resize(self._cpos, pos, geom, self._cgeom, self._direction)
            min_width, min_height = self.minimumSizeHint().toTuple()
            if r[2] > min_width and r[3] > min_height:
                return self.setGeometry(*r)
        shape = Cursor.match(pos, geom, [0, 1, 4])["shape"]
        self.setCursor(shape)



def execute():
    app = QApplication([])
    window = FramelessWindow()
    window.show()
    app.exec()
