from PySide6.QtWidgets import QApplication
from QtFrameless import FramelessWindow

class MainWindow(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("HELLO WORLD!")

if "main" in __name__:
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
