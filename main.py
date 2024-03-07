import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from styles import setupTheme
from main_window import MainWindow
from display import Display
from variables import WINDOW_ICON_PATH
from info import Info

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
    info = Info('20.0 ^ 2 = 400.0')
    window.addVLayout(info)
    
    # Display
    display = Display()
    #display.setPlaceholderText('Digite a conta')
    window.addVLayout(display)

    window.adjustFixedSize()
    window.show()
    app.exec()