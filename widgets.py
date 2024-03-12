from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLayout, QLabel, QLineEdit,
                               QPushButton, QGridLayout)
from PySide6.QtCore import Qt, Slot
from variables import SMALL_FONT_SIZE, MEDIUM_FONT_SIZE, BIG_FONT_SIZE, INFO_MARGIN, TEXT_MARGIN, MINIMUM_WIDTH
from utils import isNumOrDot, isValidNumber, isEmpyt

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
    def __init__(self, display: Display, info: Info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '='],
        ]
         
        self.display = display
        self.info = info
        self._equation = ''
        self._leftNum = None
        self._operator = None
        self._rightNum = None
        self._makeGrid()
        
    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)
        
    def _makeGrid(self):
        for i, row in enumerate(self._gridMask):
            for j, button_text in enumerate(row):

                if button_text == '':
                    continue
                
                button = Button(button_text)
                
                if not isNumOrDot(button_text):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)
                
                if button_text == '0':
                    self.addWidget(button, i, j, 1, 2)
                else:
                    self.addWidget(button, i, j)

                slot = self._makeSlot(self._ButTextToDisplay, button)
                self._connectButtonClicked(button, slot)
                
    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)
        
    def _configSpecialButton(self, button):
        buttonText = button.text()
        
        if buttonText == 'C':
            self._connectButtonClicked(button, self._clear)
            
        if buttonText == '◀':
            self._connectButtonClicked(button, self.display.backspace)
            
        if buttonText in '+-*/^':
            self._connectButtonClicked(button, self._makeSlot(self._operatorClicked, button))
            
        if buttonText == '=':
            self._connectButtonClicked(button, self._makeOperation)
            
    def _makeSlot(self, func, *args, **kwargs):
        @Slot()
        def realSlot():
            func(*args, **kwargs)
        return realSlot
    
    def _ButTextToDisplay(self, button):
        buttonText = button.text()
        newValueDisplay = self.display.text() + buttonText 
        
        if not isValidNumber(newValueDisplay):
            return
        
        self.display.insert(buttonText)
        
    def _clear(self):
        self._equation = ''
        self._leftNum = None
        self._operator = None
        self._rightNum = None
        self.display.clear()
        self.info.clear()
        
    def _operatorClicked(self, button):
        buttonText = button.text()  # Operator
        displayText = self.display.text()  # Left Number
        self.display.clear()  # Clean display
        
        if isEmpyt(displayText) and self._leftNum is None:
            # Dialog message ??
            return
    
        if self._leftNum is None:
            self._leftNum = float(displayText)
        
        if buttonText == '^':
            self._operator = '**'
        else:
            self._operator = buttonText
            
        self.equation = f'{self._leftNum} {self._operator}'
         
    def _makeOperation(self):
        displayText = self.display.text()
        
        if isEmpyt(displayText) or self._leftNum is None:
            return
        
        self._rightNum = float(displayText)  
        self.equation = f'{self._leftNum} {self._operator} {self._rightNum}'
        
        error = False
        try:
            result = eval(self.equation)
            self.display.clear()
            self._leftNum = result
            self.info.setText(f'{self.equation} = {result}')
        except ZeroDivisionError:
            self.info.setText('Zero Division Error')
            error = True
        except OverflowError:
            self.info.setText('Overflow Error')
            error = True

        if error:
            self.display.clear()
            self._leftNum = None
        