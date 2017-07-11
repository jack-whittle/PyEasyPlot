import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates
import datetime as dt
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLabel, QComboBox, QFormLayout, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import sys


def plot_simple_2d(x_col_name, y_col_name, df):
    x_data = df[x_col_name]
    y_data = df[y_col_name]
    plt.xlabel(x_col_name)
    plt.ylabel(y_col_name)
    plt.plot(x_data, y_data)
    plt.show()


def format_date_for_plotting(date, time):
    date_str = date + 'T' + time
    null_dates = date_str == '0/0/0T00:01:00'
    datetimes = date_str[~null_dates]
    datetimes = dt.datetime.strptime(date_str, '%d/%m/%YT%H:%M:%S')
    return dates.date2num(datetimes)


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.df = pd.read_csv(r'resources/Pegasus Data (05-05-17 15h53m23s) - Waregem.csv', delimiter=',', header=5)
        data_names = self.df.columns.tolist()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.form_layout = QFormLayout()
        x_data_label = QLabel('X Data')
        y_data_label = QLabel('Y Data')
        x_options = QComboBox()
        x_options.addItems(data_names)

        self.form_layout.addRow(x_data_label, x_options)

        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(self.form_layout)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        x_data = self.df['Temperature (degC)']
        y_data = self.df['Humidity (%)']
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x_data, y_data)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

# filepath = r'resources/Pegasus Data (05-05-17 15h53m23s) - Waregem.csv'
#
# data_df = pd.read_csv(filepath, delimiter=',', header=5)
#
# plot_simple_2d('Temperature (degC)', 'Humidity (%)', data_df)
# plot_simple_2d('Battery Voltage', 'Temperature (degC)', data_df)
# date_col = format_date(data_df['Date (D/M/Y)'], data_df['Time (H:M:S)'])
# print(type(date_col))
# print()
