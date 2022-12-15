import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

info = """
Resizable = False
Draggable = True
Maximizable = True
Minimizable = True
Closable = True
TitleBar = True
"""

class TitleBar(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Highlight)
        self.minimize=QToolButton(self)
        self.maximize=QToolButton(self)
        close=QToolButton(self)
        self.minimize.setMinimumHeight(10)
        close.setMinimumHeight(10)
        self.maximize.setMinimumHeight(10)
        label=QLabel(self)
        label.setText("Window Title")
        self.setWindowTitle("Window Title")
        hbox=QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(self.minimize)
        hbox.addWidget(self.maximize)
        hbox.addWidget(close)
        hbox.insertStretch(1,500)
        hbox.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        self.maxNormal=False
        close.clicked.connect(self.close)
        self.minimize.clicked.connect(self.showSmall)
        self.maximize.clicked.connect(self.showMaxRestore)

    def showSmall(self):
        box.showMinimized()

    def showMaxRestore(self):
        if(self.maxNormal):
            box.showNormal()
            self.maxNormal= False
        else:
            box.showMaximized()
            self.maxNormal=  True

    def close(self):
        box.close()

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            box.moving = True
            box.offset = event.position()

    def mouseMoveEvent(self,event):
        if box.moving: box.move(event.globalPosition().toPoint()-box.offset)


class Frame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.m_mouse_down= False
        self.setFrameShape(QFrame.StyledPanel)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.m_titleBar= TitleBar(self)
        self.m_content= QWidget(self)
        vbox=QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.setSpacing(0)
        layout=QVBoxLayout(self)
        layout.addWidget(self.m_content)
        layout.setSpacing(0)
        vbox.addLayout(layout)

    def contentWidget(self):
        return self.m_content

    def titleBar(self):
        return self.m_titleBar

    def mousePressEvent(self,event):
        self.m_old_pos = event.position()
        self.m_mouse_down = event.button()== Qt.LeftButton

    def mouseReleaseEvent(self,event):
        self.m_mouse_down=False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    box = Frame()
    box.move(60,60)
    l=QVBoxLayout(box.contentWidget())
    # l.setMargin(0)
    edit=QLabel("""I would've did anything for you to show you how much I adored you
But it's over now, it's too late to save our loveJust promise me you'll think of me
Every time you look up in the sky and see a star 'cuz I'm  your star.""")
    l.addWidget(edit)
    box.show()
    app.exec()
