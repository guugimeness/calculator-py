from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout)

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Title
        self.setWindowTitle('Calculator')
        
        # Central Widget
        self.central_w = QWidget()
        self.setCentralWidget(self.central_w)
        
        # Layout
        self.v_layout = QVBoxLayout()
        self.central_w.setLayout(self.v_layout)

    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
        
    def addWidgetVLayout(self, widget: QWidget):
        self.v_layout.addWidget(widget)
        self.adjustFixedSize()
