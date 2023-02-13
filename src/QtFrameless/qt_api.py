import sys

if "PyQt6" in sys.modules:
    from PyQt6.QtWidgets import *
    from PyQt6.QtGui import *
    from PyQt6.QtCore import *
elif "PyQt5" in sys.modules:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
else:
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from PySide6.QtCore import *


QMainWindow = QMainWindow
QWidget = QWidget
QPushButton = QPushButton
QLabel = QLabel
QApplication = QApplication
QVBoxLayout = QVBoxLayout
Qt = Qt
QPixmap = QPixmap
QHBoxLayout = QHBoxLayout
QSizePolicy = QSizePolicy
try:
    Signal = Signal
except:
    Signal = pyqtSignal
QObject = QObject
QMouseEvent = QMouseEvent
QEvent = QEvent
