import sys
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot
import MainWindow
import pandas as pd
import numpy as np
from pydispatch import dispatcher
import os


class StartPegasusViewer(QMainWindow):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.showMaximized()
        self.ui = MainWindow.Ui_MainWindow()
        # attributes initialised in subsequent methods
        self.dm = None

        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.choose_file)
        self.ui.comboBox.currentIndexChanged.connect(self.x_changed)
        self.ui.comboBox_2.currentIndexChanged.connect(self.y_changed)
        self.ui.comboBox_session.currentIndexChanged.connect(self.session_changed)
        self.ui.pushButton.clicked.connect(self.apply_btn_press)
        self.ui.pushButton_export.clicked.connect(self.export_btn_press)
        self.ui.pushButton_smooth.clicked.connect(self.apply_moving_avg)

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
            self.ui.comboBox_session.addItems([str(x) for x in self.dm.get_sorted_session_keys()])
            dispatcher.send('UpdateXCombo', update=self.dm.x_columns[0])

    def apply_btn_press(self):
        start_time = self.ui.timeEdit.time().toPyTime()
        end_time = self.ui.timeEdit_2.time().toPyTime()
        self.dm.apply_time_filter(start_time, end_time)
        dispatcher.send("UpdatePlot", plot_params=self.dm.plot_data)

    def export_btn_press(self):
        fd = QFileDialog(self)
        export_dir = str(fd.getExistingDirectory(self, "Select Export Directory"))
        export_dir = os.path.dirname(export_dir + os.sep + str(self.dm.current_session_key) + os.sep)
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        export_vars = ['Battery Voltage', 'Temperature (degC)', 'Humidity (%)', 'Pressure (hPa)']
        for export_var in export_vars:
            self.dm.update_y_plot_data(export_var)
            dispatcher.send("ExportPlot", plot_params=self.dm.plot_data, export_dir=export_dir)

    def apply_moving_avg(self):
        self.dm.apply_moving_avg()
        dispatcher.send("UpdatePlot", plot_params=self.dm.plot_data)

    @pyqtSlot()
    def x_changed(self):
        new_value = self.ui.comboBox.currentText()
        self.dm.update_x_plot_data(new_value)
        dispatcher.send("UpdatePlot", plot_params=self.dm.plot_data)

    def y_changed(self):
        new_value = self.ui.comboBox_2.currentText()
        self.dm.update_y_plot_data(new_value)
        dispatcher.send("UpdatePlot", plot_params=self.dm.plot_data)

    def session_changed(self):
        new_session_key = pd.to_datetime(self.ui.comboBox_session.currentText(), format='%Y/%m/%d %H:%M:%S')
        self.dm.update_session_plot_data(new_session_key)
        dispatcher.send("UpdatePlot", plot_params=self.dm.plot_data)
        dispatcher.send("UpdateTimeFields", s_time=self.dm.cur_start_time, e_time=self.dm.cur_end_time)


