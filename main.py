import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from widgets import MainWindow
from styles import setupTheme
from variables import WINDOW_ICON_PATH

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Window config
    window = MainWindow()
    window.adjustFixedSize()
    
    # Theme
    setupTheme()
    
    # Icon
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)
    
    window.show()
    app.exec()