import sys
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication
import MainWindow


class StartQT4(QMainWindow):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())