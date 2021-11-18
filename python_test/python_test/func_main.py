import time
from func_modbus_tcp import *
from PyQt5.QtCore import QTimer


###################################################################################################
def do_main_ui(window,master):

    #设置快捷键
    ui_set_shortcut(window)
    #按钮响应
    do_push_button(window,master)
   
    #定时刷新界面文字
    window.timer = QTimer(window)  # 初始化一个定时器
    window.timer.timeout.connect(lambda:do_label(window,master))  # 每次计时到时间时发出信号
    window.timer.start(1000)  # 设置计时间隔并启动；单位毫秒

    #定时自动掉线重连网络
    window.timer2 = QTimer(window)  # 初始化一个定时器
    window.timer2.timeout.connect(lambda:do_reconnect_modbus(window,master))  # 每次计时到时间时发出信号
    window.timer2.start(5000)

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
def do_push_button(window,master):
    window.pushButton_autorun_start.clicked.connect(lambda:do_btn_autorun_start(master))
    window.pushButton_autorun_stop.clicked.connect(lambda:do_btn_autorun_stop(master))
    window.pushButton_autorun_charge.clicked.connect(lambda:do_btn_autorun_charge(master))
    window.pushButton_autorun_add_water.clicked.connect(lambda:do_btn_autorun_add_water(master))

    window.pushButton_drive_forward.pressed.connect(lambda:do_btn_drive_forward(master))
    window.pushButton_drive_forward.released.connect(lambda:do_btn_drive_forward_straight(master))
    #window.pushButton_drive_backward.clicked.connect(lambda:do_btn_drive_backward(master))
    window.pushButton_drive_backward.pressed.connect(lambda:do_btn_drive_backward(master))
    window.pushButton_drive_backward.released.connect(lambda:do_btn_drive_backward_straight(master))
    window.pushButton_drive_pause.clicked.connect(lambda:do_btn_drive_pause(master))
    window.pushButton_turn_left.clicked.connect(lambda:do_btn_turn_left(master))
    window.pushButton_turn_right.clicked.connect(lambda:do_btn_turn_right(master))

    window.pushButton_arm_position_origin.clicked.connect(lambda:do_btn_arm_position_origin(master))
    window.pushButton_arm_position_wall_1.clicked.connect(lambda:do_btn_arm_position_wall_1(master))
    window.pushButton_arm_position_wall_2.clicked.connect(lambda:do_btn_arm_position_wall_2(master))
    window.pushButton_arm_position_wall_3.clicked.connect(lambda:do_btn_arm_position_wall_3(master))
    window.pushButton_arm_position_wall_4.clicked.connect(lambda:do_btn_arm_position_wall_4(master))
    window.pushButton_arm_position_ground_1.clicked.connect(lambda:do_btn_arm_position_ground_1(master))
    window.pushButton_work_clean.clicked.connect(lambda:do_btn_work_clean(window))

    window.pushButton_tcp_connect.clicked.connect(lambda:do_btn_tcp_connect(window,master))
    window.pushButton_tcp_disconnect.clicked.connect(lambda:do_btn_tcp_disconnect(window,master))

    #window.verticalScrollBar_robo_speed.valueChanged.connect(lambda:print(window.verticalScrollBar_robo_speed.value()))
    #window.verticalScrollBar_robo_speed.valueChanged.connect(lambda:do_scroll_robo_speed(window))
    #window.horizontalScrollBar_steer_angle.valueChanged.connect(lambda:do_scroll_steer_angle(window))

    return

#带切换功能按键响应
def do_toggle_widget(widget,up_text,up_func,down_text,down_func):
#def do_toggle_widget(widget,up_text,down_text):
    if widget.isChecked() == True :
        up_func()
        widget.setText(down_text)
        pass
    elif widget.isChecked() == False :
        down_func()
        widget.setText(up_text)
        pass
    else :
        pass
    
'''
def do_scroll_robo_speed(window):
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #手动模式-取消暂停
    drive_ctrl.value = 0
    modbus_write(master,drive_ctrl)
    #手动模式下速度输入
    robo_speed_set.value = window.verticalScrollBar_robo_speed.value()
    modbus_write(master,robo_speed_set)
    #print(window.verticalScrollBar_robo_speed.value())
    return

def do_scroll_steer_angle(window):
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #手动模式下转角输入
    steer_angle_set.value = window.horizontalScrollBar_steer_angle.value()
    modbus_write(master,steer_angle_set)
    return
'''


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


