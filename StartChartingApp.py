import sys
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot
from matplotlib import dates
import datetime as dt
import MainWindow
import pandas as pd


class StartQT4(QMainWindow):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.choose_file)

    @pyqtSlot()
    def choose_file(self):
        fd = QFileDialog(self)
        self.filename = fd.getOpenFileName()
        from os.path import isfile
        if isfile(self.filename[0]):
            raw_data = pd.read_csv(self.filename[0], delimiter=',', header=5)
            self.dm = DataManager(raw_data)


class DataManager():
    def __init__(self, data=None):
        self.raw_data = data
        self.add_plottable_date_col()

    def add_plottable_date_col(self):
        if ('Date (D/M/Y)' in self.raw_data.columns) & ('Time (H:M:S)' in self.raw_data.columns):
            date_str = self.raw_data['Date (D/M/Y)']
            time_str = self.raw_data['Time (H:M:S)']
            datetime_str = date_str + 'T' + time_str
            null_dates = datetime_str == '0/0/0T00:01:00'
            # Remove rows with null dates
            datetime_str = datetime_str[~null_dates]
            self.raw_data = self.raw_data[~null_dates]
            datetimes = pd.to_datetime(datetime_str, format='%d/%m/%YT%H:%M:%S')
            plottable_datetime = dates.date2num(datetimes)
            self.raw_data['Plottable_datetime'] = plottable_datetime
            print(self.raw_data['Plottable_datetime'].head(5))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())