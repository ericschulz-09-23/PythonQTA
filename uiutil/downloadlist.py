#-*- coding:utf-8 -*-
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import time
import socket
import urllib.request

'''
    下载状态报告接口
'''
class IDownloadReporter:
    '''
        报告错误
    '''
    def error(self,txt):
        raise NotImplementedError
    
    '''
        报告进度
    '''
    def progress(self,percent):
        raise NotImplementedError

    '''
        报告完成
    '''
    def finish(self):
        raise NotImplementedError

'''
    下载任务描述信息类
'''
class DownloadTaskInfo:
    def __init__(self,source,dest,reporter):
        self.sourceUrl = source
        self.localPath = dest
        self.isDeleted = False
        self.isFinished = False
        self.reporter = reporter
        self.reporter.taskInfo = self

    '''
        显示下载进度
    '''
    def reportProgress(self,blocknum,blocksize,totalsize):
        percent=int(((blocknum*blocksize)/totalsize) * 100)
        if percent>100:
            percent=100
        
        #显示进度
        if percent>=0:
            print("正在下载{0}>>>{1}%".format(self.sourceUrl,percent))
            if self.reporter != None:
                self.reporter.progress(percent)

'''
    多线程下载类(使用同步Queue实现的多文件下载)
'''
class DownloadWorker(threading.Thread):
    def __init__(self):
        super().__init__()
        #生成一个队列对象
        self.queue = queue.Queue()
        #设置线程守护
        self.setDaemon(True)
        #设置运行标记
        self.isRunning = True
        #创建线程池
        self.downloadThreadPool = ThreadPoolExecutor(32)
        #设置超时时间为30s
        socket.setdefaulttimeout(30)
        #下载失败重试次数
        self.errorTryCount = 10
        #设置UserAgent
        self.userAgentString = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    '''
        添加入队(同步方法)
    '''
    def addTask(self,task):
        self.queue.put(task)

    '''
        对象出队(同步方法)
    '''
    def __getTask(self):
        return self.queue.get(True,2)

    '''
        数据下载私有函数
    '''
    def __download(self,task):
        #安装请求头
        opener = urllib.request.build_opener()
        opener.addheaders=[('user-agent',self.userAgentString)]
        urllib.request.install_opener(opener)
        #下载数据
        try:
            urllib.request.urlretrieve(task.sourceUrl,filename=task.localPath,reporthook=task.reportProgress)
        except socket.timeout:
            count = 1
            while count <= self.errorTryCount:
                if task.reporter != None:
                    task.reporter.error('正在进行第{0}次重试！'.format(str(count)))
                try:
                    urllib.request.urlretrieve(task.sourceUrl,filename=task.localPath,reporthook=task.reportProgress)
                    break
                except socket.timeout:
                    err_info = 'Reloading for %d time'%count if count == 1 else 'Reloading for %d times'%count
                    print(err_info)
                    count += 1
                except Exception as ex1:
                    if task.reporter != None:
                        task.reporter.error(str(ex1))
            #报告超时错误
            if count > self.errorTryCount:
                if task.reporter != None:
                    task.reporter.error('对不起，超过重试次数！')
                raise Exception("download error!")
        except Exception as ex2:
            if task.reporter != None:
                task.reporter.error(str(ex2))
        #下载完成
        if task.reporter != None:
            task.reporter.finish()

    '''
        线程方法体
    '''
    def run(self):
        print('DownloadTheadStart!')
        while self.isRunning==True:
            task = None
            try:
                #取下载任务
                task = self.__getTask()
            except Exception as exx:
                pass
            try:
                if (task != None):
                    #已删除的任务直接pass
                    if (task.isDeleted==True):
                        continue
                    else:
                        print('Task:{0}'.format(task.sourceUrl))
                        #使用线程池调用下载函数
                        self.downloadThreadPool.submit(self.__download,task)
                #睡一会
                time.sleep(0.3)
            except Exception as ex:
                print('DownloadError:' + str(ex))
        print('DownloadTheadEnd!')
