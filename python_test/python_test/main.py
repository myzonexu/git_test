# -*- coding: utf-8 -*-
import sys
import time

#from PyQt5.Qt import *
from PyQt5.Qt import QMainWindow,QApplication
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QTimer

# 导入ui文件，ui_main是.ui文件生成的.py文件名
from ui_main import Ui_mainWindow
from func_main import *


class Window(QMainWindow, Ui_mainWindow):
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
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.func_list()
    window.show()
    do_main_ui(window,master_robo)
    sys.exit(app.exec_())
    