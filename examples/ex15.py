import sys
from PySide6 import QtCore, QtGui, QtWidgets


info = """
Resizable = False
Draggable = True
Maximizable = True
Minimizable = True
Closable = True
TitleBar = True
"""

class HiddenButton(QtWidgets.QPushButton):
    hover = QtCore.Signal()
    def __init__(self, parent):
        super(HiddenButton, self).__init__(parent)
        self.setUpdatesEnabled(False)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    def enterEvent(self, event):
        self.hover.emit()

    def leaveEvent(self, event):
        self.hover.emit()


class SpecialTitleWindow(QtWidgets.QMainWindow):
    __watchedActions = (
        QtCore.QEvent.ActionAdded,
        QtCore.QEvent.ActionChanged,
        QtCore.QEvent.ActionRemoved
    )
    titleOpt = None
    __menuBar = None
    __titleBarMousePos = None
    __sysMenuLock = False
    __topMargin = 0
    def __init__(self):
        super(SpecialTitleWindow, self).__init__()
        self.widgetHelpers = []
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint
        )
        # set the WindowActive to ensure that the title bar is painted as active
        self.setWindowState(self.windowState() | QtCore.Qt.WindowActive)

        # create a StyleOption that we need for painting and computing sizes
        self.titleOpt = QtWidgets.QStyleOptionTitleBar()
        self.titleOpt.initFrom(self)
        self.titleOpt.titleBarFlags = (
            QtCore.Qt.Window | QtCore.Qt.MSWindowsOwnDC |
            QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint |
            QtCore.Qt.WindowCloseButtonHint
            )
        self.titleOpt.state |= (QtWidgets.QStyle.State_Active |
            QtWidgets.QStyle.State_HasFocus)
        self.systemButton = HiddenButton(self)
        self.systemButton.pressed.connect(self.showSystemMenu)
        self.minimizeButton = HiddenButton(self)
        self.minimizeButton.hover.connect(self.checkHoverStates)
        self.minimizeButton.clicked.connect(self.minimize)
        self.maximizeButton = HiddenButton(self)
        self.maximizeButton.hover.connect(self.checkHoverStates)
        self.maximizeButton.clicked.connect(self.maximize)
        self.closeButton = HiddenButton(self)
        self.closeButton.hover.connect(self.checkHoverStates)
        self.closeButton.clicked.connect(self.close)

        self.ctrlButtons = {
            QtWidgets.QStyle.SC_TitleBarMinButton: self.minimizeButton,
            QtWidgets.QStyle.SC_TitleBarMaxButton: self.maximizeButton,
            QtWidgets.QStyle.SC_TitleBarNormalButton: self.maximizeButton,
            QtWidgets.QStyle.SC_TitleBarCloseButton: self.closeButton,
        }

        self.widgetHelpers.extend([self.minimizeButton, self.maximizeButton, self.closeButton])
        self.resetTitleHeight()
        fileMenu = self.menuBar().addMenu('File')
        fileMenu.addAction('Open')
        fileMenu.addAction('Save')
        workMenu = self.menuBar().addMenu('Work')
        workMenu.addAction('Work something')
        analysisMenu = self.menuBar().addMenu('Analysis')
        analysisMenu.addAction('Analize action')

        self.statusBar()
        self.resize(400, 250)

    def resetTitleHeight(self):
        if not self.titleOpt:
            return
        self.titleHeight = max(
            self.style().pixelMetric(
                QtWidgets.QStyle.PM_TitleBarHeight, self.titleOpt, self),
            self.menuBar().sizeHint().height()
            )
        self.titleOpt.rect.setHeight(self.titleHeight)
        self.menuBar().setMaximumHeight(self.titleHeight)
        if self.minimumHeight() < self.titleHeight:
            self.setMinimumHeight(self.titleHeight)

    def checkHoverStates(self):
        if not self.titleOpt:
            return
        pos = self.mapFromGlobal(QtGui.QCursor.pos())
        for ctrl, btn in self.ctrlButtons.items():
            rect = self.style().subControlRect(QtWidgets.QStyle.CC_TitleBar,
                self.titleOpt, ctrl, self)
            if rect and rect.contains(pos):
                self.titleOpt.activeSubControls = ctrl
                self.titleOpt.state |= QtWidgets.QStyle.State_MouseOver
                break
        else:
            self.titleOpt.state &= ~QtWidgets.QStyle.State_MouseOver
            self.titleOpt.activeSubControls = QtWidgets.QStyle.SC_None
        self.titleOpt.state |= QtWidgets.QStyle.State_Active
        self.update()

    def showSystemMenu(self, pos=None):
        if sys.platform != 'win32':
            return
        if self.__sysMenuLock:
            self.__sysMenuLock = False
            return
        winId = int(self.effectiveWinId())
        if pos is None:
            pos = self.systemButton.mapToGlobal(self.systemButton.rect().bottomLeft())
            self.__sysMenuLock = True
        QtCore.QTimer.singleShot(0, lambda: setattr(self, '__sysMenuLock', False))

    def actualWindowTitle(self):
        title = self.windowTitle()
        if title:
            title = title.replace('[*]', '*' if self.isWindowModified() else '')
        return title

    def updateTitleBar(self):
        menuWidth = self.menuBar().sizeHint().width()
        availableRect = self.style().subControlRect(QtWidgets.QStyle.CC_TitleBar,
            self.titleOpt, QtWidgets.QStyle.SC_TitleBarLabel, self)
        left = availableRect.left()
        if self.menuBar().sizeHint().height() < self.titleHeight:
            top = (self.titleHeight - self.menuBar().sizeHint().height()) // 2
            height = self.menuBar().sizeHint().height()
        else:
            top = 0
            height = self.titleHeight
        title = self.actualWindowTitle()
        titleWidth = self.fontMetrics().boundingRect(title).width()
        if not title and menuWidth > availableRect.width():
            width = availableRect.width()
        elif menuWidth + titleWidth > availableRect.width():
            width = availableRect.width() // 2
            if menuWidth > titleWidth:
                width = max(left, min(availableRect.width() - titleWidth, width))
            if availableRect.width() - width < left:
                width = left
            extButton = self.menuBar().findChild(QtWidgets.QToolButton, 'qt_menubar_ext_button')
            if self.isVisible() and extButton:
                minWidth = extButton.width()
                menuBar = self.menuBar()
                spacing = self.style().pixelMetric(QtWidgets.QStyle.PM_MenuBarItemSpacing)
                for i, action in enumerate(menuBar.actions()):
                    actionWidth = menuBar.actionGeometry(action).width()
                    if minWidth + actionWidth > width:
                        width = minWidth
                        break
                    minWidth += actionWidth + spacing
        else:
            width = menuWidth
        self.menuBar().setGeometry(left, top, width, height)
        for w in self.widgetHelpers:
            w.raise_()
        self.update()

    def __setMenuBar(self, menuBar):
        if self.__menuBar:
            if self.__menuBar in self.widgetHelpers:
                self.widgetHelpers.remove(self.__menuBar)
            self.__menuBar.removeEventFilter(self)
        self.__menuBar = menuBar
        self.widgetHelpers.append(menuBar)
        self.__menuBar.installEventFilter(self)
        self.__menuBar.setNativeMenuBar(False)
        self.__menuBar.setStyleSheet('''
            QMenuBar {
                background-color: transparent;
            }
            QMenuBar::item {
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: palette(button);
            }
        ''')

    def setMenuBar(self, menuBar):
        self.__setMenuBar(menuBar)

    def menuBar(self):
        if not self.__menuBar:
            self.__setMenuBar(QtWidgets.QMenuBar(self))
        return self.__menuBar

    def setCentralWidget(self, widget):
        if self.centralWidget():
            self.centralWidget().removeEventFilter(self)
        l, self.__topMargin, r, b = widget.contentsMargins()
        super(SpecialTitleWindow, self).setCentralWidget(widget)
        widget.installEventFilter(self)

    def eventFilter(self, source, event):
        if source == self.centralWidget():
            if (event.type() == QtCore.QEvent.MouseButtonPress and
                event.button() == QtCore.Qt.LeftButton and
                event.y() <= self.titleHeight):
                    self.__titleBarMousePos = event.pos()
                    event.accept()
                    return True
        elif source == self.__menuBar and event.type() in self.__watchedActions:
            self.resetTitleHeight()
        return super(SpecialTitleWindow, self).eventFilter(source, event)

    def minimize(self):
        self.setWindowState(QtCore.Qt.WindowMinimized)

    def maximize(self):
        if self.windowState() & QtCore.Qt.WindowMaximized:
            self.setWindowState(
                self.windowState() & (~QtCore.Qt.WindowMaximized | QtCore.Qt.WindowActive))
        else:
            self.setWindowState(
                self.windowState() | QtCore.Qt.WindowMaximized | QtCore.Qt.WindowActive)
        self.checkHoverStates()

    def contextMenuEvent(self, event):
        if not self.menuBar().geometry().contains(event.pos()):
            self.showSystemMenu(event.globalPos())

    def mousePressEvent(self, event):
        if not self.centralWidget() and (event.type() == QtCore.QEvent.MouseButtonPress and
            event.button() == QtCore.Qt.LeftButton and event.position().y() <= self.titleHeight):
                self.__titleBarMousePos = event.position()

    def mouseMoveEvent(self, event):
        super(SpecialTitleWindow, self).mouseMoveEvent(event)
        if event.buttons() == QtCore.Qt.LeftButton and self.__titleBarMousePos:
            self.move((event.globalPosition() - self.__titleBarMousePos).toPoint())

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.maximize()

    def mouseReleaseEvent(self, event):
        super(SpecialTitleWindow, self).mouseReleaseEvent(event)
        self.__titleBarMousePos = None

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.ActivationChange:
            if self.isActiveWindow():
                self.titleOpt.titleBarState = (
                    int(self.windowState()) | int(QtWidgets.QStyle.State_Active))
                self.titleOpt.palette.setCurrentColorGroup(QtGui.QPalette.Active)
            else:
                self.titleOpt.titleBarState = 0
                self.titleOpt.palette.setCurrentColorGroup(QtGui.QPalette.Inactive)
            self.update()
        elif event.type() == QtCore.QEvent.WindowStateChange:
            self.checkHoverStates()
        elif event.type() == QtCore.QEvent.WindowTitleChange:
            if self.titleOpt:
                self.updateTitleBar()

    def showEvent(self, event):
        if not event.spontaneous():
            self.updateTitleBar()

    def resizeEvent(self, event):
        super(SpecialTitleWindow, self).resizeEvent(event)
        if (self.centralWidget() and
            self.centralWidget().getContentsMargins()[1] + self.__topMargin != self.titleHeight):
                l, t, r, b = self.centralWidget().getContentsMargins()
                self.centralWidget().setContentsMargins(
                    l, self.titleHeight + self.__topMargin, r, b)
        self.titleOpt.rect.setWidth(self.width())
        for ctrl, btn in self.ctrlButtons.items():
            rect = self.style().subControlRect(
                QtWidgets.QStyle.CC_TitleBar, self.titleOpt, ctrl, self)
            if rect:
                btn.setGeometry(rect)
        sysRect = self.style().subControlRect(QtWidgets.QStyle.CC_TitleBar,
            self.titleOpt, QtWidgets.QStyle.SC_TitleBarSysMenu, self)
        if sysRect:
            self.systemButton.setGeometry(sysRect)
        self.titleOpt.titleBarState = int(self.windowState())
        if self.isActiveWindow():
            self.titleOpt.titleBarState |= int(QtWidgets.QStyle.State_Active)
        self.updateTitleBar()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        self.style().drawComplexControl(QtWidgets.QStyle.CC_TitleBar, self.titleOpt, qp, self)
        titleRect = self.style().subControlRect(QtWidgets.QStyle.CC_TitleBar,
            self.titleOpt, QtWidgets.QStyle.SC_TitleBarLabel, self)
        icon = self.windowIcon()
        if not icon.isNull():
            iconRect = QtCore.QRect(0, 0, titleRect.left(), self.titleHeight)
            qp.drawPixmap(iconRect, icon.pixmap(iconRect.size()))
        title = self.actualWindowTitle()
        titleRect.setLeft(self.menuBar().geometry().right())
        if title:
            elided = self.fontMetrics().elidedText(
                title, QtCore.Qt.ElideRight, titleRect.width() - 2)
            qp.drawText(titleRect, QtCore.Qt.AlignCenter, elided)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = SpecialTitleWindow()
    w.setWindowTitle('My window')
    w.show()
    sys.exit(app.exec())
