from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.resize(500,500)

        # attributes
        self._resizing = False
        self._resizable = True
        self._margin = 4
        self._pressToMove = False
        self._vertExpandStart = False
        self._vertExpanded = False
        self._originY = 0
        self._originHeight = 0

        # Flags

        self.setMouseTracking(True)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint )
        self.setCursors()

    def setCursors(self):
        self._T, self._B, self._L, self._R = 1, 2, 3, 4
        self.cursors = {
            (self._T,): Qt.SizeVerCursor,
            (self._B,): Qt.SizeVerCursor,
            (self._L,): Qt.SizeHorCursor,
            (self._R,): Qt.SizeHorCursor,
            (self._T, self._R): Qt.SizeBDiagCursor,
            (self._T, self._L): Qt.SizeFDiagCursor,
            (self._B, self._L): Qt.SizeBDiagCursor,
            (self._B, self._R): Qt.SizeFDiagCursor,
        }

    def isResizable(self):
        return self._resizable

    def _cursorHoverShape(self, event):
        if self.isResizable():
            if self.isMaximized() or self.isFullScreen():
                return
            rect = self.rect()
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            rect.setX(x + self._margin)
            rect.setY(y + self._margin)
            rect.setWidth(w  - self._margin * 2)
            rect.setHeight(h - self._margin * 2)
            if rect.contains(event.position().toPoint()):
                self.cursor().setShape(Qt.CursorShape.ArrowCursor)
                return
            x2, y2 = event.position().x(), event.position().y()
            edges = [e for e,v in [
                    (self._T, abs(y2 - y) <= self._margin),
                    (self._B, abs(y2 - (self.height() + y)) <= self._margin),
                    (self._L, abs(x2 - x) <= self._margin),
                    (self._R, abs(x2 - (self.width() + x)) <= self._margin),
                    ] if v]
            self.cursor().setShape(self.cursors[tuple(edges)])
            self.direction = edges

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.isResizable():
                self._resize()
            else:
                if self._pressToMove:
                    self._move()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self._cursorHoverShape(event)
        return super().mouseMoveEvent(event)

    def enterEvent(self, event):
        self._cursorHoverShape(event)
        return super().enterEvent(event)

    def _resize(self):
        window = self.window().windowHandle()
        if self.cursor().shape() == Qt.SizeHorCursor:
            if self._L in self.direction:
                window.startSystemResize(Qt.LeftEdge)
            if self._R in self.direction:
                window.startSystemResize(Qt.RightEdge)
        elif self.cursor().shape() == Qt.SizeVerCursor:
            if self._T in self.direction:
                window.startSystemResize(Qt.TopEdge)
            elif self._B in self.direction:
                window.startSystemResize(Qt.BottomEdge)
        elif self.cursor().shape() == Qt.SizeBDiagCursor:
            if (self._T, self._R) == self.direction:
                window.startSystemResize(Qt.TopEdge | Qt.RightEdge)
            else:
                window.startSystemResize(Qt.BottomEdge | Qt.LeftEdge)
        elif self.cursor().shape() == Qt.SizeFDiagCursor:
            if (self._T, self._L) == self.direction:
                window.startSystemResize(Qt.TopEdge | Qt.LeftEdge)
            else:
                window.startSystemResize(Qt.BottomEdge | Qt.RightEdge)

    def _move(self):
        window = self.window().windowHandle()
        window.startSystemMove()


