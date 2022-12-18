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


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.gripSize = 16
        self.grips = []
        for i in range(4):
            grip = QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        self.grips[1].move(rect.right() - self.gripSize, 0)
        self.grips[2].move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        self.grips[3].move(0, rect.bottom() - self.gripSize)

class SideGrip(QWidget):
    def __init__(self, parent, edge):
        QWidget.__init__(self, parent)
        if edge == Qt.LeftEdge:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == Qt.TopEdge:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == Qt.RightEdge:
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
    _gripSize = 8
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.sideGrips = [
            SideGrip(self, Qt.LeftEdge),
            SideGrip(self, Qt.TopEdge),
            SideGrip(self, Qt.RightEdge),
            SideGrip(self, Qt.BottomEdge),
        ]
        self.cornerGrips = [QSizeGrip(self) for i in range(4)]

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
            -self.gripSize, -self.gripSize)

        self.cornerGrips[0].setGeometry(
            QRect(outRect.topLeft(), inRect.topLeft()))
        self.cornerGrips[1].setGeometry(
            QRect(outRect.topRight(), inRect.topRight()).normalized())
        self.cornerGrips[2].setGeometry(
            QRect(inRect.bottomRight(), outRect.bottomRight()))
        self.cornerGrips[3].setGeometry(
            QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(),
            inRect.top(), self.gripSize, inRect.height())
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(),
            inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        self.updateGrips()

if __name__ == "__main__":
    app = QApplication([])
    m = Main()
    m.show()
    m.resize(240, 160)
    app.exec()
