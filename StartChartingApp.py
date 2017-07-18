import sys
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot
import matplotlib.pyplot as plt
import MainWindow
import pandas as pd
from pubsub import pub


class StartQT4(QMainWindow):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = MainWindow.Ui_MainWindow()
        # attributes initialised in subsequent methods
        self.dm = None

        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.choose_file)
        self.ui.comboBox.currentIndexChanged.connect(self.set_x_data)

    @pyqtSlot()
    def choose_file(self):
        fd = QFileDialog(self)
        filename = fd.getOpenFileName()
        from os.path import isfile
        if isfile(filename[0]):
            raw_data = pd.read_csv(filename[0], delimiter=',', header=5)
            self.dm = DataManager(raw_data)
            self.ui.comboBox.addItems(self.dm.x_columns)
            self.ui.comboBox_2.addItems(self.dm.y_columns)

    @pyqtSlot()
    def set_x_data(self):
        self.dm.plot_data['x_name'] = self.ui.comboBox.currentText()
        pub.sendMessage('UpdateX', update=self.dm.plot_data['x_name'])


class DataManager():
    def __init__(self, data=None):
        self.data = data
        self.x_columns = None
        self.y_columns = None
        self.plot_data = None
        if self.data is not None:
            self.inititialise_data()
        # self.data.plot(subplots=True, figsize=(6, 6))
        # plt.legend(loc='best')

    def inititialise_data(self):
        if ('Date (D/M/Y)' in self.data.columns) & ('Time (H:M:S)' in self.data.columns):
            # Filter out null dates
            null_dates = self.data['Date (D/M/Y)'] == '0/0/0'
            self.data = self.data[~null_dates]

            # Concatenate date and time into single column
            datetime_str = self.data['Date (D/M/Y)'] + 'T' + self.data['Time (H:M:S)']
            date_times = pd.to_datetime(datetime_str, format='%d/%m/%YT%H:%M:%S')
            self.data['date_time'] = pd.Series(date_times)

            self.data.index = self.data['date_time']

            self.x_columns = [self.data.index.name] + self.data.columns.tolist()
            self.y_columns = self.data.columns.tolist()
            self.plot_data = dict()
            self.plot_data['x_name'] = self.data.index.name
            self.plot_data['x_data'] = self.data.index
            self.plot_data['y_name'] = self.y_columns[1]
            self.plot_data['y_data'] = self.data[self.plot_data['y_name']]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())