#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *
from uievents.awindowbase import *
from uidefines.Ui_SplashWindow import *
from uiutil.envs import *
from uiutil.globaltool import *
import os
import sys
import pathlib
import datetime

'''
    这是SplashWindow窗体的实现类
'''
#class FSplashWindow(IWindowImpl):
class FSplashWindow(IWindowImplM):
    '''
       初始化所有数据(抽象函数)
    '''
    def initUIAndData(self):
        #初始化事件
        self.initEvents()
        #初始化投递线程
        self.msgWorker = QTInvokeQueueWorkerWithProcess(self)
        self.msgWorker.start()

    '''
        初始化事件
    '''
    def initEvents(self):
        pass

    '''
       返回UI定义类的实例(例如uiDefines/Ui_MainWindow.py的实例,抽象函数)
    '''
    def getUIDefineObject(self):
        return Ui_SplashWindow()

    '''
        InvokeUI的实现(用于跨线程操作UI内容)
    '''
    def runUIImpl(self, uiArgs):
        self.uiObj.lblContent.setText(uiArgs.contentVal)
        self.uiObj.pbProgress.setValue(uiArgs.progressVal)

    '''
        显示窗体
    '''
    def showWindow(title, doWorkImpl):
        if doWorkImpl != None and title != None:
            #显示窗体
            windowObj, ui, event = WindowBuilder.buildWindow(None, FSplashWindow())
            windowObj.setWindowTitle(title)
            doWorkImpl.windowObj = windowObj
            doWorkImpl.eventObj = event
            windowObj.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            windowObj.setFixedSize(windowObj.width(), windowObj.height())
            windowObj.show()
            #运行线程
            thread = threading.Thread(target=doWorkImpl.process)
            thread.start()

'''
    Splash处理类
'''
class ISplashDoWork:
    '''
        处理数据
    '''
    def process(self):
        raise NotImplementedError

'''
    Splash的Invoke参数
'''
class SplashInvokeArgs(QTInvokeArgs):
    def __init__(self, progress, content):
        super().__init__()
        self.progressVal = progress
        self.contentVal = content
