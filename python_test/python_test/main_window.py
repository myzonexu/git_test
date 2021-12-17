# -*- coding: utf-8 -*-
#import sys
#import time
#import threading

from PyQt5.Qt import QMainWindow,QApplication
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSlot

from ui_main import Ui_MainWindow
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

    @pyqtSlot()
    def on_pushButton_add_task_clicked(self):
        print("按下添加")

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
    
    def show_table_error_list(self):
        if self.radioButton_err_active.isChecked():
            err_list=robot_group.robot_selected.error_chassis.active_err_info()
        else:
            err_list=robot_group.robot_selected.error_chassis.history_err_info()
        table_fill_data_list_2d(self.tableWidget_error,err_list)
        
    @pyqtSlot()
    def on_radioButton_err_active_toggled(self):
        self.show_table_error_list()
    @pyqtSlot()
    def on_pushButton_clear_err_clicked(self):
        if self.radioButton_err_active.isChecked():
            #清除现行故障
            pass
        else:
            robot_group.robot_selected.error_chassis.clear_history()
 

    
