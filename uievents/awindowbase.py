#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *
from uiutil.envs import *
import os
import sys
import pathlib
import time
import threading
from multiprocessing import Manager
import queue

'''
    这是窗体的实现类接口
    PyQT中一个窗体的结构如下：
       QMainWindow = C#下的Form
            uiDefines中的ui_MainWidow.py=C#下的xxForm.designer.cs
            uiEvents中eventMainWindow.py=C#下的xxForm.cs
'''
class IWindowImpl:
    '''
        窗体初始化
    '''
    def initWindow(self, appObj, windowObj, uiObj):
        #保存引用
        #Application对象
        self.appObj = appObj
        #主窗体线程
        self.windowObj = windowObj
        #窗体定义类
        self.uiObj = uiObj
        #初始化所有数据
        self.initUIAndData()

    '''
       初始化所有数据(抽象函数)
    '''
    def initUIAndData(self):
        raise NotImplementedError

    '''
       返回UI定义类的实例(例如uiDefines/Ui_MainWindow.py的实例,抽象函数)
    '''
    def getUIDefineObject(self):
        raise NotImplementedError

    '''
        模仿C#中的Form.Invoke(用于跨线程操作UI内容)
    '''
    def invokeUI(self, uiArgs):
        self.invokeThread = QTUIInvokerThread(uiArgs)
        self.invokeThread.signal.connect(self.runUIImpl)
        self.invokeThread.start()

    '''
        InvokeUI的实现(用于跨线程操作UI内容)
    '''
    def runUIImpl(self, uiArgs):
        raise NotImplementedError

'''
    基于QMainWindow的窗体的实现类接口
'''
class IWindowImplM(IWindowImpl, QMainWindow):
    pass

'''
    基于QWidget的窗体的实现类接口
'''
class IWindowImplW(IWindowImpl, QWidget):
    pass

'''
    基于QDialog的窗体的实现类接口
'''
class IWindowImplD(IWindowImpl, QDialog):
    pass

'''
    窗体对象生成器(通过QMainWindow或QWidget或QDialog,结合uiDefines和uiEvent配置窗体对象)
'''
class WindowBuilder:
    '''
        创建窗体对象
        windowObj = QMainWindow或QWidget或QDialog的实例,如果为空则使用eventImpl的值充当窗体对象
        eventImpl = 窗体实现类的实例
        输出参数：QMainWindow或QWidget或QDialog的实例,窗体UI定义类的实例,窗体实现类的实例
    '''
    def buildWindow(windowObj, eventImpl):
        if eventImpl != None:
            uiDefine = eventImpl.getUIDefineObject()
            if CFEnv.appObj != None and uiDefine != None and eventImpl != None:
                #设置描述类到窗体线程
                if windowObj != None:
                    uiDefine.setupUi(windowObj)
                else:
                    uiDefine.setupUi(eventImpl)
                #初始化窗体事件类
                if windowObj != None:
                    eventImpl.initWindow(CFEnv.appObj, windowObj, uiDefine)
                    #返回对象
                    return windowObj, uiDefine, eventImpl
                else:
                    eventImpl.initWindow(CFEnv.appObj, eventImpl, uiDefine)
                    #返回对象
                    return eventImpl, uiDefine, eventImpl
            else:
                return None, None, None
        else:
                return None, None, None

'''
    Invoke参数类
'''
class QTInvokeArgs:
    pass

'''
    Invoke参数类(只有一个Content)
'''
class QTObjectInvokeArgs(QTInvokeArgs):
    def __init__(self, tag):
        super().__init__()
        self.content = tag

'''
    Invoke参数类(command,content,tag)
'''
class QTCommandInvokeArgs(QTInvokeArgs):
    def __init__(self, cmd, content, tag):
        super().__init__()
        self.command = cmd
        self.content = content
        self.tag = tag

'''
    QT的UI线程，用于模仿C#中的Form.Invoke的功能(用于跨线程操作UI内容)
'''
class QTUIInvokerThread(QThread):
    signal = pyqtSignal(QTInvokeArgs)    # 括号里填写信号传递的参数

    def __init__(self, uiArgs):
        super().__init__()
        self.uiArgs = uiArgs

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        try:
            self.signal.emit(self.uiArgs)    # 发射信号
        except Exception as exx:
            print(exx)

'''
    用Queue实现的Invoke消息队列(使用Manager.Queue()以支持进程间数据)
'''
class QTInvokeQueueWorkerWithProcess(threading.Thread):
    def __init__(self, windowObj):
        super().__init__()
        #生成一个队列对象
        self.queue = Manager().Queue()
        #设置线程守护
        self.setDaemon(True)
        #设置运行标记
        self.isRunning = True
        #设置窗体对象
        self.windowObj = windowObj
    
    '''
        添加入队(同步方法)
    '''
    def addMsg(self, task):
        self.queue.put(task)

    '''
        对象出队(同步方法)
    '''
    def __getMsg(self):
        return self.queue.get(True, 2)

    '''
        线程方法体
    '''
    def run(self):
        print('QTUIInvokeMsgQueueWorker-Start!')
        while self.isRunning==True:
            task = None
            try:
                #取下载任务
                task = self.__getMsg()
            except Exception as exx:
                pass
            try:
                if (task != None and self.windowObj != None):
                    self.windowObj.invokeUI(task)
                #睡一会
                time.sleep(0.05)
            except Exception as ex:
                print('QTUIInvokeMsgQueueWorker:' + str(ex))
        print('QTUIInvokeMsgQueueWorker-End!')

'''
    用Queue实现的Invoke消息队列
'''
class QTInvokeQueueWorker(threading.Thread):
    def __init__(self, windowObj):
        super().__init__()
        #生成一个队列对象
        self.queue = queue.Queue()
        #设置线程守护
        self.setDaemon(True)
        #设置运行标记
        self.isRunning = True
        #设置窗体对象
        self.windowObj = windowObj
    
    '''
        添加入队(同步方法)
    '''
    def addMsg(self, task):
        self.queue.put(task)

    '''
        对象出队(同步方法)
    '''
    def __getMsg(self):
        return self.queue.get(True, 2)

    '''
        线程方法体
    '''
    def run(self):
        print('QTUIInvokeMsgQueueWorker-Start!')
        while self.isRunning==True:
            task = None
            try:
                #取下载任务
                task = self.__getMsg()
            except Exception as exx:
                pass
            try:
                if (task != None and self.windowObj != None):
                    self.windowObj.invokeUI(task)
                #睡一会
                time.sleep(0.05)
            except Exception as ex:
                print('QTUIInvokeMsgQueueWorker:' + str(ex))
        print('QTUIInvokeMsgQueueWorker-End!')
