# -*- coding: utf-8 -*-


from PyQt5.Qt import QMainWindow
#from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWebEngineWidgets import *
#from PyQt5.QtCore import QTimer
#from PyQt5.QtCore import pyqtSlot

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtSvg

from ui_main import Ui_MainWindow
#from func_main import *
from func_robot import *



class Window(QMainWindow, Ui_MainWindow):
    #初始化###################################################################################################
    def __init__(self):
        super().__init__()
        self.setupUi(self)
       

    def func_list(self):
        self.setup_ui_extra()
        self.load_map()
        #self.ui_set_shortcut()
        self.setup_timer()
 
    #事件响应###################################################################################################
    #窗口大小改变响应
    def resizeEvent(self, QResizeEvent):
        #Window resize event.
        super().resizeEvent(QResizeEvent)
        if robots.current==None:
            pass
        else:
            camera_ratio=robots.current.camera.ratio_w_h
            camrea_show_height=self.groupBox_map.height()
            camrea_show_width=int(camrea_show_height*camera_ratio)
            offset_width=camrea_show_width-self.label_camera.width()
            self.groupBox_map.resize(self.groupBox_map.width()-offset_width,self.groupBox_map.height())
            self.label_camera.move(self.label_camera.x()-offset_width,self.label_camera.y())
            self.label_camera.resize(camrea_show_width,camrea_show_height)


    #信号-槽响应###############################################################################################
    #按钮响应
    @pyqtSlot()
    def on_pushButton_autorun_start_clicked(self):
        robots.current.clean_task_start()
        robots.current.task.start_time=datetime.now()
        robots.current.task.stop_time=None
    @pyqtSlot()
    def on_pushButton_autorun_stop_clicked(self):
        robots.current.clean_task_stop()
        robots.current.task.stop_time=datetime.now()
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
    #test
    @pyqtSlot()
    def on_pushButton_add_task_clicked(self):
        print("按下添加")
    @pyqtSlot()
    def xxx(self):
        pass
    @pyqtSlot()
    def xxx(self):
        pass

    #方法######################################################################################
    #UI额外设置
    def setup_ui_extra(self):
        self.init_table_group()
        self.setup_ui_tablewidget()
        self.ui_set_shortcut()
        pass
    #设置快捷键
    def ui_set_shortcut(self):
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
        self.tableWidget_group_show=[self.tableWidget_robot_list,self.tableWidget_robot_info,self.tableWidget_task_info ,
                                        self.tableWidget_error ,self.tableWidget_warning,self.tableWidget_log_info ,
                                        self.tableWidget_task_list ,self.tableWidget_task_log ]
    def setup_ui_tablewidget(self):
        for table_widget in self.tableWidget_group_show:
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table_widget.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)

        for i in range(0,4):
            self.tableWidget_robot_list.horizontalHeader().setSectionResizeMode(i,QHeaderView.ResizeToContents)

        for j in range(0,4):
            self.tableWidget_error.horizontalHeader().setSectionResizeMode(j,QHeaderView.ResizeToContents)


    #UI更新
    def update_ui(self):
        self.update_ui_table()
        self.update_ui_tab_text()

    #更新表格显示
    def update_ui_table(self):
        table_fill_data_list_2d(self.tableWidget_robot_list,robots.list_info())      
        if robots.current == None:
            pass
        else:
            table_fill_data_list_2d(self.tableWidget_robot_info,robots.current.robot_info())
            table_fill_data_list_2d(self.tableWidget_task_info,robots.current.task_info())
        

            if self.radioButton_err_active.isChecked():
                err_list=robots.current.error_chassis.active_err_info()
            else:
                err_list=robots.current.error_chassis.history_err_info()
            table_fill_data_list_2d(self.tableWidget_error,err_list)

    #更新tab页文字
    def update_ui_tab_text(self):
        self.tabWidget_robots_info.setTabText(3,"机器人列表("+str(len(robots.robots))+")")
        if robots.current==None:
            pass
        else:
            self.tabWidget_robots_info.setTabText(0,"故障信息("+str(robots.current.err_count())+")")
            self.tabWidget_robots_info.setTabText(1,"警告信息("+str(robots.current.warning_count())+")")
        

               
    #更新控件使能
    def update_ui_widget_enbaled(self):
        #if master.is_opened() and master.is_reconnect()==False :
        if robots.current.master.is_opened() :
            self.tabWidget_robo_ctrl.setEnabled(True)
        else:
            self.tabWidget_robo_ctrl.setEnabled(False)

        #self.tab.setTabEnabled

    #显示监控视频
    def show_camera(self):
        if robots.current==None:
            pass
        else:
            self.label_camera.setPixmap(QPixmap.fromImage(robots.current.camera.img_scaled))


    #加载地图
    def load_map(self):
        self.svgWidget = QtSvg.QSvgWidget('map.svg')
        self.scrollArea_map.setWidget(self.svgWidget)

    #显示SVG地图
    x=0
    def show_map(self):
        render=self.svgWidget.renderer()
        global x
        x=x+1
        render.setViewBox(QRect(x,10,100,80))
        self.scrollArea_map.repaint()
        #render.repaintNeeded.connect(window.scrollArea_map.repaint)
    

    

 
        
   
    #故障信息：当前故障、历史故障切换
    def toggle_table_error_list(self):
        if self.radioButton_err_active.isChecked():
            err_list=robots.current.error_chassis.active_err_info()
        else:
            err_list=robots.current.error_chassis.history_err_info()
        table_fill_data_list_2d(self.tableWidget_error,err_list)
        
    
    
            
    

    #定时器
    def setup_timer(self):
        self.timer_ui_refresh = QTimer(self)  # 初始化一个定时器
        self.timer_ui_refresh.timeout.connect(self.update_ui)  # 每次计时到时间时发出信号
        self.timer_ui_refresh.start(1000)  # 设置计时间隔并启动；单位毫秒
        self.timer_camera = QTimer()
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_camera.start(30)  # 设置计时间隔并启动；单位毫秒

        self.timer_test = QTimer()
        #self.timer_test.timeout.connect(lambda:self.progressBar.setValue(len(robots.current.master._write_buffer)))  # 每次计时到时间时发出信号
        self.timer_test.start(30)  # 设置计时间隔并启动；单位毫秒

        
    
    #重连网络——改用线程
    #刷新界面——改用信号
    #视频显示——改用线程
    
