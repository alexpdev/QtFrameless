from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from QtFrameless import FramelessWindow

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(45,45)

class Window(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.central = QWidget(self)
        self.layout = QVBoxLayout(self.central)
        self.setCentralWidget(self.central)
        self.display = QLCDNumber(8, parent=self)
        self.display.setFixedHeight(65)
        self.layout.addWidget(self.display)
        self.grid = QGridLayout()
        self.last = None
        self.buffer = "0"
        self.func = None
        self.history = []
        self.layout.addLayout(self.grid)
        self.add_buttons()
        self.connect_slots()
        self.setFixedWidth(240)
        self.setFixedHeight(410)
        self.display.setSegmentStyle(self.display.segmentStyle().Outline)
        self.setStyleSheet(
            """
            QPushButton {
                margin: 2px;
                background-color: #233;
                color: #FFF;
            }
            QLCDNumber {
                font-size: 15pt;
                background-color: #000;
                color: #FFF;
            }
            """
        )

    def add_buttons(self):
        self.one = Button("1", parent=self)
        self.two = Button("2", parent=self)
        self.three = Button("3", parent=self)
        self.four = Button("4", parent=self)
        self.five = Button("5", parent=self)
        self.six = Button("6", parent=self)
        self.seven = Button("7", parent=self)
        self.eight = Button("8", parent=self)
        self.nine = Button("9", parent=self)
        self.zero = Button("0", parent=self)
        self.plus = Button("+", parent=self)
        self.mult = Button("*", parent=self)
        self.div = Button("/", parent=self)
        self.minus = Button("-", parent=self)
        self.decimal = Button(".", parent=self)
        self.square = Button("x*x", parent=self)
        self.sqrt = Button("sqrt", parent=self)
        self.log = Button("log", parent=self)
        self.ln = Button("ln", parent=self)
        self.abs = Button("|x|", parent=self)
        self.pi = Button("pi", parent=self)
        self.clear = Button("C", parent=self)
        self.back = Button("<-",parent=self)
        self.eq = Button("=", parent=self)
        self.layout_buttons()

    def equals(self):
        value = self.func(float(self.buffer))
        self.display.display(value)

    def oper(self, value):
        if not self.last:
            self.last = self.buffer
            self.buffer = "0"
        if value == "+":
            self.func = lambda x: x + self.last
        elif value == "-":
            self.func = lambda x: x - self.last
        elif value == "*":
            self.func = lambda x: x * self.last
        elif value == "/":
            self.func = lambda x: x / self.last
        elif value == "|x|":
            self.diplay.display(abs(float(self.buffer)))
            self.last = str(abs(float(self.buffer)))
        elif value == "sq":
            self.display.display(float(self.buffer)**2)
            self.last = str(float(self.buffer)**2)

    def number(self, value):
        if not self.func:
            if self.buffer == "0":
                self.buffer = str(value)
            else:
                self.buffer += str(value)
        self.display.display(int(self.buffer))

    def connect_slots(self):
        self.plus.clicked.connect(lambda: self.oper("+"))
        self.mult.clicked.connect(lambda: self.oper("*"))
        self.div.clicked.connect(lambda: self.oper("/"))
        self.minus.clicked.connect(lambda: self.oper("-"))
        self.square.clicked.connect(lambda: self.oper("sq"))
        self.sqrt.clicked.connect(lambda: self.oper("sqrt"))
        self.log.clicked.connect(lambda: self.oper("log"))
        self.ln.clicked.connect(lambda: self.oper("ln"))
        self.abs.clicked.connect(lambda: self.oper("|x|"))
        self.pi.clicked.connect(lambda: self.oper("pi"))
        self.eq.clicked.connect(self.equals)
        self.one.clicked.connect(lambda: self.number(1))
        self.two.clicked.connect(lambda: self.number(2))
        self.three.clicked.connect(lambda: self.number(3))
        self.four.clicked.connect(lambda: self.number(4))
        self.five.clicked.connect(lambda: self.number(5))
        self.six.clicked.connect(lambda: self.number(6))
        self.seven.clicked.connect(lambda: self.number(7))
        self.eight.clicked.connect(lambda: self.number(8))
        self.nine.clicked.connect(lambda: self.number(9))
        self.zero.clicked.connect(lambda: self.number(0))

    def layout_buttons(self):
        self.grid.addWidget(self.pi,0,0,1,1)
        self.grid.addWidget(self.abs,0,1,1,1)
        self.grid.addWidget(self.clear,0,2,1,1)
        self.grid.addWidget(self.back,0,3,1,1)
        self.grid.addWidget(self.square,1,0,1,1)
        self.grid.addWidget(self.sqrt,1,1,1,1)
        self.grid.addWidget(self.log,1,2,1,1)
        self.grid.addWidget(self.ln,1,3,1,1)
        self.grid.addWidget(self.seven,2,0,1,1)
        self.grid.addWidget(self.eight,2,1,1,1)
        self.grid.addWidget(self.nine,2,2,1,1)
        self.grid.addWidget(self.div,2,3,1,1)
        self.grid.addWidget(self.four,3,0,1,1)
        self.grid.addWidget(self.five,3,1,1,1)
        self.grid.addWidget(self.six,3,2,1,1)
        self.grid.addWidget(self.mult,3,3,1,1)
        self.grid.addWidget(self.one,4,0,1,1)
        self.grid.addWidget(self.two,4,1,1,1)
        self.grid.addWidget(self.three,4,2,1,1)
        self.grid.addWidget(self.minus,4,3,1,1)
        self.grid.addWidget(self.decimal,5,0,1,1)
        self.grid.addWidget(self.zero,5,1,1,1)
        self.grid.addWidget(self.plus,5,2,1,1)
        self.grid.addWidget(self.eq,5,3,1,1)

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
