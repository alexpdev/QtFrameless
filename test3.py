import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

X=0
X2=8
Y=0
Y2=30

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'TEST'
        self.setWindowTitle(self.title)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(640, 480)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.setMouseTracking(True)
        self.widget.setMouseTracking(True)
        self.rightClick = False
        self.leftClick = False
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Fichier')
        fileMenu2 = menubar.addMenu('Outils')
        fileMenu3 = menubar.addAction('Readme')
        self.menu2= QMenuBar(menubar)
        menubar.setCornerWidget(self.menu2, Qt.TopRightCorner)
        fileMenu4 = self.menu2.addAction(" -- ")
        fileMenu5 = self.menu2.addAction(" // ")
        Exit = self.menu2.addAction(" X ")
        Exit.triggered.connect(app.exit)
        self.show()

    def mousePressEvent(self, event):
        super(App, self).mousePressEvent(event)

        if event.button() == Qt.RightButton:
            self.rdragx = event.x()
            self.rdragy = event.y()
            self.currentx = self.width()
            self.currenty = self.height()
            self.rightClick = True

        if event.button() == Qt.LeftButton:
            self.leftClick = True
            global X,Y
            X=event.pos().x()
            Y=event.pos().y()

    def mouseMoveEvent(self, event):
        super(App, self).mouseMoveEvent(event)

        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        width5 = width + 5
        widthm5 = width - 5
        height5 = height + 5
        heightm5 = height - 5

        posMouse = event.pos()
        posMouseX = event.x()
        posMouseY = event.y()

        if posMouseX >= widthm5 and posMouseX <= width5:
         QApplication.setOverrideCursor(Qt.SizeHorCursor)
        elif posMouseX >= -5 and posMouseX <= 5:
         QApplication.setOverrideCursor(Qt.SizeHorCursor)
        elif posMouseY >= heightm5 and posMouseY <= height5:
         QApplication.setOverrideCursor(Qt.SizeVerCursor)
        elif posMouseY >= -5 and posMouseY <= 5:
         QApplication.setOverrideCursor(Qt.SizeVerCursor)
        else:
         QApplication.restoreOverrideCursor()

        if self.rightClick == True:

            x = max(self.widget.minimumWidth(),
                self.currentx + event.x() - self.rdragx)
            y = max(self.widget.minimumHeight(),
                self.currenty + event.y() - self.rdragy)
            self.resize(x, y)

        if self.leftClick == True:
            self.move(event.globalPos().x()-X-X2,event.globalPos().y()-Y-Y2)

    def mouseReleaseEvent(self, event):
        super(App, self).mouseReleaseEvent(event)
        self.rightClick = False
        self.leftClick = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
