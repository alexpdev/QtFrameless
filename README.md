# QtFrameless

## Overview

A custom frameless Qt QmainWindow.

## Features

- Frameless
- Custom Title Bar
- Resizeable
- Moveable
- Pluggable
- Extensible

## Examples

There are a number of examples below and provided in the examples directory:

`helloworld.py`
```
class MainWindow(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("HELLO WORLD!")
```



`texteditor.py`
```
class MainWindow(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Text Editor")
        self.textEdit = QTextEdit(parent=self)
        self.setCentralWidget(self.textEdit)
        self.setStyleSheet("QTextEdit {border: 1px solid black;}")
```
