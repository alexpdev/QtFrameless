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
    # a simple VLine, like the one you get from designer
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine|self.Sunken)


class Grabber(QtWidgets.QWidget):
    dirty = True
    def __init__(self):
        super(Grabber, self).__init__()
        self.setWindowTitle('Screen grabber')
        # ensure that the widget always stays on top, no matter what
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        # limit widget AND layout margins
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # create a "placeholder" widget for the screen grab geometry
        self.grabWidget = QtWidgets.QWidget()
        self.grabWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(self.grabWidget)

        # let's add a configuration panel
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
        # get the *whole* window geometry, including its titlebar and borders
        frameRect = self.frameGeometry()

        # get the grabWidget geometry and remap it to global coordinates
        grabGeometry = self.grabWidget.geometry()
        grabGeometry.moveTopLeft(self.grabWidget.mapToGlobal(QtCore.QPoint(0, 0)))

        # get the actual margins between the grabWidget and the window margins
        left = frameRect.left() - grabGeometry.left()
        top = frameRect.top() - grabGeometry.top()
        right = frameRect.right() - grabGeometry.right()
        bottom = frameRect.bottom() - grabGeometry.bottom()

        # reset the geometries to get "0-point" rectangles for the mask
        frameRect.moveTopLeft(QtCore.QPoint(0, 0))
        grabGeometry.moveTopLeft(QtCore.QPoint(0, 0))

        # create the base mask region, adjusted to the margins between the
        # grabWidget and the window as computed above
        region = QtGui.QRegion(frameRect.adjusted(left, top, right, bottom))
        # "subtract" the grabWidget rectangle to get a mask that only contains
        # the window titlebar, margins and panel
        region -= QtGui.QRegion(grabGeometry)
        self.setMask(region)

        # update the grab size according to grabWidget geometry
        self.widthLabel.setText(str(self.grabWidget.width()))
        self.heightLabel.setText(str(self.grabWidget.height()))

    def resizeEvent(self, event):
        super(Grabber, self).resizeEvent(event)
        # the first resizeEvent is called *before* any first-time showEvent and
        # paintEvent, there's no need to update the mask until then; see below
        if not self.dirty:
            self.updateMask()

    def paintEvent(self, event):
        super(Grabber, self).paintEvent(event)
        # on Linux the frameGeometry is actually updated "sometime" after show()
        # is called; on Windows and MacOS it *should* happen as soon as the first
        # non-spontaneous showEvent is called (programmatically called: showEvent
        # is also called whenever a window is restored after it has been
        # minimized); we can assume that all that has already happened as soon as
        # the first paintEvent is called; before then the window is flagged as
        # "dirty", meaning that there's no need to update its mask yet.
        # Once paintEvent has been called the first time, the geometries should
        # have been already updated, we can mark the geometries "clean" and then
        # actually apply the mask.
        if self.dirty:
            self.updateMask()
            self.dirty = False


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    grabber = Grabber()
    grabber.show()
    sys.exit(app.exec_())
