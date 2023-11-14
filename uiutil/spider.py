#-*- coding:utf-8 -*-
import sys
import os
import pathlib
import js2py
from twisted.internet import reactor
import scrapy.crawler as crawler
import scrapy
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process, Queue
from scrapy.utils.log import configure_logging
from uiutil.globaltool import *
import json

'''
    使用JS代码实现蜘蛛程序
'''
class JsSpider(scrapy.Spider):
    #Spider名称
    name = 'JsSpider'

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        #初始化解析器名称
        self.currentParseName = 'main'
        #初始化地址
        try:
            self.initStartUrls()
            for url in self.start_urls:
                print('URL:' + url)
        except Exception  as ex:
            print(ex)

    '''
        初始化地址
    '''
    def initStartUrls(self):
        if jsSpider.urlCode != None:
            getUrls = js2py.eval_js(jsSpider.urlCode)
            self.start_urls = getUrls()

    '''
        使用JS代码进行解析
    '''
    def parse(self, response):
        try:
            if jsSpider.resolveCode != None:
                spiderRun = js2py.eval_js(jsSpider.resolveCode)
                nextPageJsons = json.loads(spiderRun(self.currentParseName, response))
                print(nextPageJsons)
                if nextPageJsons.get('type') != None:
                    nextType = nextPageJsons['type']
                    nextParseName = nextPageJsons['parse']
                    nextPageUrls = nextPageJsons['urls']
                    for url in nextPageUrls:
                        if nextType == 'request':
                            self.currentParseName = nextParseName
                            yield scrapy.Request(url, callback=self.parse)
                        elif nextType == 'follow':
                            self.currentParseName = nextParseName
                            yield response.follow(url, callback=self.parse)
        except Exception as ex:
            print(ex)

'''
    蜘蛛工具
'''
class SpiderTool:
    '''
        创建蜘蛛进程
    '''
    def createSpiderProcess(scriptPluginDir):
        def f(q):
            try:
                runner = crawler.CrawlerRunner()
                deferred = runner.crawl(jsSpider)
                deferred.addBoth(lambda _: reactor.stop())
                reactor.run()
                q.put(None)
            except Exception as e:
                q.put(e)
        #载入脚本
        jsSpider.urlCode = IOTool.readAllText(os.path.join(scriptPluginDir, 'url.js'))
        jsSpider.resolveCode = IOTool.readAllText(os.path.join(scriptPluginDir, 'spider.js'))
        #运行蜘蛛程序
        q = Queue()
        return Process(target=f, args=(q,))

    '''
        使用Xpath方式解析数据
    '''
    def resolveXPath(response, xpathString):
        return response.xpath(xpathString).extract()

    '''
        使用scrapy.Request方式()
    '''
    def requestPage(pName, urls):
        urlTT = []
        for u in urls:
            urlTT.append(u)
        data={'type': 'request', 'parse': pName, 'urls': urlTT}
        return json.dumps(data, indent=4)

    '''
        使用response.follow方式()
    '''
    def followPage(pName, urls):
        urlTT = []
        for u in urls:
            urlTT.append(u)
        data={'type': 'follow', 'parse': pName, 'urls': urlTT}
        return json.dumps(data, indent=4)

    '''
        不需要下一页
    '''
    def noPage():
        data={'type': 'nopage', 'parse': 'none', 'urls': []}
        return json.dumps(data, indent=4)

    '''
        初始化日志接口
    '''
    def initLogger(loggers):
        spidertool.logger = loggers

    '''
        打印日志
    '''
    def printLog(content):
        try:
            if spidertool.logger != None:
                spidertool.logger.printLog(content)
        except Exception as ex:
            print(ex)

    '''
        报告下载地址
    '''
    def reportDownloadUrl(url):
        try:
            if spidertool.logger != None:
                spidertool.logger.reportDownloadUrl(url)
        except Exception as ex:
            print(ex)

    '''
        报告下载完成
    '''
    def reportFinish():
        try:
            if spidertool.logger != None:
                spidertool.logger.reportFinish()
        except Exception as ex:
            print(ex)

'''
    日志接口
'''
class ILogDisplay:
    '''
        显示日志
    '''
    def printLog(self, content):
        raise NotImplementedError

    '''
        报告下载地址
    '''
    def reportDownloadUrl(self, url):
        raise NotImplementedError

    '''
        搜索完成
    '''
    def reportFinish(self):
        raise NotImplementedError
