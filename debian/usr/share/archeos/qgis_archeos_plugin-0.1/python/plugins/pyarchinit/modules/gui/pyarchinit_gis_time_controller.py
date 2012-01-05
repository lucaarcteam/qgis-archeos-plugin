# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/pyarchinit/.qgis/python/plugins/pyarchinit/modules/gui/pyarchinit_gis_time_controller.ui'
#
# Created: Wed Mar 24 21:39:35 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogGisTimeController(object):
    def setupUi(self, DialogGisTimeController):
        DialogGisTimeController.setObjectName("DialogGisTimeController")
        DialogGisTimeController.resize(400, 156)
        DialogGisTimeController.setMinimumSize(QtCore.QSize(400, 156))
        DialogGisTimeController.setMaximumSize(QtCore.QSize(400, 156))
        DialogGisTimeController.setSizeIncrement(QtCore.QSize(400, 156))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/iconTimeControll.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogGisTimeController.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(DialogGisTimeController)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(DialogGisTimeController)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 3)
        self.label = QtGui.QLabel(DialogGisTimeController)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.spinBox_cron_iniz = QtGui.QSpinBox(DialogGisTimeController)
        self.spinBox_cron_iniz.setMinimum(-4000000)
        self.spinBox_cron_iniz.setMaximum(2010)
        self.spinBox_cron_iniz.setSingleStep(250)
        self.spinBox_cron_iniz.setObjectName("spinBox_cron_iniz")
        self.gridLayout.addWidget(self.spinBox_cron_iniz, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(DialogGisTimeController)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(DialogGisTimeController)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.spinBox_cron_fin = QtGui.QSpinBox(DialogGisTimeController)
        self.spinBox_cron_fin.setMinimum(-4000000)
        self.spinBox_cron_fin.setMaximum(2010)
        self.spinBox_cron_fin.setSingleStep(250)
        self.spinBox_cron_fin.setObjectName("spinBox_cron_fin")
        self.gridLayout.addWidget(self.spinBox_cron_fin, 2, 1, 1, 1)
        self.label_5 = QtGui.QLabel(DialogGisTimeController)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)
        self.pushButton_visualize = QtGui.QPushButton(DialogGisTimeController)
        self.pushButton_visualize.setMinimumSize(QtCore.QSize(100, 15))
        self.pushButton_visualize.setObjectName("pushButton_visualize")
        self.gridLayout.addWidget(self.pushButton_visualize, 3, 1, 1, 1)

        self.retranslateUi(DialogGisTimeController)
        QtCore.QMetaObject.connectSlotsByName(DialogGisTimeController)

    def retranslateUi(self, DialogGisTimeController):
        DialogGisTimeController.setWindowTitle(QtGui.QApplication.translate("DialogGisTimeController", "pyArchInit Gestione Scavi - Time Controller", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogGisTimeController", "Seleziona il periodo da visualizzare sul GIS compreso tra:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogGisTimeController", "Cronologia iniziale", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DialogGisTimeController", "a. C.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DialogGisTimeController", "Cronologia finale", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("DialogGisTimeController", "d. C.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_visualize.setToolTip(QtGui.QApplication.translate("DialogGisTimeController", "Prev rec", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_visualize.setText(QtGui.QApplication.translate("DialogGisTimeController", "Visualizza", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
