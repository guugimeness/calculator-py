from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout)

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
        
    def addVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)
