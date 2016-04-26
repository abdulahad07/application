# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Kedar\Projects\smartcfd\work\dev\smartcfd-2.0\src\Preferences.ui'
#
# Created: Thu Nov 28 20:09:40 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName(_fromUtf8("Preferences"))
        Preferences.resize(621, 190)
        Preferences.setWindowTitle(QtGui.QApplication.translate("Preferences", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_3 = QtGui.QGridLayout(Preferences)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Preferences)
        self.label.setText(QtGui.QApplication.translate("Preferences", "Default Path", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.defaultPath_ledit = QtGui.QLineEdit(Preferences)
        self.defaultPath_ledit.setObjectName(_fromUtf8("defaultPath_ledit"))
        self.gridLayout.addWidget(self.defaultPath_ledit, 0, 1, 1, 1)
        self.browseButton = QtGui.QPushButton(Preferences)
        self.browseButton.setText(QtGui.QApplication.translate("Preferences", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.gridLayout.addWidget(self.browseButton, 0, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(Preferences)
        self.label_2.setText(QtGui.QApplication.translate("Preferences", "License server", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.licServer_ledit = QtGui.QLineEdit(Preferences)
        self.licServer_ledit.setObjectName(_fromUtf8("licServer_ledit"))
        self.horizontalLayout.addWidget(self.licServer_ledit)
        self.label_3 = QtGui.QLabel(Preferences)
        self.label_3.setText(QtGui.QApplication.translate("Preferences", "port", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.licPort_ledit = QtGui.QLineEdit(Preferences)
        self.licPort_ledit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.licPort_ledit.setMaxLength(1000)
        self.licPort_ledit.setObjectName(_fromUtf8("licPort_ledit"))
        self.horizontalLayout.addWidget(self.licPort_ledit)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 81, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Preferences)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Preferences)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Preferences.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Preferences.reject)
        QtCore.QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        pass

