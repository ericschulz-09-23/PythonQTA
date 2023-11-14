# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/flyss/myData/myCode/pythonWorkSpace/PythonQTApplicationTemplete/uiDefines/SplashWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SplashWindow(object):
    def setupUi(self, SplashWindow):
        SplashWindow.setObjectName("SplashWindow")
        SplashWindow.resize(711, 170)
        SplashWindow.setStyleSheet("background: rgb(133, 133, 133)")
        self.centralwidget = QtWidgets.QWidget(SplashWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lblContent = QtWidgets.QLabel(self.centralwidget)
        self.lblContent.setGeometry(QtCore.QRect(10, 10, 691, 111))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lblContent.setFont(font)
        self.lblContent.setStyleSheet("border:1px solid rgb(255, 255, 255);\n"
"color:rgb(255, 255, 255);\n"
"border-radius: 15px;")
        self.lblContent.setAlignment(QtCore.Qt.AlignCenter)
        self.lblContent.setWordWrap(True)
        self.lblContent.setObjectName("lblContent")
        self.pbProgress = QtWidgets.QProgressBar(self.centralwidget)
        self.pbProgress.setGeometry(QtCore.QRect(10, 130, 690, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pbProgress.setFont(font)
        self.pbProgress.setStyleSheet("color:rgb(255, 255, 255);\n"
"border:1px solid rgb(255, 255, 255);")
        self.pbProgress.setProperty("value", 50)
        self.pbProgress.setAlignment(QtCore.Qt.AlignCenter)
        self.pbProgress.setObjectName("pbProgress")
        SplashWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashWindow)
        QtCore.QMetaObject.connectSlotsByName(SplashWindow)

    def retranslateUi(self, SplashWindow):
        _translate = QtCore.QCoreApplication.translate
        SplashWindow.setWindowTitle(_translate("SplashWindow", "MainWindow"))
        self.lblContent.setText(_translate("SplashWindow", "xxxxxxxxxxx"))

