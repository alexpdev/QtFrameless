from PySide6.QtWidgets import QPushButton, QApplication

class TopBarButton(QPushButton):
    def __init__(self, prop, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(20)
        self.setFixedWidth(20)
        self.setProperty(prop, "true")
        self.clicked.connect(self.window_action)

    def window_action(self):
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
