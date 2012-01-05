# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file Ui_VTEnviro.ui
# Created with: PyQt4 UI code generator 4.4.4
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VTEnviro(object):
    def setupUi(self, VTEnviro):
        VTEnviro.setObjectName("VTEnviro")
        VTEnviro.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(VTEnviro)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(VTEnviro)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), VTEnviro.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), VTEnviro.reject)
        QtCore.QMetaObject.connectSlotsByName(VTEnviro)

    def retranslateUi(self, VTEnviro):
        VTEnviro.setWindowTitle(QtGui.QApplication.translate("VTEnviro", "VTEnviro", None, QtGui.QApplication.UnicodeUTF8))
