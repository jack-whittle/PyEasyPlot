# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from pydispatch import dispatcher


class Plotter(object):
    def __init__(self):
        self.fig = plt.figure()
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot([1, 2, 3], [1, 2, 3])
        self.ax.set_xlabel('X label')
        self.ax.set_ylabel('Y label')
        plt.tight_layout()
        dispatcher.connect(self.replot_listener, signal="UpdatePlot", sender=dispatcher.Any)

    def replot_listener(self, plot_params):
        self.ax.clear()
        self.ax.set_xlabel(plot_params['x_name'])
        self.ax.set_ylabel(plot_params['y_name'])
        self.ax.plot(list(plot_params['x_data']), list(plot_params['y_data']))
        self.ax.grid('on')
        self.fig.canvas.draw()

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

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setObjectName("timeEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.timeEdit)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.timeEdit_2 = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit_2.setObjectName("timeEdit_2")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.timeEdit_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.pushButton)
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
        self.label.setText(_translate("MainWindow", "X Data:"))
        self.label_2.setText(_translate("MainWindow", "Y Data:"))
        self.label_3.setText(_translate("MainWindow", "Start Time:"))
        self.label_4.setText(_translate("MainWindow", "End Time:"))
        self.pushButton.setText(_translate("MainWindow", "Apply"))
        self.pushButton_2.setText(_translate("MainWindow", "Load Data"))
        self.label_session.setText(_translate("MainWindow", "Session:"))

        dispatcher.connect(self.update_x_combo, signal="UpdateXCombo", sender=dispatcher.Any)
        dispatcher.connect(self.update_y_combo, signal="UpdateYCombo", sender=dispatcher.Any)
        dispatcher.connect(self.update_time_fields, signal="UpdateTimeFields", sender=dispatcher.Any)

    def update_x_combo(self, update):
        self.comboBox.setCurrentText(update)

    def update_y_combo(self, update):
        self.comboBox_2.setCurrentText(update)

    def update_time_fields(self, s_time, e_time):
        self.timeEdit.setMinimumTime(s_time)
        self.timeEdit.setMaximumTime(e_time)
        self.timeEdit.setTime(s_time)
        self.timeEdit_2.setMinimumTime(s_time)
        self.timeEdit_2.setMaximumTime(e_time)
        self.timeEdit_2.setTime(e_time)


