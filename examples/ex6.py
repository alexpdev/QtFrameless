import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

info = """
Resizable = False
Draggable = False
Maximizable = False
Minimizable = False
Closable = True
RoundedCorners = True
Styled = True
"""

class Dialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setObjectName('Custom_Dialog')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(Stylesheet)

        self.initUi()

    def initUi(self):
        # Important: this widget is used as background and rounded corners.
        self.widget = QWidget(self)
        self.widget.setObjectName('Custom_Widget')
        layout = QVBoxLayout(self)
        layout.addWidget(self.widget)

        # Add user interface to widget
        layout = QGridLayout(self.widget)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 0)
        layout.addWidget(QPushButton(
            'r', self, clicked=self.accept, objectName='closeButton'), 0, 1)
        layout.addWidget(QLabel("<h2 style='color:blue;'>Hello, world!</h2>"), 2, 0, 5, 2, alignment=Qt.AlignCenter)

    def sizeHint(self):
        return QSize(300, 380)


Stylesheet = """
#Custom_Widget {
    background: #002025;
    border-radius: 20px;
    opacity: 100;
    border: 2px solid #ff2025;
}
#closeButton {
    min-width: 36px;
    min-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#closeButton:hover {
    color: #ccc;
    background: red;
}
"""


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Dialog()
    w.exec_()
    QTimer.singleShot(200, app.quit)
    sys.exit(app.exec())
