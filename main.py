
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

from MainWindow import MainWindow

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