class BaseWidget(QWidget):
    changedToDark = Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _initVal(self):
        self._pressToMove = True
        self._resizable = True
        self._border_width = 5

        self.__detect_theme_flag = True

    def _initUi(self, hint=None):
        if hint is None:
            hint = ['min', 'max', 'close']
        # self._windowEffect = WindowsEffectHelper()

        # remove window border
        # seems kinda pointless(though if you get rid of code below frame will still be seen), but if you don't add this, cursor won't properly work
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # add DWM shadow and window animation
        self._windowEffect.setBasicEffect(self.winId(), hint)

        self.windowHandle().screenChanged.connect(self._onScreenChanged)

        self._titleBar = TitleBar(self, hint)

        self.__setCurrentWindowsTheme()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self._pressToMove:
                self._move()
        return super().mousePressEvent(e)

    def _move(self):
        window = self.window().windowHandle()
        window.startSystemMove()

    def isPressToMove(self) -> bool:
        return self._pressToMove

    def setPressToMove(self, f: bool):
        self._pressToMove = f
        self._titleBar.setPressToMove(f)

    # set Windows theme by referring registry key
    # def __setCurrentWindowsTheme(self):
    #     try:
    #         root = ConnectRegistry(None, HKEY_CURRENT_USER)
    #         root_key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize', 0, KEY_READ)
    #         lightThemeValue, regtype = QueryValueEx(root_key, 'AppsUseLightTheme')
    #         if lightThemeValue == 0 or lightThemeValue == 1:
    #             dark_f = lightThemeValue == 0
    #             if dark_f:
    #                 pass
    #                 # QGuiApplication.setPalette(QPalette(QColor(0, 0, 0)))
    #             else:
    #                 pass
    #                 # QGuiApplication.setPalette(QPalette(QColor(255, 255, 255)))
    #             self._windowEffect.setDarkTheme(self.winId(), dark_f)
    #             self.changedToDark.emit(dark_f)
    #         else:
    #             raise Exception(f'Unknown value "{lightThemeValue}".')
    #     except FileNotFoundError:
    #         print('AppsUseLightTheme not found.')
    #     except Exception as e:
    #         print(e)

    def setDarkTheme(self, f: bool):
        self._windowEffect.setDarkTheme(self.winId(), f)

    def isDetectingThemeAllowed(self):
        return self.__detect_theme_flag

    def allowDetectingTheme(self, f: bool):
        self.__detect_theme_flag = f

    def isResizable(self) -> bool:
        return self._resizable

    def setResizable(self, f: bool):
        self._resizable = f
        self._titleBar.setBaseWindowResizable(f)

    # def nativeEvent(self, e, message):
    #     msg = MSG.from_address(message.__int__())
    #     # check if it is message from Windows OS
    #     if msg.hWnd:
    #         # update cursor shape to resize/resize feature
    #         # get WM_NCHITTEST message
    #         # more info - https://learn.microsoft.com/ko-kr/windows/win32/inputdev/wm-nchittest
    #         if msg.message == win32con.WM_NCHITTEST:
    #             if self._resizable:
    #                 pos = QCursor.pos()
    #                 x = pos.x() - self.x()
    #                 y = pos.y() - self.y()

    #                 w, h = self.width(), self.height()

    #                 left = x < self._border_width
    #                 top = y < self._border_width
    #                 right = x > w - self._border_width
    #                 bottom = y > h - self._border_width

    #                 # to support snap layouts
    #                 # more info - https://learn.microsoft.com/en-us/windows/apps/desktop/modernize/apply-snap-layout-menu
    #                 # if win32gui.PtInRect((10, 10, 100, 100), (x, y)):
    #                 #     return True, win32con.HTMAXBUTTON

    #                 if top and left:
    #                     return True, win32con.HTTOPLEFT
    #                 elif top and right:
    #                     return True, win32con.HTTOPRIGHT
    #                 elif bottom and left:
    #                     return True, win32con.HTBOTTOMLEFT
    #                 elif bottom and right:
    #                     return True, win32con.HTBOTTOMRIGHT
    #                 elif left:
    #                     return True, win32con.HTLEFT
    #                 elif top:
    #                     return True, win32con.HTTOP
    #                 elif right:
    #                     return True, win32con.HTRIGHT
    #                 elif bottom:
    #                     return True, win32con.HTBOTTOM

    #         # maximize/minimize/full screen feature
    #         # get WM_NCCALCSIZE message
    #         # more info - https://learn.microsoft.com/ko-kr/windows/win32/winmsg/wm-nccalcsize
    #         elif msg.message == win32con.WM_NCCALCSIZE:
    #             if msg.wParam:
    #                 rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
    #             else:
    #                 rect = cast(msg.lParam, LPRECT).contents

    #             max_f = win32utils.isMaximized(msg.hWnd)
    #             full_f = win32utils.isFullScreen(msg.hWnd)

    #             # adjust the size of window
    #             if max_f and not full_f:
    #                 thickness = win32utils.getResizeBorderThickness(msg.hWnd)
    #                 rect.top += thickness
    #                 rect.left += thickness
    #                 rect.right -= thickness
    #                 rect.bottom -= thickness

    #             # for auto-hide taskbar
    #             if (max_f or full_f) and win32utils.Taskbar.isAutoHide():
    #                 position = win32utils.Taskbar.getPosition(msg.hWnd)
    #                 if position == win32utils.Taskbar.LEFT:
    #                     rect.top += win32utils.Taskbar.AUTO_HIDE_THICKNESS
    #                 elif position == win32utils.Taskbar.BOTTOM:
    #                     rect.bottom -= win32utils.Taskbar.AUTO_HIDE_THICKNESS
    #                 elif position == win32utils.Taskbar.LEFT:
    #                     rect.left += win32utils.Taskbar.AUTO_HIDE_THICKNESS
    #                 elif position == win32utils.Taskbar.RIGHT:
    #                     rect.right -= win32utils.Taskbar.AUTO_HIDE_THICKNESS

    #             result = 0 if not msg.wParam else win32con.WVR_REDRAW
    #             return True, result
    #         elif msg.message == win32con.WM_SETTINGCHANGE:
    #             if self.__detect_theme_flag:
    #                 self.__setCurrentWindowsTheme()
    #     return super().nativeEvent(e, message)

    # def _onScreenChanged(self):
    #     hWnd = int(self.windowHandle().winId())
    #     win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
    #                           win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)

    def setWindowIcon(self, filename):
        icon = QIcon()
        icon.addFile(filename)
        self._titleBar.setIcon(icon)
        super().setWindowIcon(icon)

    def setWindowTitle(self, title: str) -> None:
        super().setWindowTitle(title)
        self._titleBar.setTitle(title)

    def setTitleBarVisible(self, f):
        self._titleBar.setVisible(f)
        if self.isPressToMove() or self._titleBar.isPressToMove():
            self._titleBar.setPressToMove(f)
            self.setPressToMove(not f)

    def setTitleBarHint(self, hint: list):
        self._titleBar.setTitleBarHint(hint)

    def getTitleBar(self):
        return self._titleBar

    def setFixedSize(self, width, height):
        super().setFixedSize(width, height)
        self.setResizable(False)


