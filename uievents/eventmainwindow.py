#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *
from uievents.awindowbase import *
from uidefines.Ui_MainWindow import *
from uievents.eventsplashwindow import *
import os
import sys
import pathlib
import datetime

'''
    这是MainWindow窗体的实现类
'''
#class FMainWindow(IWindowImpl):
class FMainWindow(IWindowImplM):
    '''
       初始化所有数据(抽象函数)
    '''
    def initUIAndData(self):
        self.initEvents()
        self.msgWorker = QTInvokeQueueWorker(self)
        self.msgWorker.start()

    '''
        初始化事件
    '''
    def initEvents(self):
        self.uiObj.btnTestA.clicked.connect(self.btnTestAClicked)
        self.uiObj.btnTestB.clicked.connect(self.btnTestBClicked)
        self.uiObj.btnTestC.clicked.connect(self.btnTestCClicked)
        self.uiObj.btnTestD.clicked.connect(self.btnTestDClicked)

    '''
       返回UI定义类的实例(例如uiDefines/Ui_MainWindow.py的实例,抽象函数)
    '''
    def getUIDefineObject(self):
        return Ui_MainWindow()

    '''
        InvokeUI的实现(用于跨线程操作UI内容)
    '''
    def runUIImpl(self, uiArgs):
        self.uiObj.txtContent.setText(uiArgs.content)

    '''
        按钮A
    '''
    def btnTestAClicked(self, e):
        #显示SplashWindow窗体,SplashProcess为实现类
        FSplashWindow.showWindow('aaaaa', SplashProcess())

    '''
        按钮B
    '''
    def btnTestBClicked(self, e):
        if QMessageBox.question(self,"消息框标题","这是一条问答。",QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.invokeUI(QTObjectInvokeArgs("bbbbbbbbbbbbbbb"))

    '''
        按钮C
    '''
    def btnTestCClicked(self, e):
        self.msgWorker.addMsg(QTObjectInvokeArgs(datetime.datetime.now().__str__()))

    '''
        按钮D
    '''
    def btnTestDClicked(self, e):
        IOTool.shellExecute('file:///home/flyss/Downloads')

'''
    SplashProcess为SplashWindow显示控制类
'''
class SplashProcess(ISplashDoWork):
    def process(self):
        #显示进度为10,内容为111111111111111111111111
        self.eventObj.msgWorker.addMsg(SplashInvokeArgs(10, '111111111111111111111111'))
        time.sleep(1)
        #显示进度为30,内容为222222222222222222222222
        self.eventObj.msgWorker.addMsg(SplashInvokeArgs(30, '222222222222222222222222'))
        time.sleep(1)
        #显示进度为60,内容为333333333333333333333333
        self.eventObj.msgWorker.addMsg(SplashInvokeArgs(60, '333333333333333333333333'))
        time.sleep(1)
        #显示进度为80,内容为444444444444444444444444
        self.eventObj.msgWorker.addMsg(SplashInvokeArgs(80, '444444444444444444444444'))
        time.sleep(1)
        #显示进度为100,内容为555555555555555555555555
        self.eventObj.msgWorker.addMsg(SplashInvokeArgs(100, '555555555555555555555555'))
        time.sleep(1)
        #关闭窗体
        self.windowObj.close()
