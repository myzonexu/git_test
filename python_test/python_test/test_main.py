# -*- coding: utf-8 -*-


import sys
import time

#from PyQt5.Qt import *
from PyQt5.Qt import QMainWindow,QApplication
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QTimer

from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


# 导入ui文件，ui_main是.ui文件生成的.py文件名
from ui_test import Ui_MainWindow
from func_main import *


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
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.func_list()
    bro=QWebEngineView()
    
    bro.load(QUrl('https://www.baidu.com'))
    #bro.setParent(window.widget)
    #bro.setParent(window.scrollArea)
    window.scrollArea.setWidget(bro)
    #bro.setGeometry(0,0,1200,800)
    #bro.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #print(dir(bro))
    #window.widget.child(bro)

    print(window.scrollArea.geometry())
    
    #window.widget_bro.show()
    window.show()
    #do_main_ui(window,master_robo)
    sys.exit(app.exec_())
'''
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('百度')  #窗口标题
        self.setGeometry(5,30,1355,730)  #窗口的大小和位置设置
        self.browser=QWebEngineView()
        #加载外部的web界面
        self.browser.load(QUrl('https://www.baidu.com'))
        self.setCentralWidget(self.browser)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=MainWindow()
    win.show()
    app.exit(app.exec_())
'''

