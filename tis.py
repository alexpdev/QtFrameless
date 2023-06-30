from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


LEFT = Qt.LeftEdge
RIGHT = Qt.RightEdge
TOP = Qt.TopEdge
BOTTOM = Qt.BottomEdge


class Side(QWidget):
    def __init__(self, parent, edge):
        super().__init__(parent)
        if edge == LEFT:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == TOP:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == RIGHT:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        else:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None

    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None


class Main(QMainWindow):
    _edgeSize = 1
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.sides = [
            Side(self, Qt.LeftEdge),
            Side(self, Qt.TopEdge),
            Side(self, Qt.RightEdge),
            Side(self, Qt.BottomEdge),
        ]
        # corner grips should be "on top" of everything, otherwise the side grips
        # will take precedence on mouse events, so we are adding them *after*;
        # alternatively, widget.raise_() can be used
        self.corners = [QSizeGrip(self) for _ in range(4)]
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)
        self.editor = QTextEdit()
        self.layout.addWidget(self.editor)

    @property
    def gripSize(self):
        return self._edgeSize

    def setGripSize(self, size):
        if size == self._edgeSize:
            return
        self._edgeSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
            -self.gripSize, -self.gripSize)
        self.corners[0].setGeometry(
            QRect(outRect.topLeft(), inRect.topLeft()))
        self.corners[1].setGeometry(
            QRect(outRect.topRight(), inRect.topRight()).normalized())
        self.corners[2].setGeometry(
            QRect(inRect.bottomRight(), outRect.bottomRight()))
        self.corners[3].setGeometry(
            QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        self.sides[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())
        self.sides[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)
        self.sides[2].setGeometry(
            inRect.left() + inRect.width(),
            inRect.top(), self.gripSize, inRect.height())
        self.sides[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(),
            inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateGrips()


app = QApplication([])
m = Main()
m.show()
m.resize(240, 160)
app.exec_()
