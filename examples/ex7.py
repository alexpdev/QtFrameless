import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

info = """
Resizable = False
Draggable = True
Maximizable = True
Minimizable = False
Closable = True
TitleBar = True
"""


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)

        hlayout = QHBoxLayout()
        self.textArea = QTextEdit("Lorem ipsum...")
        hlayout.addWidget(self.textArea)
        self.textArea.setStyleSheet("QTextEdit {color:white;background-color:#212121;border-radius:+16px;}")
        self.sans = QFont("Segoe UI",20)
        self.textArea.setFont(self.sans)
        self.btnLayout = QVBoxLayout()
        self.btnLayout.addWidget(QPushButton("Open"))
        self.btnLayout.addWidget(QPushButton("Setup"))
        self.btnLayout.addWidget(QPushButton("Find"))
        self.setStyleSheet("QPushButton {max-width:200px;color:#4fc3f7;background-color:#424242;border:2px solid #4fc3f7;border-radius:16px;font-size:35px;font-weight:bold;}" + "QPushButton:hover {color:#212121;background-color:#4fc3f7;}" + "QPushButton:pressed {color:white;background-color:#212121;border-color:white;}")
        self.status = QTextEdit()
        self.status.insertPlainText("Successfully loaded" + "\nOpen a file...")
        self.status.setReadOnly(1)
        self.status.setStyleSheet("QTextEdit {color:white;background-color:#212121;border-radius:+16px;font-size:14px;max-width:200px;}")
        self.btnLayout.addWidget(self.status)
        self.setFixedSize(800, 400)
        self.setWindowTitle("Py app")
        hlayout.addLayout(self.btnLayout)

        custom_titlebar = TitleBar()

        lay = QVBoxLayout(self)
        lay.addWidget(custom_titlebar)
        lay.addLayout(hlayout)



class TitleBar(QWidget):
    def __init__(self, parent=None):
        super(TitleBar, self).__init__(parent)

        self.title = QLabel("My Own Bar")

        btn_size = 35

        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size,btn_size)
        self.btn_close.setStyleSheet("background-color: red;")

        self.btn_min = QPushButton("-")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet("background-color: gray;")

        self.btn_max = QPushButton("+")
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(btn_size, btn_size)
        self.btn_max.setStyleSheet("background-color: gray;")

        self.title.setFixedHeight(35)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("background-color: black;color: white;")

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)

        lay.addWidget(self.title)
        lay.addWidget(self.btn_min)
        lay.addWidget(self.btn_max)
        lay.addWidget(self.btn_close)

        self.pressing = False
        self.dragPosition = QPoint()

    def resizeEvent(self, QResizeEvent):
        super(TitleBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.window().width())

    def mousePressEvent(self, event):
        self.start = event.globalPosition().toPoint()
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = event.globalPosition().toPoint()
            delta = self.end - self.start
            self.window().move(self.window().pos() + delta)
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False


    def btn_close_clicked(self):
        self.window().close()

    def btn_max_clicked(self):
        self.window().showMaximized()

    def btn_min_clicked(self):
        self.window().showMinimized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))
    app.setStyleSheet("QWidget {background-color:#424242;border-radius:12px;}")
    app.setFont(QFont("Consolas"))
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