class DataManager():
    def __init__(self, data=None):
        self.data = data
        self.x_columns = None
        self.y_columns = None
        self.plot_data = None
        self.current_session_key = None
        self.cur_start_time = None
        self.cur_end_time = None
        self.cur_plot_df = None
        self.sessions = dict()

        if self.data is not None:
            self.inititialise_data()

    def inititialise_data(self):
        if ('Date (D/M/Y)' in self.data.columns) & ('Time (H:M:S)' in self.data.columns):
            # Filter out null dates
            null_dates = self.data['Date (D/M/Y)'] == '0/0/0'
            self.data = self.data[~null_dates]
            self.data = self.data.dropna()
            self.data = self.data.reset_index()

            # Concatenate date and time into single column
            datetime_str = self.data['Date (D/M/Y)'] + 'T' + self.data['Time (H:M:S)']
            date_times = pd.to_datetime(datetime_str, format='%d/%m/%YT%H:%M:%S')
            date_times = pd.Series(date_times)
            del self.data['Date (D/M/Y)']
            del self.data['Time (H:M:S)']
            self.x_columns = ['date_time'] + self.data.columns.tolist()
            self.y_columns = self.data.columns.tolist()
            self.data['date_time'] = date_times
            # Create dictionary for which each entry is a session
            self.split_on_id()
            session_keys = self.get_sorted_session_keys()
            # Set current session
            self.current_session_key = session_keys[0]
            self.cur_plot_df = self.sessions[self.current_session_key]
            self.cur_start_time = self.cur_plot_df['date_time'][0]
            self.cur_end_time = self.cur_plot_df['date_time'][len(self.cur_plot_df)-1]
            # Create plot data dictionary
            self.plot_data = dict()
            self.plot_data['x_name'] = 'date_time'
            self.plot_data['x_data'] = self.cur_plot_df['date_time'].values
            self.plot_data['y_name'] = self.y_columns[1]
            self.plot_data['y_data'] = self.cur_plot_df[self.plot_data['y_name']].values

    def update_x_plot_data(self, new_value):
        self.plot_data['x_name'] = new_value
        self.plot_data['x_data'] = self.cur_plot_df[new_value].values

    def update_y_plot_data(self, new_value):
        self.plot_data['y_name'] = new_value
        self.plot_data['y_data'] = self.cur_plot_df[new_value].values

    def update_session_plot_data(self, new_session_key):
        self.current_session_key = new_session_key
        self.cur_plot_df = self.sessions[self.current_session_key]
        self.plot_data['x_data'] = self.cur_plot_df[self.plot_data['x_name']].values
        self.plot_data['y_data'] = self.cur_plot_df[self.plot_data['y_name']].values
        start_time = self.cur_plot_df['date_time'][0]
        self.cur_start_time = DataManager.PdTimestamp2Datetime(start_time).time()
        end_time = self.cur_plot_df['date_time'][len(self.cur_plot_df) - 1]
        self.cur_end_time = DataManager.PdTimestamp2Datetime(end_time).time()

    def split_on_id(self):
        gap_indexes = self.data[self.data['Session Index'] == 0].index.tolist()
        if len(gap_indexes) == 1:
            self.sessions[self.data['date_time'][0]] = self.data
        else:
            for i in range(len(gap_indexes) - 1):
                df_session = self.data[gap_indexes[i]: gap_indexes[i+1]]
                df_session = df_session.reset_index()
                self.sessions[df_session['date_time'][0]] = df_session
            df_session = self.data[gap_indexes[len(gap_indexes)-1]:]
            df_session = df_session.reset_index()
            self.sessions[df_session['date_time'][0]] = df_session

    def get_sorted_session_keys(self):
        if self.sessions:
            session_keys = []
            for key in self.sessions:
                session_keys.append(key)
            return sorted(session_keys)
        else:
            return None

    def apply_time_filter(self, start_time, end_time):
        import datetime as dt
        self.cur_start_time = start_time
        self.cur_end_time = end_time
        date = self.sessions[self.current_session_key]['date_time'][0].date()
        start_time = pd.to_datetime(dt.datetime.combine(date, start_time))
        end_time = pd.to_datetime(dt.datetime.combine(date, end_time))
        current_session = self.sessions[self.current_session_key]
        self.cur_plot_df = current_session[(current_session['date_time'] > start_time) &
                                           (current_session['date_time'] < end_time)]
        self.plot_data['x_data'] = self.cur_plot_df[self.plot_data['x_name']].values
        self.plot_data['y_data'] = self.cur_plot_df[self.plot_data['y_name']].values

    def apply_moving_avg(self, window_len=10):
        # Get the pandas series from current df
        y_data = self.cur_plot_df[self.plot_data['y_name']]
        y_data = y_data.rolling(window=window_len).mean()
        null_mask = pd.notnull(y_data)
        y_data = y_data[null_mask]
        self.plot_data['y_data'] = y_data.values
        self.plot_data['x_data'] = self.plot_data['x_data'][null_mask]

    @staticmethod
    def PdTimestamp2Datetime(PdTimestamp):
        import datetime
        time_str = str(PdTimestamp)
        return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('cleanlooks')
    myapp = StartPegasusViewer()
    myapp.show()
    sys.exit(app.exec_())
