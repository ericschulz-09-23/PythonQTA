#-*- coding:utf-8 -*-
import sys
import os
import pathlib
import json
import base64
import subprocess
import shutil
import io
from PyQt5 import QtCore, QtGui
from uiutil.envs import CFEnv

'''
   用于模仿C#下的StringBuilder的功能
'''
class StringBuffer(object):
    def __init__(self):
        super().__init__()
        StringBuffer.enterFlag = '{<%enter%>}'
        self.clear()

    '''
       清空缓冲区
    '''
    def clear(self):
        self.__buf = ''
        return self

    '''
       添加文字
    '''
    def append(self,cnt):
        self.__buf = self.__buf + (cnt.replace('\r','').replace('\n',StringBuffer.enterFlag))
        return self

    '''
       添加文字并添加换行符
    '''
    def appendLine(self,cnt):
        self.append(cnt).append(StringBuffer.enterFlag)
        return self

    '''
       将文字放入缓冲区
    '''
    def fromString(self,cnt):
        self.__buf = (cnt.replace('\r','').replace('\n',StringBuffer.enterFlag))
        return self

    '''
       输出文字
    '''
    def toString(self):
        return self.__buf.replace(StringBuffer.enterFlag,'\n')

    '''
       解析Base64编码并放入缓冲区
    '''
    def fromB64String(self,b64String):
        return self.fromString(str(base64.b64decode(b64String), "utf-8"))        

    '''
       将内容编译为Base64文字并输出
    '''
    def toB64String(self):
        return str(base64.b64encode(self.__buf.encode("utf-8")), "utf-8")

'''
    Json字典
'''
class JsonDict(object):
    def __init__(self):
        super().__init__()
        self.__buf = {}

    '''
       添加或更新
    '''
    def addOrUpdate(self,cName,cContent):
        self.__buf[cName] = cContent

    '''
       删除
    '''
    def remove(self,cName):
        try:
            return self.__buf.pop(cName)
        except Exception as ex:
            return None

    '''
       载入Json字典数据(从Json字符串)
    '''
    def load(self,cnt):
        try:
            self.__buf = json.loads(cnt)
        except Exception as ex:
            self.__buf = {}

    '''
       从文件载入Json字典数据(从文件)
    '''
    def loadFile(self,file):
        self.load(IOTool.readAllText(file))

    '''
       从文件载入Json字典数据(从ScriptDir中的文件)
    '''
    def loadFileFromScriptDir(self,fName):
        self.loadFile(os.path.join(CFEnv.scriptDir,fName))

    '''
       保存Json数据到文件
    '''
    def saveFile(self,file):
        IOTool.writeAllText(file,json.dumps(self.__buf,indent=4))

    '''
       保存Json数据到ScriptDir中的文件
    '''
    def saveFileToScriptDir(self,fName):
        self.saveFile(os.path.join(CFEnv.scriptDir,fName))

    '''
       获得数据
    '''
    def getValue(self,pName,defaultVal):
        if self.__buf.get(pName) == None:
            return defaultVal
        else:
            return self.__buf[pName]

    '''
       字典缓存中的items()函数
    '''
    def items(self):
        return self.__buf.items()

    '''字典缓存中的keys()函数
    '''
    def keys(self):
        keyList = []
        for k,v in self.items():
            keyList.append(k)
        return keyList

    '''
       字典缓存中的clear()函数
    '''
    def clear(self):
        self.__buf.clear()

    '''
       字典记录数
    '''
    def count(self):
        return len(self.__buf)

    '''
       输出Json串
    '''
    def toJsonString(self):
        return json.dumps(self.__buf,indent=4)
    
'''
    代码生成（主要用于载入模板文件然后替换）
'''
class CodeMaker(object):
    def __init__(self):
        self.__templete = ''
        self.kvData = JsonDict()

    '''
        载入模板(从字符串)
    '''
    def loadTemplete(self,cnt):
        self.__templete = cnt
    
    '''
        载入模板(从文件)
    '''
    def loadTempleteFile(self,file):
        self.loadTemplete(IOTool.readAllText(file))

    '''
        载入模板(从ScriptDir中的文件)
    '''
    def loadTempleteFileFromScriptDir(self,tName):
        self.loadTempleteFile(os.path.join(CFEnv.scriptDir,tName))

    '''
        替换关键字
    '''
    def execute(self):
        tempStr = self.__templete
        for k,v in self.kvData.items():
            replaceKey = '$%' + k + '%$'
            tempStr = tempStr.replace(replaceKey,v)
        return StringBuffer().fromString(tempStr)

'''
   读写工具类
'''
class IOTool(object):
    '''
        模仿Windows的ShellExecute的实现（可以打开http://或file://等）
    '''
    def shellExecute(url):
        return QtGui.QDesktopServices.openUrl(QtCore.QUrl(url, QtCore.QUrl.TolerantMode))

    '''
      运行指令并等待返回结果（会阻塞直到完成）
      输入参数：命令行字符串，返回内容编码
      返回参数: 文本内容+错误信息，文本内容，错误信息
    '''
    def start(cmdStr,responseCoding):
       print('start command:' + cmdStr)
       proc = subprocess.Popen(cmdStr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
       proc.wait()
       stream_stdout = io.TextIOWrapper(proc.stdout, encoding=responseCoding)
       stream_stderr = io.TextIOWrapper(proc.stderr, encoding=responseCoding)      
       str_stdout = str(stream_stdout.read())
       str_stderr = str(stream_stderr.read())
       print("stdout: " + str_stdout)
       print("stderr: " + str_stderr)
       result = (str_stdout + str_stderr).strip()
       print('stdresult:' + result)
       return result,str_stdout,str_stderr

    '''
      读入所有文本
    '''
    def readAllText(fPath):
        result = ""
        if pathlib.Path(fPath).exists():
            try:
                f = open(fPath,mode='r',encoding='utf-8')
                result = f.read()
                f.close()
            except IOError as e:
                print(e)            
        return result

    '''
      读入所有字节
    '''
    def readAllByte(fPath):
        result = b''
        if pathlib.Path(fPath).exists():
            try:
                f = open(fPath,mode='rb')
                result = f.read()
                f.close()
            except IOError as e:
                print(e)            
        return result

    '''
      写入所有文本
    '''
    def writeAllText(fPath,strContent):
        try:
            f = open(fPath,mode='w',encoding='utf-8')
            f.write(strContent)
            f.close()
        except IOError as e:
            print(e)

    '''
      写入所有字节
    '''
    def writeAllByte(fPath,byteContent):
        try:
            f = open(fPath,mode='wb')
            f.write(byteContent)
            f.close()
        except IOError as e:
            print(e)

    '''
      追加文本
    '''
    def appendText(fPath,strContent):
        try:
            f = open(fPath,mode='a',encoding='utf-8')
            f.write(strContent)
            f.close()
        except IOError as e:
            print(e)

    '''
      追加字节
    '''
    def appendByte(fPath,byteContent):
        try:
            f = open(fPath,mode='ab')
            f.write(byteContent)
            f.close()
        except IOError as e:
            print(e)
