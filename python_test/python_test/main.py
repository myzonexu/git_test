# -*- coding: utf-8 -*-

import sys
import time
import threading

from PyQt5.Qt import QApplication

#导入功能模块
from func_robot import *
#导入UI界面
from main_window import *
#导入线程管理
from thread_manage import *

#线程管理
def get_camera_frame_():
    while window_main.tabWidget_main.currentIndex()==0:
        if robots.now==None:
            pass
        elif robots.now.master.is_opened():
        #if True :
            robots.now.camera.get_frame()
            robots.now.camera.frame_scale(window_main.label_camera.height())
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_main = Window()
    window_main.func_list()
    window_main.show()
    #增加线程
    #from thread_manage import *
    thread_camera = threading.Thread(target=get_camera_frame_, name='thread_camera')
    thread_camera.start()
    thread_manage()
    sys.exit(app.exec_())
    thread_camera.join()
    thread_close()
   