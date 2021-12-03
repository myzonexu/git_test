import time
from func_modbus_tcp import *
from PyQt5.QtCore import QTimer

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from PyQt5 import QtSvg
import threading
from func_camera import *

###################################################################################################
def do_main_ui(window,master,camera):
    load_map(window)
    #设置快捷键
    #ui_set_shortcut(window)
    #按钮响应
    do_push_button(window,master,camera)
    
    #定时自动掉线重连网络
    window.timer2 = QTimer(window)  # 初始化一个定时器
    window.timer2.timeout.connect(lambda:do_reconnect_modbus(window,master,camera))  # 每次计时到时间时发出信号
    window.timer2.start(5000)

    #定时刷新界面改用线程，不再使用定时器
    #window.timer3 = QTimer(window)  # 初始化一个定时器
    #window.timer3.timeout.connect(lambda:do_ui_refresh(window,master))  # 每次计时到时间时发出信号
    #window.timer3.start(1000)  # 设置计时间隔并启动；单位毫秒
    
    #相机预览改用线程，不再使用定时器
    #window.timer_camera = QTimer(window)
    #window.timer_camera.timeout.connect(lambda:do_show_camera(window,master,camera))  # 每次计时到时间时发出信号
    #window.timer_camera.start(40)  # 设置计时间隔并启动；单位毫秒  

    window.timer_camera = QTimer(window)
    window.timer_camera.timeout.connect(lambda:window.label_camera.setPixmap(QPixmap.fromImage(camera.img)))  # 每次计时到时间时发出信号
    window.timer_camera.start(30)  # 设置计时间隔并启动；单位毫秒 
    
    return
###################################################################################################

#设置快捷键
def ui_set_shortcut(window):
    #window.pushButton_drive_forward.setShortcut('Ctrl + Up')
    window.pushButton_drive_forward.setShortcut('Up')
    window.pushButton_drive_backward.setShortcut('Down')
    window.pushButton_turn_left.setShortcut('Left')
    window.pushButton_turn_right.setShortcut('Right')
    window.pushButton_drive_pause.setShortcut('Space')
    window.pushButton_autorun_start.setShortcut('Home')
    window.pushButton_autorun_stop.setShortcut('End')

    window.pushButton_arm_position_origin.setShortcut('0')
    window.pushButton_arm_position_wall_1.setShortcut('1')
    window.pushButton_arm_position_wall_2.setShortcut('2')
    window.pushButton_arm_position_wall_3.setShortcut('3')
    window.pushButton_arm_position_wall_4.setShortcut('4')
    window.pushButton_arm_position_ground_1.setShortcut('5')

#按钮响应####################################################################################
def do_push_button(window,master,camera):
    window.pushButton_autorun_start.clicked.connect(lambda:do_btn_autorun_start(master))
    window.pushButton_autorun_stop.clicked.connect(lambda:do_btn_autorun_stop(master))
    window.pushButton_autorun_charge.clicked.connect(lambda:do_btn_autorun_charge(master))
    window.pushButton_autorun_add_water.clicked.connect(lambda:do_btn_autorun_add_water(master))

    #window.pushButton_drive_forward.pressed.connect(lambda:do_btn_drive_forward(master))
    #window.pushButton_drive_forward.released.connect(lambda:do_btn_drive_forward_straight(master))
    #window.pushButton_drive_backward.pressed.connect(lambda:do_btn_drive_backward(master))
    #window.pushButton_drive_backward.released.connect(lambda:do_btn_drive_backward_straight(master))
    #window.pushButton_drive_pause.clicked.connect(lambda:do_btn_drive_pause(master))
    #window.pushButton_turn_left.clicked.connect(lambda:do_btn_turn_left(master))
    #window.pushButton_turn_right.clicked.connect(lambda:do_btn_turn_right(master))

    window.pushButton_arm_position_origin.clicked.connect(lambda:do_btn_arm_position_origin(master))
    window.pushButton_arm_position_wall_1.clicked.connect(lambda:do_btn_arm_position_wall_1(master))
    window.pushButton_arm_position_wall_2.clicked.connect(lambda:do_btn_arm_position_wall_2(master))
    window.pushButton_arm_position_wall_3.clicked.connect(lambda:do_btn_arm_position_wall_3(master))
    window.pushButton_arm_position_wall_4.clicked.connect(lambda:do_btn_arm_position_wall_4(master))
    window.pushButton_arm_position_ground_1.clicked.connect(lambda:do_btn_arm_position_ground_1(master))
    window.pushButton_work_clean.clicked.connect(lambda:do_btn_work_clean(window,master))
    window.pushButton_arm_power_restart.clicked.connect(lambda:do_btn_arm_power_restart(window,master))

    window.pushButton_tcp_connect.clicked.connect(lambda:do_btn_tcp_connect(window,master,camera))
    #window.pushButton_tcp_connect.clicked.connect(thread_modbus.start)
    window.pushButton_tcp_disconnect.clicked.connect(lambda:do_btn_tcp_disconnect(window,master))

    window.spinBox_robo_speed.valueChanged.connect(lambda:do_spinBox_robo_speed(window,master))
    window.pushButton_robo_speed_zero.clicked.connect(lambda:do_btn_robo_speed_zero(window,master))
    window.spinBox_steer_angle.valueChanged.connect(lambda:do_spinBox_steer_angle(window,master))
    window.pushButton_steer_angle_zero.clicked.connect(lambda:do_btn_steer_angle_zero(window,master))
    window.pushButton_chassis_power_restart.clicked.connect(lambda:do_btn_chassis_power_restart(window,master))
    window.pushButton_drive_track_forward.clicked.connect(lambda:do_btn_drive_track_forward(window,master))
    window.pushButton_drive_track_backward.clicked.connect(lambda:do_btn_drive_track_backward(window,master))

    return

