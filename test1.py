from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class CustomWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setContentsMargins(0, 0, 0, 0)

    def mouseMoveEvent(self, event: QMouseEvent):
        QApplication.setOverrideCursor(Qt.ArrowCursor)


class CustomTitleBar(QLabel):
    def __init__(self, text, window: QMainWindow):
        super().__init__()
        self.setMouseTracking(True)
        self.setText(text)
        self.parent_window = window
        self.setContentsMargins(0, 0, 0, 0)
        self.parent_window.oldPos = self.parent_window.pos()

    def mousePressEvent(self, event: QMouseEvent):
        self.parent_window.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            delta = QPoint(event.globalPosition().toPoint() - self.parent_window.oldPos)
            self.parent_window.move(self.parent_window.x() + delta.x(), self.parent_window.y() + delta.y())
            self.parent_window.oldPos = event.globalPosition().toPoint()

class FramelessResizableWindow(QMainWindow):
    margin = 6
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.window_margin = self.margin
        self.setContentsMargins(*[self.window_margin]*4)
        self.cursorPositions = CursorPositions()
        self.cursorPositions.actualPosition = CursorPositions.DEFAULT
        self.window_contents = CustomWidget()
        self.setCentralWidget(self.window_contents)
        self.title_bar = CustomWidget()
        self.main_widget = CustomWidget()
        self.vb1 = QVBoxLayout()
        self.hb_title_bar = QHBoxLayout()
        self.hb_title = QHBoxLayout()
        self.hb_title_bar_buttons = QHBoxLayout()
        self.close_button = QPushButton("X")
        self.maximize_button = QPushButton("+")
        self.minimize_button = QPushButton("-")
        self.title = CustomTitleBar("this is a title", self)
        self.title_bar_layout = QHBoxLayout()
        self.setup_main_widget()

    def mousePressEvent(self, event: QMouseEvent):
        x, y = event.globalPosition().toPoint().x(), event.globalPosition().toPoint().y()
        if y < self.window_margin:
            if x < self.window_margin:
                self.cursorPositions.actualPosition = CursorPositions.TOP_LEFT
            else:
                if x > self.width() - self.window_margin:
                    self.cursorPositions.actualPosition = CursorPositions.TOP_RIGHT
                else:
                    self.cursorPositions.actualPosition = CursorPositions.TOP_CENTER
        else:
            if y > self.height() - self.window_margin:
                if x < self.window_margin:
                    self.cursorPositions.actualPosition = CursorPositions.BOTTOM_LEFT
                else:
                    if x > self.width() - self.window_margin:
                        self.cursorPositions.actualPosition = CursorPositions.BOTTOM_RIGHT
                    else:
                        self.cursorPositions.actualPosition = CursorPositions.BOTTOM_CENTER
            else:
                if x < self.window_margin:
                    self.cursorPositions.actualPosition = CursorPositions.MIDDLE_LEFT
                else:
                    if x > self.width() - self.window_margin:
                        self.cursorPositions.actualPosition = CursorPositions.MIDDLE_RIGHT
                    else:
                        self.cursorPositions.actualPosition = CursorPositions.DEFAULT

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.cursorPositions.actualPosition = CursorPositions.DEFAULT

    def mouseMoveEvent(self, event: QMouseEvent):
        x, y = event.position().toPoint().x(), event.position().toPoint().y()
        gx, gy = event.globalPosition().toPoint().x(), event.globalPosition().toPoint().y()
        if self.cursorPositions.actualPosition >= 0:
            if self.cursorPositions.actualPosition <= 2:
                if self.cursorPositions.actualPosition == CursorPositions.TOP_LEFT:
                    bottom_side = y + self.height()
                    top_side = gy
                    right_side = x + self.width()
                    left_side = gx
                    self.setGeometry(QRect(left_side, top_side, right_side - left_side, bottom_side - top_side))
                    pass
                else:
                    if self.cursorPositions.actualPosition == CursorPositions.TOP_CENTER:
                        bottom_side = y + self.height()
                        top_side = gy
                        self.setGeometry(QRect(x, top_side, self.width(), bottom_side - top_side))
                        pass
                    else:
                        deference = gx - x
                        bottom_side = y + self.height()
                        top_side = gy
                        self.setGeometry(QRect(x, top_side, deference, bottom_side - top_side))
                        pass

            else:
                if self.cursorPositions.actualPosition >= 5:
                    if self.cursorPositions.actualPosition == CursorPositions.BOTTOM_LEFT:
                        top_side = y
                        bottom_side = gy
                        right_side = x + self.width()
                        left_side = gx
                        self.setGeometry(QRect(left_side, y, right_side - left_side, bottom_side - top_side))
                        pass
                    else:
                        if self.cursorPositions.actualPosition == CursorPositions.BOTTOM_CENTER:
                            top_side = y
                            bottom_side = gy
                            self.resize(self.width(), bottom_side - top_side)
                            pass
                        else:
                            self.resize(x, y)
                            pass
                else:
                    if self.cursorPositions.actualPosition == CursorPositions.MIDDLE_RIGHT:
                        deference = gx - x
                        self.resize(deference, self.height())
                        pass
                    else:
                        if self.cursorPositions.actualPosition == CursorPositions.MIDDLE_LEFT:
                            right_side = x + self.width()
                            left_side = gx
                            self.setGeometry(QRect(left_side, y, right_side - left_side, self.height()))
                            pass
        else:
            self.change_cursor_shape(event)

    def change_cursor_shape(self, event):
        x, y = event.position().toPoint().x(), event.position().toPoint().y()
        if y < self.window_margin:
            if x < self.window_margin:
                QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
            else:
                if x > self.width() - self.window_margin:
                    QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
                else:
                    QApplication.setOverrideCursor(Qt.SizeVerCursor)
        else:
            if y > self.height() - self.window_margin:
                if x < self.window_margin:
                    QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
                else:
                    if x > self.width() - self.window_margin:
                        QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
                    else:
                        QApplication.setOverrideCursor(Qt.SizeVerCursor)
            else:
                if x < self.window_margin:
                    QApplication.setOverrideCursor(Qt.SizeHorCursor)
                else:
                    if x > self.width() - self.window_margin:
                        QApplication.setOverrideCursor(Qt.SizeHorCursor)
                    else:
                        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def setup_main_widget(self):
        self.setStyleSheet("background-color:white")
        self.vb1.setContentsMargins(0, 0, 0, 0)
        self.hb_title_bar.setContentsMargins(0, 0, 0, 0)
        self.hb_title.setContentsMargins(0, 0, 0, 0)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(12)
        size_policy.setHeightForWidth(self.main_widget.sizePolicy().hasHeightForWidth())
        self.main_widget.setSizePolicy(size_policy)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(1)
        size_policy.setHeightForWidth(self.title_bar.sizePolicy().hasHeightForWidth())
        self.title_bar.setSizePolicy(size_policy)
        self.title_bar.setMinimumSize(0, 30)
        self.main_widget.setContentsMargins(0, 0, 0, 0)
        self.close_button.setMaximumSize(30, 30)
        self.maximize_button.setMaximumSize(30, 30)
        self.minimize_button.setMaximumSize(30, 30)
        self.close_button.clicked.connect(lambda: self.close())
        self.maximize_button.clicked.connect(lambda: self.toggle())
        self.minimize_button.clicked.connect(lambda: self.showMinimized())
        self.hb_title_bar_buttons.addWidget(self.minimize_button)
        self.hb_title_bar_buttons.addWidget(self.maximize_button)
        self.hb_title_bar_buttons.addWidget(self.close_button)
        self.hb_title_bar_buttons.setContentsMargins(0, 0, 0, 0)
        self.hb_title.addWidget(self.title)
        self.title_bar_layout.setContentsMargins(2, 2, 2, 2)
        self.title_bar_layout.addLayout(self.hb_title)
        self.title_bar_layout.addLayout(self.hb_title_bar_buttons)
        self.title_bar.setLayout(self.title_bar_layout)
        self.vb1.addWidget(self.title_bar)
        self.vb1.addWidget(self.main_widget)
        self.vb1.setSpacing(0)
        self.window_contents.setLayout(self.vb1)
        self.main_widget.setStyleSheet("background-color:yellow")
        self.title_bar.setStyleSheet("background-color:blue")
        self.close_button.setStyleSheet("border:1 solid white;background:1%;background-color:white")
        self.minimize_button.setStyleSheet("border:1 solid white;background:1%;background-color:white")
        self.maximize_button.setStyleSheet("border:1 solid white;background:1%;background-color:white")

    def toggle(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()


class CursorPositions:
    TOP_LEFT = 0
    TOP_CENTER = 1
    TOP_RIGHT = 2

    MIDDLE_LEFT = 3
    MIDDLE_RIGHT = 4

    BOTTOM_LEFT = 5
    BOTTOM_CENTER = 6
    BOTTOM_RIGHT = 7

    DEFAULT = -1

    def __init__(self):
        self.actualPosition = self.DEFAULT


app = QApplication([])
window = FramelessResizableWindow()
window.show()
app.exec()
