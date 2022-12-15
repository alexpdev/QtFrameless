import sys
if sys.platform == 'win32':
    import win32gui
    import win32con
from PyQt5 import QtCore, QtGui, QtWidgets

info = """
Resizable = False
Draggable = True
Maximizable = True
Minimizable = True
Closable = True
TitleBar = True
"""


# a "fake" button class that we need for hover and click events
class HiddenButton(QtWidgets.QPushButton):
    hover = QtCore.pyqtSignal()
    def __init__(self, parent):
        super(HiddenButton, self).__init__(parent)
        # prevent any painting to keep this button "invisible" while
        # still reacting to its events
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
#        uic.loadUi('titlebar.ui', self)
        # enable the system menu
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
        self.titleOpt.titleBarState = (int(self.windowState()) |
            int(QtWidgets.QStyle.State_Active))

        # create "fake" buttons
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

        # *** END OF SETUP ***

        fileMenu = self.menuBar().addMenu('File')
        fileMenu.addAction('Open')
        fileMenu.addAction('Save')
        workMenu = self.menuBar().addMenu('Work')
        workMenu.addAction('Work something')
        analysisMenu = self.menuBar().addMenu('Analysis')
        analysisMenu.addAction('Analize action')

        # just call the statusBar to create one, we use it for resizing purposes
        self.statusBar()

    def resetTitleHeight(self):
        # minimum height for the menu can change everytime an action is added,
        # removed or modified; let's update it accordingly
        if not self.titleOpt:
            return
        # set the minimum height of the titlebar
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
        # update the window buttons when hovering
        pos = self.mapFromGlobal(QtGui.QCursor.pos())
        for ctrl, btn in self.ctrlButtons.items():
            rect = self.style().subControlRect(QtWidgets.QStyle.CC_TitleBar,
                self.titleOpt, ctrl, self)
            # since the maximize button can become a "restore", ensure that it
            # actually exists according to the current state, if the rect
            # has an actual size
            if rect and pos in rect:
                self.titleOpt.activeSubControls = ctrl
                self.titleOpt.state |= QtWidgets.QStyle.State_MouseOver
                break
        else:
            # no hover
            self.titleOpt.state &= ~QtWidgets.QStyle.State_MouseOver
            self.titleOpt.activeSubControls = QtWidgets.QStyle.SC_None
        self.titleOpt.state |= QtWidgets.QStyle.State_Active
        self.update()

    def showSystemMenu(self, pos=None):
        # show the system menu on windows
        if sys.platform != 'win32':
            return
        if self.__sysMenuLock:
            self.__sysMenuLock = False
            return
        winId = int(self.effectiveWinId())
        sysMenu = win32gui.GetSystemMenu(winId, False)
        if pos is None:
            pos = self.systemButton.mapToGlobal(self.systemButton.rect().bottomLeft())
            self.__sysMenuLock = True
        cmd = win32gui.TrackPopupMenu(sysMenu,
            win32gui.TPM_LEFTALIGN | win32gui.TPM_TOPALIGN | win32gui.TPM_RETURNCMD,
            pos.x(), pos.y(), 0, winId, None)
        win32gui.PostMessage(winId, win32con.WM_SYSCOMMAND, cmd, 0)
        # restore the menu lock to hide it when clicking the system menu icon
        QtCore.QTimer.singleShot(0, lambda: setattr(self, '__sysMenuLock', False))

    def actualWindowTitle(self):
        # window title can show "*" for modified windows
        title = self.windowTitle()
        if title:
            title = title.replace('[*]', '*' if self.isWindowModified() else '')
        return title

    def updateTitleBar(self):
        # compute again sizes when resizing or changing window title
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
        titleWidth = self.fontMetrics().width(title)
        if not title and menuWidth > availableRect.width():
            # resize the menubar to its maximum, but without hiding the buttons
            width = availableRect.width()
        elif menuWidth + titleWidth > availableRect.width():
            # if the menubar and title require more than the available space,
            # divide it equally, giving precedence to the window title space,
            # since it is also necessary for window movement
            width = availableRect.width() // 2
            if menuWidth > titleWidth:
                width = max(left, min(availableRect.width() - titleWidth, width))
            # keep a minimum size for the menu arrow
            if availableRect.width() - width < left:
                width = left
            extButton = self.menuBar().findChild(QtWidgets.QToolButton, 'qt_menubar_ext_button')
            if self.isVisible() and extButton:
                # if the "extButton" is visible (meaning that some item
                # is hidden due to the menubar cannot be completely shown)
                # resize to the last visible item + extButton, so that
                # there's as much space available for the title
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

        # ensure that our internal widget are always on top
        for w in self.widgetHelpers:
            w.raise_()
        self.update()

    # helper function to avoid "ugly" colors on menubar items
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
        # QMainWindow.menuBar() returns a new blank menu bar if none exists
        if not self.__menuBar:
            self.__setMenuBar(QtWidgets.QMenuBar(self))
        return self.__menuBar

    def setCentralWidget(self, widget):
        if self.centralWidget():
            self.centralWidget().removeEventFilter(self)
        # store the top content margin, we need it later
        l, self.__topMargin, r, b = widget.getContentsMargins()
        super(SpecialTitleWindow, self).setCentralWidget(widget)
        # since the central widget always uses all the available space and can
        # capture mouse events, install an event filter to catch them and
        # allow us to grab them
        widget.installEventFilter(self)

    def eventFilter(self, source, event):
        if source == self.centralWidget():
            # do not propagate mouse press events to the centralWidget!
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
        # whenever a window is resized, its button states have to be checked again
        self.checkHoverStates()

    def contextMenuEvent(self, event):
        if event.pos() not in self.menuBar().geometry():
            self.showSystemMenu(event.globalPos())

    def mousePressEvent(self, event):
        if not self.centralWidget() and (event.type() == QtCore.QEvent.MouseButtonPress and
            event.button() == QtCore.Qt.LeftButton and event.y() <= self.titleHeight):
                self.__titleBarMousePos = event.pos()

    def mouseMoveEvent(self, event):
        super(SpecialTitleWindow, self).mouseMoveEvent(event)
        if event.buttons() == QtCore.Qt.LeftButton and self.__titleBarMousePos:
            # move the window
            self.move(self.pos() + event.pos() - self.__titleBarMousePos)

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.maximize()

    def mouseReleaseEvent(self, event):
        super(SpecialTitleWindow, self).mouseReleaseEvent(event)
        self.__titleBarMousePos = None

    def changeEvent(self, event):
        # change the appearance of the titlebar according to the window state
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
            # update the titlebar as soon as it's shown, to ensure that
            # most of the title text is visible
            self.updateTitleBar()

    def resizeEvent(self, event):
        super(SpecialTitleWindow, self).resizeEvent(event)
        # update the centralWidget contents margins, adding the titlebar height
        # to the top margin found before
        if (self.centralWidget() and
            self.centralWidget().getContentsMargins()[1] + self.__topMargin != self.titleHeight):
                l, t, r, b = self.centralWidget().getContentsMargins()
                self.centralWidget().setContentsMargins(
                    l, self.titleHeight + self.__topMargin, r, b)
        # resize the width of the titlebar option, and move its buttons
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
            # move left of the rectangle available for the title to the right of
            # the menubar; if the title is bigger than the available space, elide it
            elided = self.fontMetrics().elidedText(
                title, QtCore.Qt.ElideRight, titleRect.width() - 2)
            qp.drawText(titleRect, QtCore.Qt.AlignCenter, elided)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = SpecialTitleWindow()
    w.setWindowTitle('My window')
    w.show()
    sys.exit(app.exec_())
