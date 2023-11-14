#-*- coding:utf-8 -*-
#
#  Python启动入口
#
import sys

from PyQt5.QtWidgets import QApplication
from uiutil.globaltool import *
from uiutil.envs import *
from programs import *

#***************下面这段是启动代码，绝对不能删除！！！也不建议修改***************
if __name__ == '__main__':
    #创建目录以及载入配置(不建议修改！！)
    CFEnv.initEnvData()
    #调用Program类中的main函数，启动程序（绝对不能删除！！！也不建议修改！！！）
    Program.main(sys.argv)
