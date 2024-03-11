from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLayout, QLabel, QLineEdit,
                               QPushButton, QGridLayout)
from PySide6.QtCore import Qt, Slot
from variables import SMALL_FONT_SIZE, MEDIUM_FONT_SIZE, BIG_FONT_SIZE, INFO_MARGIN, TEXT_MARGIN, MINIMUM_WIDTH
from utils import isNumOrDot

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Title
        self.setWindowTitle('Calculator')
        
        # Central Widget
        self.cWidget = QWidget()
        self.setCentralWidget(self.cWidget)
        
        # Layout
        self.vLayout = QVBoxLayout()
        self.cWidget.setLayout(self.vLayout)

    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
        
    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)
        
    def addLayoutToVLayout(self, layout: QLayout):
        self.vLayout.addLayout(layout)

class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyle()
        
    def configStyle(self):
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setMargin(INFO_MARGIN)

class Display(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
        
    def configStyle(self):
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(TEXT_MARGIN, TEXT_MARGIN, TEXT_MARGIN, TEXT_MARGIN)
        self.setMinimumSize(MINIMUM_WIDTH, BIG_FONT_SIZE * 1.5)

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
        
    def configStyle(self):
        # Font
        #self.setStyleSheet(f'font-size: {MEDIUM_FONT_SIZE}px;')
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        
        # Size
        self.setMinimumSize(75, 75)
        
class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '='],
        ]
        
        self.display = display
        
    def _makeGrid(self):
        for i, row in enumerate(self._gridMask):
            for j, button_text in enumerate(row):

                if button_text == '':
                    continue
                
                button = Button(button_text)
                
                if not isNumOrDot(button_text):
                    button.setProperty('cssClass', 'specialButton')
                
                if button_text == '0':
                    self.addWidget(button, i, j, 1, 2)
                else:
                    self.addWidget(button, i, j)

                buttonSlot = self._ButtonDisplaySlot(self._ButTextToDisplay, button)
                button.clicked.connect(buttonSlot)
                
    def _ButtonDisplaySlot(self, func, *args, **kwargs):
        @Slot()
        def realSlot():
            func(*args, **kwargs)
        return realSlot
    
    def _ButTextToDisplay(self, button):
        self.display.insert(button.text())
            
        