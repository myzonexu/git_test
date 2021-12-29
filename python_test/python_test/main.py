# -*- coding: utf-8 -*-

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
    robots.init_current(robot1.unique_id)
    thread_manage()
    sys.exit(app.exec_())

   