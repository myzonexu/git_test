# -*- coding: utf-8 -*-
import sys
import time
import threading

from PyQt5.Qt import QMainWindow,QApplication
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSlot

from ui_main import Ui_MainWindow
from func_main import *
from func_camera import *


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
 
    def slot1(self):
        #print('信号处理')
        pass
 
    def func_list(self):
        self.func()
  
    def func(self):
        #print('窗口函数')
        pass 
    #@pyqtSlot()
    #def on_pushButton_add_task_clicked(self):
        #print("按下添加")

    def resizeEvent(self, QResizeEvent):
        #Window resize event.
        super().resizeEvent(QResizeEvent)
        try:
            if camera_robo.has_init():
                width_old=self.scrollArea_camera.width()
                height=self.scrollArea_camera.height()
                width_new=int(height*camera_robo.ratio_w_h)
                width_offset=width_new-width_old
                self.groupBox_map.resize(self.groupBox_map.width()-width_offset,self.groupBox_map.height())
                self.scrollArea_camera.move(self.scrollArea_camera.x()-width_offset,self.scrollArea_camera.y())
                self.scrollArea_camera.resize(width_new,height)
            else:
                pass
        except Exception as e:
            print(e)
        
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_main = Window()
    window_main.func_list()    
    window_main.show()
    do_main_ui(window_main,master_robo,camera_robo)
    #增加线程
    thread_camera = threading.Thread(target=do_show_camera,args=(window_main,master_robo,camera_robo,), name='thread_camera')
    thread_camera.start()
    #thread_camera.join()
    thread_ui_refresh = threading.Thread(target=do_ui_refresh,args=(window_main,master_robo,), name='thread_ui_refresh')
    thread_ui_refresh.start()
    sys.exit(app.exec_())
    