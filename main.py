import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from widgets import MainWindow, Info, Display, Button, ButtonsGrid
from styles import setupTheme
from variables import WINDOW_ICON_PATH

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # Theme
    setupTheme()
    
    # Icon
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)
        
    # Info
    info = Info()
    window.addWidgetToVLayout(info)
    
    # Display
    display = Display()
    #display.setPlaceholderText('Digite a conta')
    window.addWidgetToVLayout(display)
    
    # Grid
    buttonsGrid = ButtonsGrid(display, info)
    window.addLayoutToVLayout(buttonsGrid)

    window.adjustFixedSize()
    window.show()
    app.exec()