#沿轨道前进
def do_btn_drive_track_forward(window,master):
    master.write(ctrl_mode,1)
    master.write(drive_ctrl,1)
#沿轨道后退
def do_btn_drive_track_backward(window,master):
    master.write(ctrl_mode,1)
    master.write(drive_ctrl,2)
#底盘重新上电
def do_btn_chassis_power_restart(window,master):
    master.write(chassis_set,7)
#机械臂重新上电
def do_btn_arm_power_restart(window,master):
    master.write(chassis_set,6)

#手动控制速度
def do_spinBox_robo_speed(window,master):
    #控制模式-手动
    master.write(ctrl_mode,1)
    #手动模式-取消暂停
    master.write(drive_ctrl,0)
    #手动模式下速度输入
    master.write(robo_speed_set,window.spinBox_robo_speed.value())

#手动控制暂停
def do_btn_robo_speed_zero(window,master):
    window.spinBox_robo_speed.setValue(0)
    master.write(ctrl_mode,1)
    master.write(drive_ctrl,0)
    #手动模式下速度输入
    master.write(robo_speed_set,0)

#手动控制转角
def do_spinBox_steer_angle(window,master):
    #控制模式-手动
    master.write(ctrl_mode,1)
    #手动模式下转角输入
    master.write(steer_angle_set,window.spinBox_steer_angle.value())

#手动控制转向回正
def do_btn_steer_angle_zero(window,master):
    window.spinBox_steer_angle.setValue(0)
    master.write(ctrl_mode,1)
    master.write(drive_ctrl,0)
    #手动模式下转角输入
    master.write(steer_angle_set,0)

#带切换功能按键响应
def do_toggle_widget(widget,up_text,up_func,down_text,down_func,master,window):
    if widget.isChecked() == True :
        up_func(master,window)
        widget.setText(down_text)
        pass
    elif widget.isChecked() == False :
        down_func(master,window)
        widget.setText(up_text)
        pass
    else :
        pass

#自动任务处理
def do_btn_autorun_start(master):
    if master.is_opened():
        print("自动任务开始")
        #控制模式-自动
        master.write(ctrl_mode,0)
        #清洗任务-开始
        master.write(start_clean,1)
    else:
        pass

def do_btn_autorun_stop(master):
    if master.is_opened():
        print("自动任务结束")
        #控制模式-自动
        master.write(ctrl_mode,0)
        #清洗任务-开始
        master.write(start_clean,0)
    else:
        pass

def do_btn_autorun_charge(master):
    if master.is_opened():
        print("手动任务充电")
        #控制模式-手动
        master.write(ctrl_mode,1)
        #充电
        master.write(work_ctrl,2)
    else:
        pass

def do_btn_autorun_add_water(master):
    if master.is_opened():
        print("手动任务加水")
        #控制模式-手动
        master.write(ctrl_mode,1)
        #充电
        master.write(work_ctrl,3)
    else:
        pass


#机械臂控制处理
#定位初始位置
def do_btn_arm_position_origin(master):
    print("定位初始位置")
    master.write(ctrl_mode,1)
    master.write(arm_ctrl,0)

#定位侧壁-1
def do_btn_arm_position_wall_1(master):
    print("定位侧壁-1")
    #控制模式-手动
    master.write(ctrl_mode,1)
    master.write(arm_ctrl,1)

#定位侧壁-2
def do_btn_arm_position_wall_2(master):
    print("定位侧壁-2")
    master.write(ctrl_mode,1)
    master.write(arm_ctrl,2)

#定位侧壁-3
def do_btn_arm_position_wall_3(master):
    print("定位侧壁-3")
    master.write(ctrl_mode,1)
    master.write(arm_ctrl,3)

