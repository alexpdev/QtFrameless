from PyQt5 import QtCore, QtGui, QtWidgets

info = """
Resizable = False
Draggable = True
Maximizable = True
Minimizable = True
Closable = True
TitleBar = True
"""

class VLine(QtWidgets.QFrame):
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine|self.Sunken)


class Grabber(QtWidgets.QWidget):
    dirty = True
    def __init__(self):
        super(Grabber, self).__init__()
        self.setWindowTitle('Screen grabber')
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.grabWidget = QtWidgets.QWidget()
        self.grabWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(self.grabWidget)

        self.panel = QtWidgets.QWidget()
        layout.addWidget(self.panel)

        panelLayout = QtWidgets.QHBoxLayout()
        self.panel.setLayout(panelLayout)
        panelLayout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(1, 1, 1, 1)

        self.configButton = QtWidgets.QPushButton(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon), '')
        self.configButton.setFlat(True)
        panelLayout.addWidget(self.configButton)

        panelLayout.addWidget(VLine())

        self.fpsSpinBox = QtWidgets.QSpinBox()
        panelLayout.addWidget(self.fpsSpinBox)
        self.fpsSpinBox.setRange(1, 50)
        self.fpsSpinBox.setValue(15)
        panelLayout.addWidget(QtWidgets.QLabel('fps'))

        panelLayout.addWidget(VLine())

        self.widthLabel = QtWidgets.QLabel()
        panelLayout.addWidget(self.widthLabel)
        self.widthLabel.setFrameShape(QtWidgets.QLabel.StyledPanel|QtWidgets.QLabel.Sunken)

        panelLayout.addWidget(QtWidgets.QLabel('x'))

        self.heightLabel = QtWidgets.QLabel()
        panelLayout.addWidget(self.heightLabel)
        self.heightLabel.setFrameShape(QtWidgets.QLabel.StyledPanel|QtWidgets.QLabel.Sunken)

        panelLayout.addWidget(QtWidgets.QLabel('px'))

        panelLayout.addWidget(VLine())

        self.recButton = QtWidgets.QPushButton('rec')
        panelLayout.addWidget(self.recButton)

        self.playButton = QtWidgets.QPushButton('play')
        panelLayout.addWidget(self.playButton)

        panelLayout.addStretch(1000)

    def updateMask(self):
        frameRect = self.frameGeometry()

        grabGeometry = self.grabWidget.geometry()
        grabGeometry.moveTopLeft(self.grabWidget.mapToGlobal(QtCore.QPoint(0, 0)))

        left = frameRect.left() - grabGeometry.left()
        top = frameRect.top() - grabGeometry.top()
        right = frameRect.right() - grabGeometry.right()
        bottom = frameRect.bottom() - grabGeometry.bottom()

        frameRect.moveTopLeft(QtCore.QPoint(0, 0))
        grabGeometry.moveTopLeft(QtCore.QPoint(0, 0))

        region = QtGui.QRegion(frameRect.adjusted(left, top, right, bottom))
        region -= QtGui.QRegion(grabGeometry)
        self.setMask(region)

        self.widthLabel.setText(str(self.grabWidget.width()))
        self.heightLabel.setText(str(self.grabWidget.height()))

    def resizeEvent(self, event):
        super(Grabber, self).resizeEvent(event)
        if not self.dirty:
            self.updateMask()

    def paintEvent(self, event):
        super(Grabber, self).paintEvent(event)
        if self.dirty:
            self.updateMask()
            self.dirty = False


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    grabber = Grabber()
    grabber.show()
    sys.exit(app.exec_())
