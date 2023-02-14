from .qt_api import QPushButton, QApplication


class TitleBarButton(QPushButton):
    """Standard Buttons for closing and minimizing the window."""

    _action = ""

    def __init__(self, parent=None):
        """Construct the standard window control buttons."""
        super().__init__(parent=parent)
        self.setFixedHeight(20)
        self.setFixedWidth(20)
        self.setObjectName(f"TitleBarButton{self._action}")
        self.clicked.connect(self.window_action)

    def window_action(self):
        """Perform action for the specified button."""
        pass


class TitleBarCloseButton(TitleBarButton):
    """Standard Buttons for closing and minimizing the window."""

    _action = "Close"

    def window_action(self):
        """Perform action for the specified button."""
        self.window().destroy(True, True)
        QApplication.instance().exit()


class TitleBarMinButton(TitleBarButton):
    """Standard Buttons for closing and minimizing the window."""

    _action = "Min"

    def window_action(self):
        """Perform action for the specified button."""
        if self.window().isMinimized():
            self.window().showNormal()
        else:
            self.window().showMinimized()


class TitleBarMaxButton(TitleBarButton):
    """Standard Buttons for closing and minimizing the window."""

    _action = "Max"

    def window_action(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()
