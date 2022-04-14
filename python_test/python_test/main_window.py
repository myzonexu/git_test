# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.Qt import QMainWindow
#from PyQt5.QtGui import QImage,QPixmap
#from PyQt5.QtWebEngineWidgets import *
#from PyQt5.QtCore import QTimer
#from PyQt5.QtCore import pyqtSlot
import threading

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QObject , pyqtSignal

from PyQt5.QtXml import QDomDocument
from PyQt5 import QtSvg
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, Close
from svg.path import parse_path

from ui_main import Ui_MainWindow
#from func_main import *
from func_robot import *
from func_svg import *
from func_task import *

class Window(QMainWindow, Ui_MainWindow):
    camera_offlined = pyqtSignal()
    #初始化###################################################################################################
    def __init__(self):
        super().__init__()
        self.setupUi(self)
       

    def func_list(self):
        self.setup_ui_extra()
        self.init_robot_slot()
        self.load_map()
        
        self.thread_manage()
        #self.ui_set_shortcut()
        #self.setup_timer()

        #self.browser = QWebEngineView()
        #self.scrollArea_camera_browser.setWidget(self.browser)
        #self.browser.load(QUrl('http://192.168.0.64/'))
        
        self.scrollArea_camera_browser.show()

 
    #事件响应###################################################################################################
    def closeEvent(self,event):
        pass

    #窗口大小改变响应
    def resizeEvent(self, QResizeEvent):
        #Window resize event.
        super().resizeEvent(QResizeEvent)

        if robots.current == None:
            pass
        else:
            self.resize_camera_show()

        #print(self.svgWidget.size())

    def resize_camera_show(self):
        camera_ratio = robots.current.camera.ratio_w_h
        camrea_show_height = self.groupBox_map.height()
        camrea_show_width = int(camrea_show_height * camera_ratio)
        robots.current.camera.set_show_width(camrea_show_width)
        robots.current.camera.set_show_height(camrea_show_height)
        offset_width = camrea_show_width - self.label_camera.width()
        self.groupBox_map.resize(self.groupBox_map.width() - offset_width,self.groupBox_map.height())
        self.label_camera.move(self.label_camera.x() - offset_width,self.label_camera.y())
        self.label_camera.resize(camrea_show_width,camrea_show_height)

    #信号-槽响应###############################################################################################
    #按钮响应
    @pyqtSlot()
    def on_pushButton_autorun_start_clicked(self):
        robots.current.clean_task_start()
        robots.current.task.start_time = datetime.now()
        robots.current.task.stop_time = None
    @pyqtSlot()
    def on_pushButton_autorun_stop_clicked(self):
        robots.current.clean_task_stop()
        robots.current.task.stop_time = datetime.now()
    @pyqtSlot()
    def on_pushButton_autorun_charge_clicked(self):
        robots.current.charge_battery()
    @pyqtSlot()
    def on_pushButton_autorun_add_water_clicked(self):
        robots.current.add_water()
    @pyqtSlot()
    def on_pushButton_arm_position_origin_clicked(self):
        robots.current.arm_ctrl_position(0)
    @pyqtSlot()
    def on_pushButton_arm_position_wall_1_clicked(self):
        robots.current.arm_ctrl_position(1)
    @pyqtSlot()
    def on_pushButton_arm_position_wall_2_clicked(self):
        robots.current.arm_ctrl_position(2)
    @pyqtSlot()
    def on_pushButton_arm_position_wall_3_clicked(self):
        robots.current.arm_ctrl_position(3)
    @pyqtSlot()
    def on_pushButton_arm_position_wall_4_clicked(self):
        robots.current.arm_ctrl_position(4)
    @pyqtSlot()
    def on_pushButton_arm_position_ground_1_clicked(self):
        robots.current.arm_ctrl_position(5)
    @pyqtSlot()
    def on_pushButton_brush_clicked(self):
        if self.pushButton_brush.isChecked() == True :
            robots.current.pump_brush_ctrl(1)
            self.pushButton_brush.setText("关滚刷")
        else :
            robots.current.pump_brush_ctrl(0)
            self.pushButton_brush.setText("开滚刷")
        
    @pyqtSlot()
    def on_pushButton_arm_power_restart_clicked(self):
        robots.current.restart_arm()
    @pyqtSlot()
    def on_pushButton_tcp_connect_clicked(self):
        pass
    @pyqtSlot()
    def on_pushButton_tcp_disconnect_clicked(self):
        pass
    @pyqtSlot(int)
    def on_spinBox_robo_speed_valueChanged(self,speed):
        robots.current.free_drive_ctrl_speed(speed)
    @pyqtSlot()
    def on_pushButton_robo_speed_zero_clicked(self):
        self.spinBox_robo_speed.setValue(0)
        #robots.current.free_drive_ctrl_speed(0)
    @pyqtSlot(int)
    def on_spinBox_steer_angle_valueChanged(self,angle):
        robots.current.free_drive_ctrl_angle(angle)
    @pyqtSlot()
    def on_pushButton_steer_angle_zero_clicked(self):
        self.spinBox_steer_angle.setValue(0)
        #robots.current.free_drive_ctrl_angle(0)
    @pyqtSlot()
    def on_pushButton_chassis_power_restart_clicked(self):
        robots.current.restart_chassis()
    @pyqtSlot()
    def on_pushButton_on_track_forward_clicked(self):
        robots.current.on_track_drive_ctrl(1)
    @pyqtSlot()
    def on_pushButton_on_track_backward_clicked(self):
        robots.current.on_track_drive_ctrl(2)
    @pyqtSlot()
    def on_pushButton_on_track_pause_clicked(self):
        robots.current.on_track_drive_ctrl(3)
    @pyqtSlot()
    def on_radioButton_err_active_toggled(self):
        self.toggle_table_error_list()
    @pyqtSlot()
    def on_pushButton_clear_err_clicked(self):
        if self.radioButton_err_active.isChecked():
            robots.current.clear_active_error()
        else:
            robots.current.error_chassis.clear_history()
    #机器人列表选择
    @pyqtSlot(int,int)
    def on_tableWidget_robot_list_cellClicked(self, row, col):
        id = int(self.tableWidget_robot_list.item(row,0).text())
        #选择ID
        if col is 0:            
            robots.set_current(id)
        #选择故障
        elif col is 5:
            robots.set_current(id)
            self.tabWidget_robots_info.setCurrentIndex(0)
        #选择警告
        elif col is 6:
            robots.set_current(id)
            self.tabWidget_robots_info.setCurrentIndex(1)

    @pyqtSlot(int)
    def on_tabWidget_main_currentChanged(self,index):
        if index is 0:
            robots.current.camera.enable_capture()
            pass
        elif index is 1:
            self.setup_ui_camera_web()
            pass
        else:
            robots.current.camera.disable_capture()
            #robots.current.camera.close()
            print("关闭相机捕获")

    #计划任务预览
    @pyqtSlot()
    def on_pushButton_add_task_preview_clicked(self):
        self.preview_new_task_plan()
            
    #计划任务添加
    @pyqtSlot()
    def on_pushButton_add_task_clicked(self):
        self.set_new_task_plan()
        if task_plans.new_plan.name is "":
            QMessageBox.information(self,'提示','计划任务名称不能为空!请填写。',QMessageBox.Ok)
        else:
            self.preview_task_plan(task_plans.new_plan)        
            task_plans.new_plan.add_time=datetime.now() 
            #task_plans.new_plan.add_time=QDateTime.currentDateTime()
            task_plans.plan_list.append(task_plans.new_plan)
            table_fill_data_list_2d(self.tableWidget_task_plan_list,task_plans.list_info())

            #清空新任务信息
            self.lineEdit_add_task_name.setText("")
            task_plans.new_plan.__init__()
            self.preview_task_plan(task_plans.new_plan)
    

    #方法######################################################################################
    #UI额外设置
    def setup_ui_extra(self):
        self.init_table_group()
        self.init_ui_task_plan()
        self.setup_ui_tablewidget()
        self.setup_ui_statusbar()
        self.setup_ui_shortcut()
        self.camera_offlined.connect(self.update_ui_camera_offline)
        self.calendarWidget_task_preview.currentPageChanged.connect(self.preview_new_task_plan)
        
        

    #初始化当前机器人信号槽
    def init_robot_slot(self):
        robots.current_inited.connect(self.setup_ui_robot_current_slot)

    def setup_ui_robot_current_slot(self):
        robots.current.camera.inited.connect(self.resize_camera_show)
        robots.current.camera.frame_captured.connect(self.update_ui_camera)
        robots.current.state_updated.connect(self.update_ui)
        robots.current_changed.connect(self.update_ui)
        robots.current.master.offlined.connect(self.update_ui)
        

    def setup_ui_statusbar(self):
        self.label_wirte_buffer = QLabel('{:<100}'.format('发送缓冲区:'))
        self.statusbar.addWidget(self.label_wirte_buffer, 1)
        self.statusbar.addWidget(self.progressBar, 2)
        self.setStatusBar(self.statusbar)
    #设置快捷键
    def setup_ui_shortcut(self):
        self.pushButton_on_track_forward.setShortcut('Up')
        self.pushButton_on_track_backward.setShortcut('Down')
        self.pushButton_autorun_start.setShortcut('Home')
        self.pushButton_autorun_stop.setShortcut('End')
        self.pushButton_arm_position_origin.setShortcut('0')
        self.pushButton_arm_position_wall_1.setShortcut('1')
        self.pushButton_arm_position_wall_2.setShortcut('2')
        self.pushButton_arm_position_wall_3.setShortcut('3')
        self.pushButton_arm_position_wall_4.setShortcut('4')
        self.pushButton_arm_position_ground_1.setShortcut('5')
    #设置表格属性
    def init_table_group(self):
        self.tableWidget_group_show = [self.tableWidget_robot_list,self.tableWidget_robot_info,self.tableWidget_task_info ,
                                        self.tableWidget_error ,self.tableWidget_warning,self.tableWidget_log_info ,
                                        self.tableWidget_task_plan_list ]
    def setup_ui_tablewidget(self):
        for table_widget in self.tableWidget_group_show:
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table_widget.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)

        for i in range(0,3):
            self.tableWidget_robot_list.horizontalHeader().setSectionResizeMode(i,QHeaderView.ResizeToContents)

        for j in range(0,2):
            self.tableWidget_error.horizontalHeader().setSectionResizeMode(j,QHeaderView.ResizeToContents)

        for j in range(0,4):
            self.tableWidget_task_plan_list.horizontalHeader().setSectionResizeMode(j,QHeaderView.ResizeToContents)


    #UI更新
    def update_ui(self):
        self.update_ui_widget_enbaled()
        self.update_ui_table()
        self.update_ui_tab_text()
        self.update_ui_map()
               

    #更新表格显示
    def update_ui_table(self):
        table_fill_data_list_2d(self.tableWidget_robot_list,robots.list_info())      
        if robots.current == None:
            pass
        else:
            table_fill_data_list_2d(self.tableWidget_robot_info,robots.current.robot_info())
            table_fill_data_list_2d(self.tableWidget_task_info,robots.current.task_info())
        

            if self.radioButton_err_active.isChecked():
                err_list = robots.current.error_chassis.active_err_info()
            else:
                err_list = robots.current.error_chassis.history_err_info()
            table_fill_data_list_2d(self.tableWidget_error,err_list)

    #更新tab页文字
    def update_ui_tab_text(self):
        self.tabWidget_robots_info.setTabText(3,"机器人列表(" + str(len(robots.robots)) + ")")
        if robots.current == None:
            pass
        else:
            self.tabWidget_robots_info.setTabText(0,"故障(" + str(robots.current.err_count()) + ")")
            self.tabWidget_robots_info.setTabText(1,"警告(" + str(robots.current.warning_count()) + ")")
             
    #更新控件使能
    def update_ui_widget_enbaled(self):
        #if master.is_opened() and master.is_reconnect()==False :
        self.tabWidget_main.setTabEnabled(3,False)
        if robots.current == None:
            self.tabWidget_robo_ctrl.setEnabled(False)
        else:
            if robots.current.master.is_opened() :
                self.tabWidget_robo_ctrl.setEnabled(True)
            else:
                self.tabWidget_robo_ctrl.setEnabled(False)
    #相机web页面
    def setup_ui_camera_web(self):
        self.browser = QWebEngineView()
        self.browser.load(QUrl(robots.current.camera.web_url))
        self.scrollArea_camera_browser.setWidget(self.browser)
        self.scrollArea_camera_browser.show()

        #if robots.current==None:
        #    pass
        #else:
        #    if robots.current.camera.is_web_open==False:
        #        self.browser = QWebEngineView()
        #        self.browser.load(QUrl(robots.current.camera.web_url))
        #        self.scrollArea_camera_browser.setWidget(self.browser)
        #        self.scrollArea_camera_browser.show()
        #        print(robots.current.camera.web_url)
        #        robots.current.camera.is_web_open=True
 
    #显示监控视频
    def update_ui_camera(self):
        if robots.current == None:
            pass
        else:
            self.label_camera.setPixmap(QPixmap.fromImage(robots.current.camera.img_scaled))
            #self.label_camera.setPixmap(QPixmap.fromImage(robots.current.camera.img))
            self.progressBar.setValue(len(robots.current.master._write_buffer))
    #监控画面显示为离线图片
    def update_ui_camera_offline(self):        
        self.label_camera.setPixmap(QPixmap(":/main_window/img/camera.jpeg"))
        pass

    #加载地图
    def load_map(self):
        
        self.svgWidget = QtSvg.QSvgWidget()       
        
        self.scrollArea_map.setWidget(self.svgWidget)
        self.hbox = QHBoxLayout()
        #hbox.addStretch(1)
        self.hbox.addWidget(self.svgWidget)

        #self.svgWidget.resize( QSize(800,600)) #固定大小，有滚动条
        self.scrollArea_map.setLayout(self.hbox) #自适应大小，无滚动条

        self.svgWidget.load(svg_map.doc.toByteArray())

        self.svgWidget.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
        

    #更新地图
    def update_ui_map(self):
        svg_map.update_robot_pos(robots.current.position.path_pos,reverse=True)
        self.svgWidget.load(svg_map.doc.toByteArray())

    #故障信息：当前故障、历史故障切换
    def toggle_table_error_list(self):
        if self.radioButton_err_active.isChecked():
            err_list = robots.current.error_chassis.active_err_info()
        else:
            err_list = robots.current.error_chassis.history_err_info()
        table_fill_data_list_2d(self.tableWidget_error,err_list)
    
       

    
    def init_ui_task_plan(self):
        """初始化计划任务ui."""
        self.dateEdit_task_cycle_start_time.setDate(QDate.currentDate())
        self.dateEdit_task_cycle_end_time.setDate(QDate.currentDate())
        self.dateEdit_task_once_date.setDate(QDate.currentDate())
        self.dateEdit_task_ignore_start_time.setDate(QDate.currentDate())
        self.dateEdit_task_ignore_end_time.setDate(QDate.currentDate())

    
    def set_new_task_plan(self):
        """新建计划任务."""

        task_plans.new_plan.name=self.lineEdit_add_task_name.text()

        if self.comboBox_add_plan_type.currentIndex() is PlanType.Cycle.value:
            task_plans.new_plan.plan_type=PlanType.Cycle

            task_plans.new_plan.start_date=self.dateEdit_task_cycle_start_time.date()
            if self.radioButton_task_cycle_stop_time.isChecked():
                task_plans.new_plan.end_date=self.dateEdit_task_cycle_end_time.date()
            else:
                task_plans.new_plan.end_date=QDate()

            if self.comboBox_task_cycle_type.currentIndex() is CycleType.Nday.value:
                task_plans.new_plan.cycle_type=CycleType.Nday
                task_plans.new_plan.cycle_value=self.spinBox_task_cycle_n_day.value()
                task_plans.new_plan.do_time=self.timeEdit_task_do_time_n_day.time()
                
            elif self.comboBox_task_cycle_type.currentIndex() is CycleType.Weekday.value:
                task_plans.new_plan.cycle_type=CycleType.Weekday
                task_plans.new_plan.cycle_value=self.comboBox_task_cycle_weekday.currentIndex()+1
                task_plans.new_plan.do_time=self.timeEdit_task_do_time_weekday.time()

            elif self.comboBox_task_cycle_type.currentIndex() is CycleType.Monthday.value:
                task_plans.new_plan.cycle_type=CycleType.Monthday
                task_plans.new_plan.cycle_value=self.spinBox_task_cycle_monthday.value()
                task_plans.new_plan.do_time=self.timeEdit_task_do_time_monthday.time()

            else:
                pass            

        elif self.comboBox_add_plan_type.currentIndex() is PlanType.Once.value:
            task_plans.new_plan.plan_type=PlanType.Once
            task_plans.new_plan.start_date=self.dateEdit_task_once_date.date()
            task_plans.new_plan.do_time=self.timeEdit_task_once_time.time()

        elif self.comboBox_add_plan_type.currentIndex() is PlanType.Ignore.value:
            task_plans.new_plan.plan_type=PlanType.Ignore
            task_plans.new_plan.start_date=self.dateEdit_task_ignore_start_time.date()
            task_plans.new_plan.end_date=self.dateEdit_task_ignore_end_time.date()

        else:
            pass
 
    def preview_task_plan(self,task_plan):
        """任务预览."""
        
        nl = '\n'
        self.textBrowser_task_plan_preview.setText(f'任务ID： {task_plan.id}{nl}{nl}任务名称： {task_plan.name}{nl}{nl}任务执行时间：{nl}{task_plan.plan_time_str()}')
        mark_calendar_plan_date(self.calendarWidget_task_preview,task_plan)

    
    def preview_new_task_plan(self):
        """预览新增任务."""
        self.set_new_task_plan()
        self.preview_task_plan(task_plans.new_plan)

    #多线程函数##############################################################################################
    def get_camera_frame(self):
        while True:
            if robots.current == None:
                self.camera_offlined.emit()
            else:
                if robots.current.master.is_opened():
                    robots.current.camera.get_frame()
                else:
                    self.camera_offlined.emit() 


    #多线程管理##############################################################################################
    def thread_manage(self):
        self.thread_get_camera_frame = threading.Thread(target=self.get_camera_frame, name='get_camera_frame')
        self.thread_get_camera_frame.setDaemon(True)
        self.thread_get_camera_frame.start()

    