class TitleBar(QWidget):
    def __init__(self, base_widget=None, hint=None):
        super().__init__(base_widget)
        self.__initVal(hint)
        self.__initUi()

    def __initVal(self, hint):
        self._pressToMove = True
        # for make this to recognize that the base window is able to resize or not
        # this is indeed really weird way to program so i'll figure out other way to handle it soon enough
        self.__baseWindowResizable = True

        # variables for icon
        self.__icon = QIcon()
        self.__iconLbl = QLabel()

        # variable for title
        self.__titleLbl = QLabel()

        # buttons
        self.__fullScreenBtn = QPushButton('▣')
        self.__minBtn = QPushButton('🗕')
        self.__maxBtn = QPushButton('🗖')
        self.__closeBtn = QPushButton('🗙')

        self.__fullScreenBtn.setCheckable(True)

        self.__btn_dict = {
            'full_screen': self.__fullScreenBtn,
            'min': self.__minBtn,
            'max': self.__maxBtn,
            'close': self.__closeBtn
        }

        self.__fullScreenBtn.clicked.connect(self.__fullScreen)
        self.__minBtn.clicked.connect(self.window().showMinimized)
        self.__maxBtn.clicked.connect(self.__maximize)
        self.__closeBtn.clicked.connect(self.window().close)

        self.__hint = hint

    def __initUi(self):
        lay = QHBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.setAlignment(Qt.AlignRight)

        lay.addWidget(self.__iconLbl)
        lay.addWidget(self.__titleLbl)
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))

        for k in self.__hint:
            if k in self.__btn_dict:
                lay.addWidget(self.__btn_dict[k])

        self._styleInit()

        self.window().installEventFilter(self)

        self.setLayout(lay)

    def _styleInit(self):
        # top right buttons' height set to 36 by default
        self.__btnsStyleInit(h=36)

        label_style = 'QLabel { margin: 4 }'

        self.__iconLbl.setStyleSheet(label_style)
        self.__titleLbl.setStyleSheet(label_style)

    # This function is separated for the reasons: to adjust height
    def __btnsStyleInit(self, h):
        for btn in self.__btn_dict.values():
            btn.setStyleSheet(f'''
                              QPushButton {{
                              background-color: transparent;
                              border: 0;
                              width: 50;
                              height: {h};
                              }}
                              QPushButton:hover {{
                              background-color: #ddd;
                              }}
                              QPushButton:pressed {{
                              background-color: #aaa;
                              }}
                              QPushButton:checked {{
                              background-color: #ddd;
                              }}
                              ''')

        self.__closeBtn.setStyleSheet(f'''
                                      QPushButton {{
                                      background-color: transparent;
                                      border: 0;
                                      width: 50;
                                      height: {h};
                                      }}
                                      QPushButton:hover {{
                                      background-color: #f00;
                                      color: white;
                                      }}
                                      QPushButton:pressed {{
                                      background-color: #f44;
                                      color: white;
                                      }}
                                      ''')

    def __maximize(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def __fullScreen(self):
        if self.window().isFullScreen():
            self.window().showNormal()
        else:
            self.window().showFullScreen()

    def mouseDoubleClickEvent(self, event):
        if self.__baseWindowResizable:
            if event.button() != Qt.LeftButton:
                return
            self.__maximize()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self._pressToMove:
                self._move()
        return super().mousePressEvent(e)

    def _move(self):
        window = self.window().windowHandle()
        window.startSystemMove()

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == 105:
                self.__fullScreenBtn.setChecked(self.window().isFullScreen())
                self.__maxBtn.setChecked(self.window().isMaximized())
                if self.window().isMaximized():
                    self.__maxBtn.setText('🗗')
                else:
                    self.__maxBtn.setText('🗖')
                if self.window().isFullScreen():
                    self.hide()
                else:
                    self.show()

        return super().eventFilter(obj, e)

    def setIcon(self, icon):
        self.__icon = icon
        # 18, 18 by default
        self.setIconSize(18, 18)

    def setTitle(self, title):
        self.__titleLbl.setText(title)

    def setPressToMove(self, f: bool):
        self._pressToMove = f

    def isPressToMove(self) -> bool:
        return self._pressToMove

    def setTitleBarFont(self, font: QFont):
        self.__titleLbl.setFont(font)
        self.__btnsStyleInit(h=font.pointSize()*2)

    def setIconSize(self, w, h):
        self.__iconLbl.setPixmap(self.__icon.pixmap(w, h))
        self.__btnsStyleInit(h=h*2)

    def setTitleBarHint(self, hint: list):
        print(hint)

    def getIcon(self) -> QLabel:
        return self.__iconLbl

    def getTitle(self) -> QLabel:
        return self.__titleLbl

    # this is indeed really weird way to program so i'll figure out other way to handle it soon enough
    def setBaseWindowResizable(self, f: bool):
        self.__baseWindowResizable = f
        self.__maxBtn.setVisible(f)



if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
