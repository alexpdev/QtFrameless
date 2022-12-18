from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QMainWindow, QFrame, QHBoxLayout, QSizePolicy, QSizeGrip
from PySide6.QtCore import QSize, QRect
from PySide6.QtGui import QCursor, Qt

class GripGeometry:
    x = 0
    y = 0
    width = 0
    height = 0

    def size(self) -> QSize:
        return QSize(self.width, self.height)

    def __call__(self) -> QRect:
        return QRect(self.x, self.y, self.width, self.height)

class Window(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.gripWidth = 5
        self.sideGripSelected = None
        self.updateGeometryOnSideGrip = True
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.__setupUI()
        self.visualize(False)
        self.setGripWidth(self.gripWidth)

    def __setupUI(self):
        self.leftSizeGrip = QFrame(self)
        self.leftSizeGrip.setObjectName(u"leftSizeGrip")
        self.leftSizeGrip.setCursor(QCursor(Qt.SizeHorCursor))
        self.leftSizeGrip.mousePressEvent = self.__leftGripPressEvent
        self.leftSizeGrip.mouseMoveEvent = self.__sideSizeGrip
        self.rightSizeGrip = QFrame(self)
        self.rightSizeGrip.setObjectName(u"rightSizeGrip")
        self.rightSizeGrip.setCursor(QCursor(Qt.SizeHorCursor))
        self.rightSizeGrip.mousePressEvent = self.__rightGripPressEvent
        self.rightSizeGrip.mouseMoveEvent = self.__sideSizeGrip
        self.bottomSizeGripContainer = QFrame(self)
        self.bottomSizeGripContainer.setObjectName(u"bottomSizeGripContainer")
        self.bottomSizeGripLayout = QHBoxLayout(self.bottomSizeGripContainer)
        self.bottomSizeGripLayout.setObjectName(u"bottomSizeGripLayout")
        self.bottomSizeGripLayout.setContentsMargins(0, 0, 0, 0)
        self.bottomSizeGripLayout.setSpacing(0)
        self.bottomLeftSizeGrip = QFrame(self.bottomSizeGripContainer)
        self.bottomLeftSizeGrip.setObjectName(u"bottomLeftSizeGrip")
        self.bottomLeftSizeGrip.setCursor(QCursor(Qt.SizeBDiagCursor))
        self.bottomSizeGripLayout.addWidget(self.bottomLeftSizeGrip, 0, Qt.AlignLeft)
        self.bottomSizeGrip = QFrame(self.bottomSizeGripContainer)
        self.bottomSizeGrip.setObjectName(u"bottomSizeGrip")
        self.bottomSizeGrip.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.bottomSizeGrip.setCursor(QCursor(Qt.SizeVerCursor))
        self.bottomSizeGrip.mousePressEvent = self.__bottomGripPressEvent
        self.bottomSizeGrip.mouseMoveEvent = self.__sideSizeGrip
        self.bottomSizeGripLayout.addWidget(self.bottomSizeGrip)
        self.bottomRightSizeGrip = QFrame(self.bottomSizeGripContainer)
        self.bottomRightSizeGrip.setObjectName(u"bottomRightSizeGrip")
        self.bottomRightSizeGrip.setCursor(QCursor(Qt.SizeFDiagCursor))
        self.bottomSizeGripLayout.addWidget(self.bottomRightSizeGrip, 0, Qt.AlignRight)
        self.topSizeGripContainer = QFrame(self)
        self.topSizeGripContainer.setObjectName(u"topSizeGripContainer")
        self.topSizeGripLayout = QHBoxLayout(self.topSizeGripContainer)
        self.topSizeGripLayout.setObjectName(u"topSizeGripLayout")
        self.topSizeGripLayout.setContentsMargins(0, 0, 0, 0)
        self.topSizeGripLayout.setSpacing(0)
        self.topLeftSizeGrip = QFrame(self.topSizeGripContainer)
        self.topLeftSizeGrip.setObjectName(u"topLeftSizeGrip")
        self.topLeftSizeGrip.setCursor(QCursor(Qt.SizeFDiagCursor))
        self.topSizeGripLayout.addWidget(self.topLeftSizeGrip, 0, Qt.AlignLeft)
        self.topSizeGrip = QFrame(self.topSizeGripContainer)
        self.topSizeGrip.setObjectName(u"topSizeGrip")
        self.topSizeGrip.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.topSizeGrip.setCursor(QCursor(Qt.SizeVerCursor))
        self.topSizeGrip.mousePressEvent = self.__topGripPressEvent
        self.topSizeGrip.mouseMoveEvent = self.__sideSizeGrip
        self.topSizeGripLayout.addWidget(self.topSizeGrip)
        self.topRightSizeGrip = QFrame(self.topSizeGripContainer)
        self.topRightSizeGrip.setObjectName(u"topRightSizeGrip")
        self.topRightSizeGrip.setCursor(QCursor(Qt.SizeBDiagCursor))
        self.topSizeGripLayout.addWidget(self.topRightSizeGrip, 0, Qt.AlignRight)
        cornerSizeGrip = lambda event: self.updateGeometry()
        self.topLeftCorner = QSizeGrip(self.topLeftSizeGrip)
        self.topLeftCorner.mouseReleaseEvent = cornerSizeGrip
        self.topRightCorner = QSizeGrip(self.topRightSizeGrip)
        self.topRightCorner.mouseReleaseEvent = cornerSizeGrip
        self.bottomLeftCorner = QSizeGrip(self.bottomLeftSizeGrip)
        self.bottomLeftCorner.mouseReleaseEvent = cornerSizeGrip
        self.bottomRightCorner = QSizeGrip(self.bottomRightSizeGrip)
        self.bottomRightCorner.mouseReleaseEvent = cornerSizeGrip

    def __topGripPressEvent(self, event):
        self.sideGripSelected = self.topSizeGrip

    def __bottomGripPressEvent(self, event):
        self.sideGripSelected = self.bottomSizeGrip

    def __leftGripPressEvent(self, event):
        self.sideGripSelected = self.leftSizeGrip

    def __rightGripPressEvent(self, event):
        self.sideGripSelected = self.rightSizeGrip

    def __sideSizeGrip(self, event):
        if event.buttons() == Qt.LeftButton:
            gripX, gripY = event.position().toTuple()
            windowX, windowY, windowWidth, windowHeight = self.geometry().getRect()
            if self.sideGripSelected is self.topSizeGrip:
                newWindowHeight = windowHeight - gripY
                newWindowY = windowY + gripY
                if newWindowHeight >= self.minimumHeight() and newWindowHeight <= self.maximumHeight():
                    self.setGeometry(windowX, newWindowY, windowWidth, newWindowHeight)
            elif self.sideGripSelected is self.leftSizeGrip:
                newWindowWidth = windowWidth - gripX
                newWindowX = windowX + gripX
                if newWindowWidth >= self.minimumWidth() and newWindowWidth <= self.maximumWidth():
                    self.setGeometry(newWindowX, windowY, newWindowWidth, windowHeight)
            elif self.sideGripSelected is self.bottomSizeGrip:
                newWindowHeight = windowHeight + gripY
                self.resize(windowWidth, newWindowHeight)
            elif self.sideGripSelected is self.rightSizeGrip:
                newWindowWidth = windowWidth + gripX
                self.resize(newWindowWidth, windowHeight)
            if self.updateGeometryOnSideGrip:
                self.updateGeometry()

    def setGripWidth(self, width: int):
        self.gripWidth = width
        self.topLeftSizeGrip.setFixedSize(self.gripWidth, self.gripWidth)
        self.topRightSizeGrip.setFixedSize(self.gripWidth, self.gripWidth)
        self.bottomLeftSizeGrip.setFixedSize(self.gripWidth, self.gripWidth)
        self.bottomRightSizeGrip.setFixedSize(self.gripWidth, self.gripWidth)
        self.updateGeometry()

    def updateGeometry(self):
        windowWidth = self.width()
        windowHeight = self.height()
        leftGrip = GripGeometry()
        leftGrip.x = 0
        leftGrip.y = self.gripWidth
        leftGrip.width = self.gripWidth
        leftGrip.height = windowHeight - self.gripWidth * 2
        self.leftSizeGrip.setGeometry(leftGrip())
        rightGrip = GripGeometry()
        rightGrip.x = windowWidth - self.gripWidth
        rightGrip.y = self.gripWidth
        rightGrip.width = self.gripWidth
        rightGrip.height = windowHeight - self.gripWidth * 2
        self.rightSizeGrip.setGeometry(rightGrip())
        bottomGripContainer = GripGeometry()
        bottomGripContainer.x = 0
        bottomGripContainer.y = windowHeight - self.gripWidth
        bottomGripContainer.width = windowWidth
        bottomGripContainer.height = self.gripWidth
        self.bottomSizeGripContainer.setGeometry(bottomGripContainer())
        self.bottomSizeGripContainer.resize(bottomGripContainer.size())
        topGripContainer = GripGeometry()
        topGripContainer.x = 0
        topGripContainer.y = 0
        topGripContainer.width = windowWidth
        topGripContainer.height = self.gripWidth
        self.topSizeGripContainer.setGeometry(topGripContainer())
        self.topSizeGripContainer.resize(topGripContainer.size())

    def visualize(self, visual: bool):
        if visual:
            self.leftSizeGrip.setStyleSheet("background: blue;")
            self.rightSizeGrip.setStyleSheet("background: blue;")
            self.bottomSizeGrip.setStyleSheet("background: blue;")
            self.bottomLeftSizeGrip.setStyleSheet("background: red")
            self.bottomRightSizeGrip.setStyleSheet("background: red")
            self.topSizeGrip.setStyleSheet("background: blue;")
            self.topLeftSizeGrip.setStyleSheet("background: red")
            self.topRightSizeGrip.setStyleSheet("background: red")
        else:
            self.leftSizeGrip.setStyleSheet("background: transparent")
            self.rightSizeGrip.setStyleSheet("background: transparent")
            self.bottomSizeGrip.setStyleSheet("background: transparent")
            self.bottomLeftSizeGrip.setStyleSheet("background: transparent")
            self.bottomRightSizeGrip.setStyleSheet("background: transparent")
            self.topSizeGrip.setStyleSheet("background: transparent")
            self.topLeftSizeGrip.setStyleSheet("background: transparent")
            self.topRightSizeGrip.setStyleSheet("background: transparent")

    def hide(self):
        self.leftSizeGrip.hide()
        self.rightSizeGrip.hide()
        self.topSizeGripContainer.hide()
        self.bottomSizeGripContainer.hide()
        super().hide()

    def show(self):
        self.leftSizeGrip.show()
        self.rightSizeGrip.show()
        self.topSizeGripContainer.show()
        self.bottomSizeGripContainer.show()
        super().show()


app = QApplication([])
window = Window()
window.show()
app.exec()
