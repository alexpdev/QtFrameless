from PySide6.QtWidgets import QPushButton, QApplication

class TitleBarButton(QPushButton):
    """Standard Buttons for closing and minimizing the window."""

    def __init__(self, prop, parent=None):
        """Construct the standard window control buttons."""
        super().__init__(parent=parent)
        self.setFixedHeight(20)
        self.setFixedWidth(20)
        self.setProperty(prop, "true")
        self.clicked.connect(self.window_action)

    def window_action(self):
        """Perform action for the specified button."""
        if self.property("close"):
            self.window().destroy(True, True)
            QApplication.instance().exit()
        if self.property("min"):
            if self.window().isMinimized():
                self.window().showNormal()
            else:
                self.window().showMinimized()
        if self.property("max"):
            if self.window().isMaximized():
                self.window().showNormal()
            else:
                self.window().showMaximized()
