from PySide6.QtWidgets import QApplication, QTextEdit
from QtFrameless import FramelessWindow

class MainWindow(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Text Editor")
        self.textEdit = QTextEdit(parent=self)
        self.setCentralWidget(self.textEdit)
        self.setStyleSheet("QTextEdit {border: 1px solid black;}")

if "main" in __name__:
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
