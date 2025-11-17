import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from theme import APP_STYLE

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    w = MainWindow(); w.show()
    app.exec()

