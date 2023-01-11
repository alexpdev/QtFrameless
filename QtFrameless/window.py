import os
from QtFrameless.qt_api import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    Qt
)
from QtFrameless.titleBar import TitleBar #, mouseMoveEvent, mousePressEvent, mouseReleaseEvent
from QtFrameless.style import stylesheet


class FramelessWindow(QMainWindow):
    """A frameless MainWindow widget."""

    def __init__(self, parent=None, titleBarClass=None):
        """Construct new frameless Qt widget."""
        super().__init__(parent=parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.setStyleSheet(stylesheet)
        self.setObjectName("MainWindow")
        self.setContentsMargins(4, 4, 4, 4)
        self._central = QWidget(parent=self)
        self._layout = QVBoxLayout(self._central)
        self._layout.setContentsMargins(0, 0, 0, 0)
        if titleBarClass is not None:
            self.titleBar = titleBarClass()
            self.titleBar.mouseMoveEvent = TitleBar.mouseMoveEvent
            self.titleBar.mouseReleaseEvent = TitleBar.mouseReleaseEvent
            self.titleBar.mousePressEvent = TitleBar.mousePressEvent
        else:
            self.titleBar = TitleBar(self)
        self._layout.addWidget(self.titleBar)
        self._layout.addStretch(1)
        self._main = QWidget(self)
        self._layout.addWidget(self._main)
        self.statusbar = self.statusBar()
        super().setCentralWidget(self._central)

    def setTitleBar(self, titleBarClass):
        item = self._layout.takeAt(0)
        item.widget().deleteLater()
        self.titleBar = titleBarClass()
        self._layout.insertWidget(0, self.titleBar)

    def setStyleSheet(self, qss):
        if not isinstance(qss, str):
            if hasattr(qss, "read"):
                qss = qss.read()
            elif hasattr(qss, "readText"):
                qss = qss.readText()
        elif os.path.exists(qss):
            qss = open(qss, "tr").read()
        qss = stylesheet + qss
        super().setStyleSheet(qss)

    def setWindowTitle(self, title: str):
        self.titleBar.setWindowTitle(title)

    def setWindowIcon(self, icon: str):
        self.titleBar.setWindowIcon(icon)

    def setCentralWidget(self, widget):
        item = self._layout.takeAt(2)
        item.widget().deleteLater()
        item.widget().destroy()
        self._layout.takeAt(1)
        widget.setContentsMargins(2, 2, 2, 2)
        widget.mouseMoveEvent = self.mouseMoveEvent
        self._layout.addWidget(widget)


def execute():
    app = QApplication([])
    window = FramelessWindow()
    window.show()
    app.exec()