#手动控制处理
def do_btn_drive_forward(master):
    if master.is_opened():
        print("前进")
        #控制模式-手动
        master.write(ctrl_mode,1)
        #手动模式-取消暂停
        master.write(drive_ctrl,0)
        #手动模式下速度输入
        master.write(robo_speed_set,robo_speed_set_manual_forward)
    else:
        pass

def do_btn_drive_forward_straight(master):
    if master.is_opened():
        print("前进")
        #控制模式-手动
        master.write(ctrl_mode,1)
        #手动模式-取消暂停
        master.write(drive_ctrl,0)
        #手动模式下转角输入0
        master.write(steer_angle_set,0)
        #手动模式下速度输入
        master.write(robo_speed_set,robo_speed_set_manual_forward)
    else:
        pass

def do_btn_drive_backward(master):
    print("后退")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #手动模式-取消暂停
    drive_ctrl.value = 0
    modbus_write(master,drive_ctrl)
    #手动模式下速度输入
    robo_speed_set.value = robo_speed_set_manual_backward
    modbus_write(master,robo_speed_set)
    return

def do_btn_drive_backward_straight(master):
    print("后退")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #手动模式-取消暂停
    drive_ctrl.value = 0
    modbus_write(master,drive_ctrl)
    #手动模式下转角输入0
    steer_angle_set.value = 0
    modbus_write(master,steer_angle_set)
    #手动模式下速度输入
    robo_speed_set.value = robo_speed_set_manual_backward
    modbus_write(master,robo_speed_set)
    return

def do_btn_drive_pause(master):
    print("暂停行驶")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #手动模式-暂停
    #drive_ctrl.value = 3
    #modbus_write(master,drive_ctrl)
    robo_speed_set.value = 0
    modbus_write(master,robo_speed_set)
    return

def do_btn_turn_left(master):
    print("左转")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #手动模式下转角输入
    steer_angle_set.value = robo_steer_angle_set_manual_left
    modbus_write(master,steer_angle_set)
    return

def do_btn_turn_right(master):
    print("右转")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #手动模式下转角输入
    steer_angle_set.value = robo_steer_angle_set_manual_right
    modbus_write(master,steer_angle_set)
    return

#机械臂控制处理
#定位初始位置
def do_btn_arm_position_origin(master):
    print("定位初始位置")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #定位初始位置
    arm_ctrl.value = 0
    modbus_write(master,arm_ctrl)
    return

#定位侧壁-1
def do_btn_arm_position_wall_1(master):
    print("定位侧壁-1")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #定位侧壁-1
    arm_ctrl.value = 1
    modbus_write(master,arm_ctrl)
    return

#定位侧壁-2
def do_btn_arm_position_wall_2(master):
    print("定位侧壁-2")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #定位侧壁-2
    arm_ctrl.value = 2
    modbus_write(master,arm_ctrl)
    return

#定位侧壁-3
def do_btn_arm_position_wall_3(master):
    print("定位侧壁-3")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #定位侧壁-3
    arm_ctrl.value = 3
    modbus_write(master,arm_ctrl)
    return

#定位侧壁-4
def do_btn_arm_position_wall_4(master):
    print("定位侧壁-4")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #定位侧壁-4
    arm_ctrl.value = 4
    modbus_write(master,arm_ctrl)
    return

#定位地面-1
def do_btn_arm_position_ground_1(master):
    print("定位地面-1")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #定位地面-1
    arm_ctrl.value = 5
    modbus_write(master,arm_ctrl)
    return

#开关滚刷控制功能
def do_btn_work_clean_start(master):
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    work_ctrl.value = 1 
    print("开水泵、刷子")
    modbus_write(master,work_ctrl)
    
def do_btn_work_clean_stop(master):
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    work_ctrl.value = 0
    print("关水泵、刷子")
    modbus_write(master,work_ctrl)

#控制水泵、刷子
def do_btn_work_clean(window):
    #带功能切换按键
    do_toggle_widget(window.pushButton_work_clean,"开滚刷",do_btn_work_clean_start,"关滚刷",do_btn_work_clean_stop)

    return



#连接网络
def do_btn_tcp_connect(window,master):
    try:
        host = window.lineEdit_ip_addr.text()
        master.set_host(host)
        master.set_timeout(MODBUS_TIMEOUT)
        master.open()
        master.no_reconnect()
        connect_info = "连接网络: " + host + " 成功"
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
def do_reconnect_modbus(window,master):
    if master.is_reconnect():
        do_btn_tcp_connect(window,master)
    else:
        pass

#标签刷新###############################################################################
def do_label(window,master):    
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



