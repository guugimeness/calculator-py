from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLayout, QLabel, QLineEdit,
                               QPushButton, QGridLayout, QMessageBox)
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QKeyEvent
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
        
        # Info
        info = Info()
        self.addWidgetToVLayout(info)
        
        # Display
        display = Display()
        self.addWidgetToVLayout(display)
        
        # Grid
        buttonsGrid = ButtonsGrid(display, info, self)
        self.addLayoutToVLayout(buttonsGrid)

    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
        
    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)
        
    def addLayoutToVLayout(self, layout: QLayout):
        self.vLayout.addLayout(layout)
        
    def makeMsgBox(self):
        return QMessageBox(self)

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
    
    # Signals
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)
    
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        text = event.text().strip()
        KEYS = Qt.Key
        
        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete, KEYS.Key_D]
        isEsc = key in [KEYS.Key_Escape, KEYS.Key_C]
        isOperator = key in [KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk, KEYS.Key_P]
        
        if isEnter or text == '=':
            self.eqPressed.emit()
            return event.ignore()
        
        if isDelete:
            self.delPressed.emit()
            return event.ignore()

        if isEsc:
            self.clearPressed.emit()
            return event.ignore()
        
        if isOperator:
            if text.lower() == 'p':
                text = '^'
            self.operatorPressed.emit(text)
            return event.ignore()
        
        if isEmpyt(text):
            return event.ignore()
        
        if isNumOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
        
    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)
        
class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, info: Info, window: MainWindow, *args, **kwargs):
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
        self.window = window
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
        
        # Conecting keyboard signals
        self.display.eqPressed.connect(self._makeOperation)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._operatorRequested)
        
        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):

                if buttonText == '':
                    continue
                
                button = Button(buttonText)
                
                if not isNumOrDot(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._connectSpecialButton(button)
                
                if buttonText == '0':
                    self.addWidget(button, i, j, 1, 2)
                else:
                    self.addWidget(button, i, j)

                slot = self._makeSlot(self._insertToDisplay, buttonText)
                self._connectButtonClicked(button, slot)
            
    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    # Special buttons aren't a number or dot    
    def _connectSpecialButton(self, button):
        buttonText = button.text()
        
        if buttonText == 'C':
            self._connectButtonClicked(button, self._clear)
            
        if buttonText == '◀':
            self._connectButtonClicked(button, self._backspace)
            
        if buttonText in '+-*/^':
            self._connectButtonClicked(button, self._makeSlot(self._operatorRequested, buttonText))
            
        if buttonText == '=':
            self._connectButtonClicked(button, self._makeOperation)
    
    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        def realSlot():
            func(*args, **kwargs)
        return realSlot
    
    @Slot()
    def _insertToDisplay(self, text: str):
        newValueDisplay = self.display.text() + text
        
        if not isValidNumber(newValueDisplay):
            return
        
        self.display.insert(text)
        self.display.setFocus()
        
    @Slot()
    def _clear(self):
        self._equation = ''
        self._leftNum = None
        self._operator = None
        self._rightNum = None
        self.display.clear()
        self.info.clear()
        self.display.setFocus()
    
    @Slot()
    def _operatorRequested(self, text: str):
        displayText = self.display.text()  # Left Number
        self.display.clear()  # Clean display
        
        if text == '-':
            if (isEmpyt(displayText) and self._leftNum is None) or (self._operator is not None):
                self.display.insert(text)
                return
                
        if isEmpyt(displayText) and self._leftNum is None:
            self._showError('Você não digitou nada!')
            return
    
        if self._leftNum is None:
            self._leftNum = float(displayText)

        if text == '^':
            self._operator = '**'
        else:
            self._operator = text
            
        self.equation = f'({self._leftNum}) {self._operator}'
        self.display.setFocus()
        
    @Slot()
    def _makeOperation(self):
        displayText = self.display.text()
        
        if (isEmpyt(displayText)) or (self._leftNum is None) or (self._operator is None):
            self._showError('Conta incompleta.')
            return
        
        self._rightNum = float(displayText)
        self.equation = f'({self._leftNum}) {self._operator} ({self._rightNum})'
        
        error = False
        try:
            result = eval(self.equation)
            self.display.clear()
            self._leftNum = result
            self._operator = None
            self.info.setText(f'{self.equation} = ({result})')
        except ZeroDivisionError:
            self._showError('A divisão por zero não é definida.')
            error = True
        except OverflowError:
            self._showError('Essa conta não pode ser realizada.')
            error = True

        if error:
            self._clear()
            
        self.display.setFocus()
            
    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()
            
    def _showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()
        