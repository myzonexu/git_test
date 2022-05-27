# -*- coding: utf-8 -*-
import sys
import os
import copy
from PyQt5.Qt import QMainWindow
#from PyQt5.QtGui import QImage,QPixmap
#from PyQt5.QtWebEngineWidgets import *
#from PyQt5.QtCore import QTimer
#from PyQt5.QtCore import pyqtSlot
import threading
import json

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QObject , pyqtSignal

from PyQt5.QtXml import QDomDocument
from PyQt5 import QtSvg
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, Close
from svg.path import parse_path

from ui_main import Ui_MainWindow
from dialog_select_robot import *
from dialog_about import *

#from func_main import *
from func_task import *
from func_robot import *
from func_svg import *
from func_export import *
from func_defines import *
from func_map import *

class Window(QMainWindow, Ui_MainWindow):
    camera_offlined = pyqtSignal()
    #初始化###################################################################################################
    def __init__(self):
        super().__init__()
        self.setupUi(self)
       

    def func_list(self):
        self.init_file_dirs()
        self.setup_ui_extra()
        self.init_robot_slot()
        self.load_map()
        #self.refresh_ui_timer()
        self.thread_manage()
        


        #self.ui_set_shortcut()
        #self.setup_timer()

        #self.browser = QWebEngineView()
        #self.scrollArea_camera_browser.setWidget(self.browser)
        #self.browser.load(QUrl('http://192.168.0.64/'))
        
        #self.scrollArea_camera_browser.show()

 
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
        
    @pyqtSlot()
    def on_pushButton_autorun_stop_clicked(self):
        robots.current.clean_task_stop()
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
            pass
        else:
            robots.current.errors.clear_history()
    #机器人列表选择
    @pyqtSlot(int,int)
    def on_tableWidget_robot_list_cellClicked(self, row, col):
        #id = int(self.tableWidget_robot_list.item(row,0).text())
        id = self.tableWidget_robot_list.item(row,0).text()
        #选择ID
        if col == 0:            
            robots.set_current(id)
        #选择故障
        elif col == 6:
            robots.set_current(id)
            self.tabWidget_robots_info.setCurrentIndex(0)
        #选择警告
        elif col == 7:
            robots.set_current(id)
            self.tabWidget_robots_info.setCurrentIndex(1)

    @pyqtSlot(int)
    def on_tabWidget_main_currentChanged(self,index):
        #控制
        if index == 0:
            if robots.current:
                robots.current.camera.enable_capture()
            pass
        #机器人
        elif index == 1:
            self.refresh_robots_list()
            pass
        #监控
        elif index == 2:
            if robots.current:
                self.setup_ui_camera_web()
            pass
        #计划任务
        elif index == 3:
            #刷新任务
            self.refresh_task_plan()
            pass
        #日志
        elif index == 4:
            #刷新日志
            self.refresh_clean_log()
            pass
        else:
            robots.current.camera.disable_capture()
            #robots.current.camera.close()
            print("关闭相机捕获")

    @pyqtSlot(int)
    def on_tabWidget_robo_ctrl_currentChanged(self,index):
        """机器人控制方式tab页切换."""
        #轨道行走
        if index == 0:
            
            pass
        #自由行走
        elif index == 1:
            QMessageBox.warning(self,'警告','当机器人与轨道连接时慎用，可能导致机器人与轨道卡死或其他意外！\n仅限自由场地或特殊情况下使用！',QMessageBox.Ok)
            pass
        #机械臂
        elif index == 2:

            pass

        else:
            pass



    @pyqtSlot()
    def on_pushButton_add_task_preview_clicked(self):
        """预览新增计划任务."""
        task_plans.new.check_state=True
        self.preview_new_task_plan()
            
    @pyqtSlot()
    def on_pushButton_add_task_clicked(self):
        """添加新增计划任务."""
        self.set_new_task_plan()
        if task_plans.new.name == "":
            QMessageBox.information(self,'提示','计划任务名称不能为空!请填写。',QMessageBox.Ok)
        else:
            task_plans.new.init_id()
            task_plans.new.enable=True
            task_plans.new.assign=task_plans.new.assign | set(list(robots.all.keys()))
            self.preview_task_plan(task_plans.new)        
            task_plans.new.add_time=datetime.now()
            #task_plans.new.add_time=QDateTime.currentDateTime()

            task_plans.all[str(task_plans.new.id)]=copy.deepcopy(task_plans.new)
         
            self.refresh_task_plan()
            
            #清空新任务信息
            self.lineEdit_add_task_name.setText("")
            task_plans.new.__init__()
            self.preview_task_plan(task_plans.new)

    
    #计划任务列表选择
    @pyqtSlot(int,int)
    def on_tableWidget_task_plan_list_cellClicked(self, row, col):
        id = int(self.tableWidget_task_plan_list.item(row,0).text())
       
    
    #计划任务机器人选择
    @pyqtSlot(int,int)
    def on_tableWidget_task_plan_list_cellDoubleClicked(self, row, col):
        id = int(self.tableWidget_task_plan_list.item(row,0).text())
        if col==4:
            self.dialog_select_robot=Dialog()
            self.dialog_select_robot.show() 

    @pyqtSlot(int)
    def on_checkBox_select_task_plan_all_stateChanged(self,state):
        """全选，全不选计划."""
        set_table_check_state(self.tableWidget_task_plan_list,state)

    @pyqtSlot()
    def on_pushButton_del_plan_clicked(self):
        """删除所选计划."""
        self.get_plan_check_state()
        task_plans.del_checked()
        self.refresh_task_plan()
        self.checkBox_select_task_plan_all.setCheckState(Qt.Unchecked)

    @pyqtSlot()
    def on_pushButton_enable_plans_checked_clicked(self):
        """开启所选计划."""
        self.get_plan_check_state()
        task_plans.enable_checked(True)
        self.refresh_task_plan()
        self.checkBox_select_task_plan_all.setCheckState(Qt.Unchecked)

    @pyqtSlot()
    def on_pushButton_disable_plans_checked_clicked(self):
        """关闭所选计划."""
        self.get_plan_check_state()
        task_plans.enable_checked(False)        
        self.refresh_task_plan()
        self.checkBox_select_task_plan_all.setCheckState(Qt.Unchecked)
    @pyqtSlot()
    def on_pushButton_preview_plans_checked_clicked(self):
        """预览所选计划."""
        task_plans.new.check_state=False
        self.get_plan_check_state()
        self.preview_task_plans()
        #self.refresh_task_plan()
        #self.checkBox_select_task_plan_all.setCheckState(Qt.Unchecked)
    @pyqtSlot(int,int)
    def on_calendarWidget_task_preview_currentPageChanged(self,year,month):
        """日历翻页预览所选计划."""
        if task_plans.new.check_state is True:
            self.preview_new_task_plan()
        else:
            self.get_plan_check_state()
            self.preview_task_plans()


    @pyqtSlot()
    def on_pushButton_send_task_plan_clicked(self):
        """计划任务下发."""
        robots.current.task_plans=set()
        for plan_id,item in task_plans.all.items():            
            for robot_id in item.assign:                
                robots.current.task_plans.add(item.id)
                item.received.add(robot_id)

                self.refresh_task_plan()
        #print(robots.current.task_plans)


        #下发当前机器人
        robots.current.send_plan()
        
       

    @pyqtSlot()
    def on_pushButton_add_robot_clicked(self):
        """添加机器人."""
        _str_id=self.lineEdit_add_robot_id.text()
        _robot=Robot(ip=self.lineEdit_add_robot_ip.text(),camera_ip=self.lineEdit_add_camera_ip.text())
        _robot.id=int(_str_id)
        robots.all[_str_id]=_robot
        if robots.current is None:
            robots.init_current(_str_id)

        self.refresh_robots_list()
    @pyqtSlot(int)
    def on_checkBox_robot_all_stateChanged(self,state):
        """全选，全不选机器人."""
        set_table_check_state(self.tableWidget_robot_all,state)

    @pyqtSlot()
    def on_pushButton_del_robot_clicked(self):
        """删除所选机器人."""
        for row in range(self.tableWidget_robot_all.rowCount()):
            if self.tableWidget_robot_all.item(row,0).checkState() == Qt.Checked:
                robots.all.pop(self.tableWidget_robot_all.item(row,0).text())
        self.refresh_robots_list()
        self.checkBox_robot_all.setCheckState(Qt.Unchecked)
        #self.save_robots_data()
        self.update_ui()

    @pyqtSlot()
    def on_pushButton_log_refresh_clicked(self):
        """刷新清扫日志."""
        self.refresh_clean_log()

    @pyqtSlot()
    def on_pushButton_export_log_clicked(self):
        """导出清扫日志."""
        rows=self.refresh_clean_log()
        header=["机器人ID","任务ID","开始时间","结束时间","行驶里程","清扫数量","加水次数","充电次数"]
        _file_name=datetime.now().strftime(TIME_SHOW_Y_M_D)
        _file = QFileDialog.getSaveFileName(self, '保存文件',f'./清扫记录_{_file_name}.csv')
        if _file[0]!="":
            export_csv(_file[0],header,rows)

    @pyqtSlot()
    def on_pushButton_del_clean_log_clicked(self):
        """删除清扫日志."""
        for row in range(self.tableWidget_log_all.rowCount()):
            if self.tableWidget_log_all.item(row,0).checkState() == Qt.Checked:
                _robot_id=self.tableWidget_log_all.item(row,0).text()
                _log_id=self.tableWidget_log_all.item(row,1).text()
                #print(_robot_id,_log_id)
                robots.all.get(_robot_id).clean_log.all.pop(_log_id)
                
        self.refresh_clean_log()
        self.checkBox_log.setCheckState(Qt.Unchecked)

    @pyqtSlot()
    def on_actionabout_triggered(self):
        """关于."""
        print("about")
        self.dialog_about=DialogAbout()
        self.dialog_about.show()


    #@pyqtSlot()
    #def on_pushButton_export_plan_clicked(self):
    #    """导出计划任务."""
    #    self.save_task_plans_data()
        
    #@pyqtSlot()
    #def on_pushButton_import_plan_clicked(self):
    #    """导入计划任务."""
    #    task_plans.import_json_file('./data/task_plans.json')
    #    #with open('./data/task_plans.json', 'r') as f:
    #    #    task_plans.import_json(json.load(f))
    #    #    #json.load(f,object_hook=task_plans.import_json)
    #    self.refresh_task_plan()
    
    #@pyqtSlot()
    #def on_pushButton_export_robot_clicked(self):
    #    """导出机器人."""
    #    self.save_robots_data()

    @pyqtSlot()
    def on_pushButton_import_robot_clicked(self):
        """导入机器人."""

        with open('./data/robots.json', 'r') as f:
            json_dict=json.load(f)
            print(json_dict)
            json_dict_to_obj(json_dict,robot2)
            #json_to_obj(json_dict,robots.all)
            print(robot2.__dict__)

    #方法######################################################################################
    #UI额外设置
    def setup_ui_extra(self):
        self.init_table_group()
        self.init_ui_task_plan()
        self.setup_ui_tablewidget()
        #self.setup_ui_statusbar()
        self.setup_ui_shortcut()
        #self.camera_offlined.connect(self.update_ui_camera_offline)
        self.table_task_plan_is_checkable=False
        
        
        

    #初始化当前机器人信号槽
    def init_robot_slot(self):
        robots.current_inited.connect(self.setup_ui_robot_current_slot)
        robots.current_changed.connect(self.setup_ui_robot_current_slot)

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
                                        self.tableWidget_error ,
                                        self.tableWidget_task_plan_list,self.tableWidget_robot_all,self.tableWidget_log_all ]
    def setup_ui_tablewidget(self):
        for table_widget in self.tableWidget_group_show:
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table_widget.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)

        for i in range(0,4):
            self.tableWidget_robot_list.horizontalHeader().setSectionResizeMode(i,QHeaderView.ResizeToContents)

        for j in range(0,3):
            self.tableWidget_error.horizontalHeader().setSectionResizeMode(j,QHeaderView.ResizeToContents)

        for j in [0,1,2,3,4,7,9]:
            self.tableWidget_task_plan_list.horizontalHeader().setSectionResizeMode(j,QHeaderView.ResizeToContents)
        #for j in range(0,2):
        #    self.tableWidget_robot_all.horizontalHeader().setSectionResizeMode(j,QHeaderView.ResizeToContents)
        #for j in range(0,2):
        #    self.tableWidget_log_all.horizontalHeader().setSectionResizeMode(j,QHeaderView.ResizeToContents)


    #UI更新
    def update_ui(self):
        self.update_ui_widget_enbaled()
        self.update_ui_table()
        self.update_ui_tab_text()
        self.update_ui_map()
        self.refresh_robots_list()
        self.save_robots_data()
               

    #更新表格显示
    def update_ui_table(self):
        table_fill_data_list_2d(self.tableWidget_robot_list,robots.list_info())  
        #table_fill_data_list_2d(self.tableWidget_robot_all,robots.list_info(),checkable=True)
        if robots.current == None:
            pass
        else:
            table_fill_data_list_2d(self.tableWidget_robot_info,robots.current.robot_info())
            table_fill_data_list_2d(self.tableWidget_task_info,robots.current.task_info())
        
            self.toggle_table_error_list()

    #更新tab页文字
    def update_ui_tab_text(self):
        self.tabWidget_robots_info.setTabText(1,f"机器人列表({str(len(robots.all))})")
        if robots.current == None:
            pass
        else:
            #self.tabWidget_robots_info.setTabText(0,"故障(" + str(robots.current.err_count()) + ")")
            #self.tabWidget_robots_info.setTabText(1,"警告(" + str(robots.current.warning_count()) + ")")
            self.tabWidget_robots_info.setTabText(0,f"故障({str(robots.current.errors.active_count)})")
            #self.tabWidget_robots_info.setTabText(1,f"警告({str(robots.current.warnings.active_count)})")
             
    #更新控件使能
    def update_ui_widget_enbaled(self):
        #if master.is_opened() and master.is_reconnect()==False :
        #self.tabWidget_main.setTabEnabled(3,False)
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
        print("打开监控web页面")

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
        #self.svgWidget.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
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

        #更新已清理标志
        path_1.clean_points.set_cleaned(robots.current.task.tracks)
        print(path_1.clean_points.array_cleaned)
        print(path_1.clean_points.count_cleaned)

    #故障信息：当前故障、历史故障切换
    def toggle_table_error_list(self):
        if self.radioButton_err_active.isChecked():
            err_list = robots.current.errors.active_err_info
        else:
            err_list = robots.current.errors.history_err_info
        table_fill_data_list_2d(self.tableWidget_error,err_list)       

    
    def init_ui_task_plan(self):
        """初始化计划任务ui."""
        self.dateEdit_task_cycle_start_time.setDate(QDate.currentDate())
        self.dateEdit_task_cycle_end_time.setDate(QDate.currentDate())
        self.dateEdit_task_once_date.setDate(QDate.currentDate())
        self.dateEdit_task_ignore_start_time.setDate(QDate.currentDate())
        self.dateEdit_task_ignore_end_time.setDate(QDate.currentDate())

        #task_plans.import_json_file('./data/task_plans.json')
        self.refresh_task_plan()

    
    def set_new_task_plan(self):
        """新建计划任务."""

        task_plans.new.name=self.lineEdit_add_task_name.text()

        if self.comboBox_add_plan_type.currentIndex() is PlanType.Cycle.value:
            task_plans.new.plan_type=PlanType.Cycle

            task_plans.new.start_date=self.dateEdit_task_cycle_start_time.date()
            if self.radioButton_task_cycle_stop_time.isChecked():
                task_plans.new.end_date=self.dateEdit_task_cycle_end_time.date()
            else:
                task_plans.new.end_date=QDate()

            if self.comboBox_task_cycle_type.currentIndex() is CycleType.Nday.value:
                task_plans.new.cycle_type=CycleType.Nday
                task_plans.new.cycle_value=self.spinBox_task_cycle_n_day.value()
                task_plans.new.do_time=self.timeEdit_task_do_time_n_day.time()
                
            elif self.comboBox_task_cycle_type.currentIndex() is CycleType.Weekday.value:
                task_plans.new.cycle_type=CycleType.Weekday
                task_plans.new.cycle_value=self.comboBox_task_cycle_weekday.currentIndex()+1
                task_plans.new.do_time=self.timeEdit_task_do_time_weekday.time()

            elif self.comboBox_task_cycle_type.currentIndex() is CycleType.Monthday.value:
                task_plans.new.cycle_type=CycleType.Monthday
                task_plans.new.cycle_value=self.spinBox_task_cycle_monthday.value()
                task_plans.new.do_time=self.timeEdit_task_do_time_monthday.time()

            else:
                pass            

        elif self.comboBox_add_plan_type.currentIndex() is PlanType.Once.value:
            task_plans.new.plan_type=PlanType.Once
            task_plans.new.start_date=self.dateEdit_task_once_date.date()
            task_plans.new.do_time=self.timeEdit_task_once_time.time()

        elif self.comboBox_add_plan_type.currentIndex() is PlanType.Ignore.value:
            task_plans.new.plan_type=PlanType.Ignore
            task_plans.new.start_date=self.dateEdit_task_ignore_start_time.date()
            task_plans.new.end_date=self.dateEdit_task_ignore_end_time.date()

        else:
            pass
 
    def preview_task_plan(self,task_plan):
        """预览单个任务."""
        
        nl = '\n'
        #self.textBrowser_task_plan_preview.setText(f'任务ID： {task_plan.id}{nl}{nl}任务名称： {task_plan.name}{nl}{nl}任务执行时间：{nl}{task_plan.plan_time_str()}')
        self.textBrowser_task_plan_preview.setText(f'任务名称： {task_plan.name}{nl}{nl}任务执行时间：{nl}{task_plan.plan_time_str()}')
        mark_calendar_plan_date(self.calendarWidget_task_preview,task_plan)
        #task_plan.get_message_frame()

    def preview_task_plans(self):
        """预览选中的多个任务."""
        ids=[]
        names=[]
        
        nl = '\n'
        for id,item in task_plans.all.items():
            if item.check_state is True:
                ids.append(id)
                names.append(item.name)
        self.textBrowser_task_plan_preview.setText(f'任务ID： {all_list_str(ids)}{nl}{nl}任务名称： {all_list_str(names)}')
        mark_calendar_plans_date(self.calendarWidget_task_preview,task_plans.all)
   
    def preview_new_task_plan(self):
        """预览新增任务."""
        self.set_new_task_plan()
        self.preview_task_plan(task_plans.new)

    def get_plan_check_state(self):
        """获取计划任务选中状态."""
        for row in range(self.tableWidget_task_plan_list.rowCount()):
            check_state=self.tableWidget_task_plan_list.item(row,0).checkState()
            #id=int(self.tableWidget_task_plan_list.item(row,0).text())
            id=self.tableWidget_task_plan_list.item(row,0).text()
            if check_state == Qt.Checked:
                task_plans.all.get(id).check_state=True
            elif check_state == Qt.Unchecked:
                task_plans.all.get(id).check_state=False
            else:
                pass
    def refresh_clean_log(self):
        """刷新清扫日志."""
        clean_infos=[]
        for id,item in robots.all.items():
            clean_info=item.clean_log.list_info()            
            for info in clean_info:
                info.insert(0,str(id))
                clean_infos.append(info)
                
        table_fill_data_list_2d(self.tableWidget_log_all,clean_infos,checkable=True)
        return clean_infos

    
    def refresh_task_plan(self):
        """刷新任务表格."""
        for _task in task_plans.all.values():
            _task.assign=set(list(robots.all.keys()))
        table_fill_data_list_2d(self.tableWidget_task_plan_list,task_plans.list_info(),checkable=True)
        self.save_task_plans_data()
    
    def refresh_robots_list(self):
        """
        刷新机器人列表表格.
    
        :returns: no return
        :raises: no exception
        """
        for row in range(self.tableWidget_robot_all.rowCount()):
            _id_item=self.tableWidget_robot_all.item(row,0)
            _rob=robots.all.get(_id_item.text())
            if _rob is None:
                pass
            else:
                if _id_item.checkState() == Qt.Checked:
                    robots.all.get(_id_item.text()).is_checked=True
                    #_rob=robots.all.get(tmp)
                    #print(_rob.id,_rob.is_checked)
                else:
                    robots.all.get(_id_item.text()).is_checked=False
             
        table_fill_data_list_2d(self.tableWidget_robot_all,robots.list_info(),checkable=True)

        for row in range(self.tableWidget_robot_all.rowCount()):
            _id_item=self.tableWidget_robot_all.item(row,0)
            _rob=robots.all.get(_id_item.text())
            if _rob is None:
                pass
            else:
                if robots.all.get(_id_item.text()).is_checked is True:
                    _id_item.setCheckState(Qt.Checked)                
                else:
                    _id_item.setCheckState(Qt.Unchecked)
        

    def save_robots_data(self):
        """保存机器人数据."""
        obj_to_json_file('./data/robots.json',robots,robots.dict_trans,"robots")

    def save_task_plans_data(self):
        """保存计划任务数据."""
        obj_to_json_file('./data/task_plans.json',task_plans,task_plans.dict_trans,"task_plans")

    
    def init_file_dirs(self):
        """
        初始化文件目录.
    
        :returns: no return
        :raises: no exception
        """

        dirs = './data'

        if not os.path.exists(dirs):
            os.makedirs(dirs)

    #多线程函数##############################################################################################
    def get_camera_frame(self):
        while True:
            if robots.current == None:
                #%self.camera_offlined.emit()
                self.update_ui_camera_offline()
            else:
                if robots.current.master.is_opened():
                    robots.current.camera.get_frame()
                else:
                    #self.camera_offlined.emit() 
                    self.update_ui_camera_offline
                    pass

    def get_robots_state(self):    
        sec=0
        while True:
            if robots.current==None:
                pass
            else:
                if robots.current.master.is_opened():
                    robots.current.get_robot_time()
                    pass
            for _robot in list(robots.all.values()):
                if _robot.master.is_opened():
                    #print(f"获取状态，ID:{_robot.id}")
                    _robot.get_state() 
            for str_id in list(robots.all.keys()):
                _robot=robots.all.get(str_id)
                if _robot.master.is_opened():
                    _robot.get_state()
                    _id=_robot.id
                    if _id != int(str_id):
                        robots.all[str(_id)]=_robot
                        robots.all.pop(str_id)

                    if sec>60:
                            _robot.sync_time()
                            sec=0
           
            time.sleep(1)
            sec=sec+1

    def scan_robots(self):
        while True:
            for _robot in list(robots.all.values()):
                if _robot.master.is_opened() is False:
                    #print(f"重连，ID:{_robot.id}")
                    #_robot.master.set_timeout(5)
                    _robot.master.read(_robot.protocol.robot_id)
                    if _robot.master.is_opened():
                        #print(f"连接ID：{_robot.id}成功")
                        #_robot.master.set_timeout(1)    
                        pass               
                else:
                    pass
            time.sleep(1)

 

    def send_modbus_write_buffer(self):
        while True:
            #for id in robots.all: 
            #for id in list(robots.all.keys()):
            for _robot in list(robots.all.values()):
                if _robot.master.is_opened():
                    _robot.master.send_write_buffer()

                time.sleep(1)


    #多线程管理##############################################################################################
    def thread_manage(self):
        self.thread_get_camera_frame = threading.Thread(target=self.get_camera_frame, name='get_camera_frame')
        self.thread_get_camera_frame.setDaemon(True)
        self.thread_get_camera_frame.start()

        #self.thread_get_robots_state = threading.Thread(target=self.get_robots_state, name='get_robots_state')
        ##线程：发送modbus写缓存中的数据
        #self.thread_send_modbus_write_buffer = threading.Thread(target=self.send_modbus_write_buffer, name='send_modbus_write_buffer')
        ##线程：扫描局域网机器人
        #self.thread_scan_robots = threading.Thread(target=self.scan_robots, name='scan_robots')

        #self.thread_get_robots_state.setDaemon(True)
        #self.thread_get_robots_state.start()
        #self.thread_send_modbus_write_buffer.setDaemon(True)
        #self.thread_send_modbus_write_buffer.start()
        #self.thread_scan_robots.setDaemon(True)
        #self.thread_scan_robots.start()

    #定时刷新界面定时器
    
    def refresh_ui_timer(self):
        """
        定时器刷新界面.
    
        :returns: no return
        :raises: no exception
        """
        
        self.timer_ui = QTimer(self)  # 初始化一个定时器
        self.timer_ui.timeout.connect(self.update_ui)  # 每次计时到时间时发出信号
        self.timer_ui.start(1000)  # 设置计时间隔并启动；单位毫秒



    