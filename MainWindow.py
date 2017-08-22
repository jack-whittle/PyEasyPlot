# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from pydispatch import dispatcher
import numpy as np
import pandas as pd
import os


class Plotter(object):
    def __init__(self):
        self.fig = plt.figure()
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot([1, 2, 3], [1, 2, 3])
        self.ax.set_xlabel('X label')
        self.ax.set_ylabel('Y label')
        dispatcher.connect(self.replot_listener, signal="UpdatePlot", sender=dispatcher.Any)
        dispatcher.connect(self.export_plot, signal="ExportPlot", sender=dispatcher.Any)

    def replot_listener(self, plot_params):
        self.ax.clear()
        # self.ax.set_xlabel(plot_params['x_name'])
        self.ax.set_ylabel(plot_params['y_name'])
        if plot_params['x_name'] == 'date_time':
            self.plot_time_series(plot_params)

    def plot_time_series(self, plot_params):
        self.ax.plot(plot_params['y_data'])
        # Add a table with summary statistics
        y_data = pd.to_numeric(plot_params['y_data'])
        summary_stats_df = pd.DataFrame([round(y_data.mean(), 3), round(y_data.std(), 3)],
                                        index=['Mean', 'Std'])
        self.ax.table(cellText=summary_stats_df.values,
                      colWidths=[0.1],
                      rowLabels=summary_stats_df.index,
                      colLabels=None,
                      cellLoc='center',
                      rowLoc='center',
                      loc='top')
        # Plot trend
        x = mdates.date2num(pd.to_datetime(plot_params['y_data'].index).to_pydatetime())
        fit = np.polyfit([float(xi) for xi in x], [float(y) for y in plot_params['y_data']], 1)
        p = np.poly1d(fit)
        self.ax.plot(list(plot_params['y_data'].index), list(p([float(xi) for xi in x])), 'm-')
        time_fmt = mdates.DateFormatter('%H:%M:%S')
        self.ax.xaxis.set_major_formatter(time_fmt)
        plt.setp(self.ax.get_xticklabels(), rotation=45)
        self.ax.legend([plot_params['y_name'], 'Trend'], loc=0)
        self.ax.grid('on')
        plt.tight_layout()
        plt.subplots_adjust(top=0.94)
        self.fig.canvas.draw()

    def plot_dependence(self, plot_params):
        return None

    def export_plot(self, plot_params, export_dir):
        self.replot_listener(plot_params)
        y_name = plot_params['y_name'].replace('/', ' per ')
        x_name = plot_params['x_name'].replace('/', ' per ')
        self.fig.savefig(export_dir + os.sep + y_name + ' Vs ' + x_name + '.png')

    def change_x_listener(self, update):
        self.ax.set_xlabel(update)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setSizeConstraint(QtWidgets.QFormLayout.SetNoConstraint)
        self.formLayout.setObjectName("formLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.pushButton_2)

        self.label_session = QtWidgets.QLabel(self.centralwidget)
        self.label_session.setObjectName("label_session")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_session)
        self.comboBox_session = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_session.setObjectName("comboBox_session")
        self.comboBox_session.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_session)

        # Decided to omit option to choose x-data
        # self.label = QtWidgets.QLabel(self.centralwidget)
        # self.label.setObjectName("label")
        # self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        # self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        # self.comboBox.setObjectName("comboBox")
        # self.comboBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setObjectName("timeEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.timeEdit)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.timeEdit_2 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_2.setObjectName("timeEdit_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.timeEdit_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.pushButton)

        self.pushButton_smooth = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_smooth.setObjectName("pushButton_smooth")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.pushButton_smooth)

        self.pushButton_export = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_export.setObjectName("pushButton_export")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.pushButton_export)
        self.horizontalLayout.addLayout(self.formLayout, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.plotter = Plotter()
        self.canvas = FigureCanvas(self.plotter.fig)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, self.centralwidget)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)
        self.horizontalLayout.addLayout(self.verticalLayout, 4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 716, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pegasus Viewer"))
        # self.label.setText(_translate("MainWindow", "X Data:"))
        self.label_2.setText(_translate("MainWindow", "Variable:"))
        self.label_3.setText(_translate("MainWindow", "Start Time:"))
        self.label_4.setText(_translate("MainWindow", "End Time:"))
        self.pushButton.setText(_translate("MainWindow", "Apply"))
        self.pushButton_export.setText(_translate("MainWindow", "Export Plots"))
        self.pushButton_smooth.setText(_translate("MainWindow", "Apply Smoothing"))
        self.pushButton_2.setText(_translate("MainWindow", "Load Data"))
        self.label_session.setText(_translate("MainWindow", "Session:"))

        # dispatcher.connect(self.update_x_combo, signal="UpdateXCombo", sender=dispatcher.Any)
        dispatcher.connect(self.update_y_combo, signal="UpdateYCombo", sender=dispatcher.Any)
        dispatcher.connect(self.update_time_fields, signal="UpdateTimeFields", sender=dispatcher.Any)

    # def update_x_combo(self, update):
    #     self.comboBox.setCurrentText(update)

    def update_y_combo(self, update):
        self.comboBox_2.setCurrentText(update)

    def update_time_fields(self, s_time, e_time):
        self.timeEdit.setMinimumTime(s_time)
        self.timeEdit.setMaximumTime(e_time)
        self.timeEdit.setTime(s_time)
        self.timeEdit_2.setMinimumTime(s_time)
        self.timeEdit_2.setMaximumTime(e_time)
        self.timeEdit_2.setTime(e_time)


