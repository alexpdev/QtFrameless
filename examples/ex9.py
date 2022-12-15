import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

info = """
Resizable = Trueish
Draggable = True
Maximizable = False
Minimizable = False
Closable = False
AlwaysOnTop = True
TitleBar = False
"""


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()


        self.text = QLabel("Hello World",alignment=Qt.AlignCenter)
        self.layout =QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.gripSize = 16
        self.grips = []
        for i in range(4):
            grip = QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)

    def resizeEvent(self, event):
        QWidget.resizeEvent(self, event)
        rect = self.rect()
        self._oldPos = None
        self.grips[1].move(rect.right() - self.gripSize, 0)
        self.grips[2].move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        self.grips[3].move(0, rect.bottom() - self.gripSize)

    def oldPos(self):
        if self._oldPos:
            return self._oldPos
        self.position()

    def mousePressEvent(self, event):
        self._oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):

        delta = QPoint(event.globalPosition().toPoint() - self.oldPos())
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self._oldPos = event.globalPosition().toPoint()




if __name__ == "__main__":
    app =QApplication([])
    window = MyWidget()
    window.show()
    app.exec()