#定位侧壁-4
def do_btn_arm_position_wall_4(master):
    print("定位侧壁-4")
    master.write(ctrl_mode,1)
    master.write(arm_ctrl,4)

#定位地面-1
def do_btn_arm_position_ground_1(master):
    print("定位地面-1")
    master.write(ctrl_mode,1)
    master.write(arm_ctrl,5)

#开关滚刷控制功能
def do_btn_work_clean_start(master,window):
    print("开水泵、刷子")
    master.write(ctrl_mode,1)
    master.write(work_ctrl,1)
    
def do_btn_work_clean_stop(master,window):
    print("关水泵、刷子")
    master.write(ctrl_mode,1)
    master.write(work_ctrl,0)

#控制水泵、刷子
def do_btn_work_clean(window,master):
    #带功能切换按键
    do_toggle_widget(window.pushButton_work_clean,"开滚刷",do_btn_work_clean_start,"关滚刷",do_btn_work_clean_stop,master,window)

#连接网络
def do_btn_tcp_connect(window,master,camera):
    try:
        host = window.lineEdit_ip_addr.text()
        master.set_host(host)
        master.set_timeout(MODBUS_TIMEOUT)
        master.open()
        master.no_reconnect()
        connect_info = "连接网络: " + host + " 成功"
        window.label_robo_info.setText("机器人编号："+str(master.read(robo_id))+"    程序版本："+str(master.read(soft_version)))
        #相机web页面
        
        set_camera_browser(camera,window.scrollArea_camera_browser)
    except modbus_tk.modbus.ModbusError as exc:
        print("%s- Code=%d", exc, exc.get_exception_code())
    except modbus_tk.modbus_tcp.socket.error as e:
        connect_info = "连接网络: " + host + " 失败，错误：" + str(e)
    else:
        pass
    finally:
        window.label_connect_info.setText(connect_info)
        print(connect_info)
    return 

#断开网络
def do_btn_tcp_disconnect(window,master):
    try:
        master.close()
        master.no_reconnect()
        connect_info = "网络已断开"
        window.label_robo_info.setText("")
    except modbus_tk.modbus.ModbusError as exc:
        print("%s- Code=%d", exc, exc.get_exception_code())
    except modbus_tk.modbus_tcp.socket.error as e:
        connect_info = "断开网络:+" + host + "失败，错误：" + str(e)
    else:
        pass
    finally:
        window.label_connect_info.setText(connect_info)
        print(connect_info)
    return 
#重连网络
def do_reconnect_modbus(window,master,camera):
    if master.is_reconnect():
        do_btn_tcp_connect(window,master,camera)
    else:
        pass

#刷新界面
def do_ui_refresh(window,master):
    '''
    do_widget_set_enbaled(window,master)
    do_label_refresh(window,master)
    show_map(window)
    '''
    while 1:
        time.sleep(1)
        do_widget_set_enbaled(window,master)
        do_label_refresh(window,master)
        #show_map(window)
        pass
        

#设置控件可用
def do_widget_set_enbaled(window,master):
    if master.is_opened() and master.is_reconnect()==False :
        window.tabWidget_robo_ctrl.setEnabled(True)
    else:
        window.tabWidget_robo_ctrl.setEnabled(False)

#标签刷新###############################################################################
def do_label_refresh(window,master):    
    if master.is_opened():
        window.label_heartbeat.setText("心跳：" + str(master.read(heartbeat)))
        window.label_robo_speed.setText("速度：" + str(master.read(robo_speed)) + "mm/s")
        if not master.read(steer_angle) == None:
            window.label_steer_angle.setText("转向：" + "{:.1f}".format(master.read(steer_angle)) + "度")
        window.label_bat_soc.setText("电量：" + str(master.read(bat_soc)) + "%")
        window.label_water_level.setText("水位：" + str(master.read(water_level)) + "%")

    if master.is_reconnect():
        window.label_heartbeat.setText("心跳：" + "--")
        window.label_robo_speed.setText("速度：" + "--" + "mm/s")
        window.label_steer_angle.setText("转向：" + "--" + "度")
        window.label_bat_soc.setText("电量：" + "--" + "%")
        window.label_water_level.setText("水位：" + "--" + "%")

def load_map(window):
    window.svgWidget = QtSvg.QSvgWidget('map.svg')
    window.scrollArea_map.setWidget(window.svgWidget)

#显示SVG地图
x=0
def show_map(window):
    render=window.svgWidget.renderer()
    global x
    x=x+1
    render.setViewBox(QRect(x,10,100,80))
    window.scrollArea_map.repaint()
    #render.repaintNeeded.connect(window.scrollArea_map.repaint)


    




