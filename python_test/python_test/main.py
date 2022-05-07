#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
File   Name ： main.py
Description :  主程序
Author      :  simon
Create Time ： 20220105
-------------------------------------------------------------------------------
Change Activity:
               时间:更改内容
-------------------------------------------------------------------------------
"""
__author__ = 'simon'

import sys
from PyQt5.Qt import QApplication

#导入功能模块
from func_robot import *
#导入UI界面
from main_window import *
#导入线程管理
from thread_manage import *

if __name__ == '__main__':    
    app = QApplication(sys.argv)
    window_main = Window()
    window_main.func_list()
    window_main.show()
    #robots.init_current(robot1.id)
    robots.init_current(list(robots.all.keys())[0])
    thread_manage()
    sys.exit(app.exec_())
