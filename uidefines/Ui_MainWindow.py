# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/flyss/myData/myCode/pythonWorkSpace/QTApplicationTemplete/PythonQTApplicationTemplete/uiDefines/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(839, 307)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnTestA = QtWidgets.QPushButton(self.centralwidget)
        self.btnTestA.setGeometry(QtCore.QRect(90, 40, 121, 51))
        self.btnTestA.setObjectName("btnTestA")
        self.txtContent = QtWidgets.QTextEdit(self.centralwidget)
        self.txtContent.setGeometry(QtCore.QRect(250, 30, 321, 70))
        self.txtContent.setObjectName("txtContent")
        self.btnTestB = QtWidgets.QPushButton(self.centralwidget)
        self.btnTestB.setGeometry(QtCore.QRect(590, 40, 121, 51))
        self.btnTestB.setObjectName("btnTestB")
        self.btnTestC = QtWidgets.QPushButton(self.centralwidget)
        self.btnTestC.setGeometry(QtCore.QRect(250, 120, 121, 51))
        self.btnTestC.setObjectName("btnTestC")
        self.btnTestD = QtWidgets.QPushButton(self.centralwidget)
        self.btnTestD.setGeometry(QtCore.QRect(450, 120, 121, 51))
        self.btnTestD.setObjectName("btnTestD")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 839, 36))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnTestA.setText(_translate("MainWindow", "测试A"))
        self.btnTestB.setText(_translate("MainWindow", "测试B"))
        self.btnTestC.setText(_translate("MainWindow", "测试C"))
        self.btnTestD.setText(_translate("MainWindow", "测试D"))

