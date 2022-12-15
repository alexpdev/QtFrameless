import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

info = """
Resizable = False
Draggable = True
Maximizable = False
Minimizable = False
Closable = False
TitleBar = False
"""

class cssden(QMainWindow):
    def __init__(self):
        super().__init__()

        # <MainWindow Properties>
        self.setFixedSize(320, 450)
        self.setStyleSheet("QMainWindow{background-color: darkgray;border: 1px solid black}")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.center()
        # </MainWindow Properties>

        # <Label Properties>
        self.lbl = QLabel(self)
        self.lbl.setText("test")
        self.lbl.setStyleSheet("QLabel{background-color: rgb(0,0,0); border: 1px solid red; color: rgb(255,255,255); font: bold italic 20pt 'Times New Roman';}")
        self.lbl.setGeometry(5, 5, 60, 40)
        # </Label Properties>

        self.oldPos = self.pos()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        # cp = QMainWindow().availableGeometry().center()
        # qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = cssden()
    sys.exit(app.exec_())
