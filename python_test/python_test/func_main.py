import time
from func_modbus_tcp import *
from PyQt5.QtCore import QTimer

class FuncMain:
    def __init__(self):
        print("初始化主逻辑")
    def func_main(self):
        print("运行主程序功能")

def do_main_ui(window):
    #按钮响应
    do_push_button(window)
    
    #timer = QTimer(window)  # 初始化一个定时器
    window.timer = QTimer(window)  # 初始化一个定时器
    window.timer.timeout.connect(lambda:do_label(window))  # 每次计时到时间时发出信号
    window.timer.start(1000)  # 设置计时间隔并启动；单位毫秒
    
    do_label(window)
    return

#按钮响应####################################################################################
def do_push_button(window):
    #window.pushButton_autorun_start.clicked.connect(lambda:do_btn_autorun_start(window))
    window.pushButton_autorun_start.clicked.connect(do_btn_autorun_start)
    window.pushButton_autorun_stop.clicked.connect(do_btn_autorun_stop)
    window.pushButton_autorun_charge.clicked.connect(do_btn_autorun_charge)
    window.pushButton_autorun_add_water.clicked.connect(do_btn_autorun_add_water)

    window.pushButton_drive_forward.clicked.connect(do_btn_drive_forward)
    window.pushButton_drive_backward.clicked.connect(do_btn_drive_backward)
    window.pushButton_drive_pause.clicked.connect(do_btn_drive_pause)
    window.pushButton_turn_left.clicked.connect(do_btn_turn_left)
    window.pushButton_turn_right.clicked.connect(do_btn_turn_right)

    window.pushButton_tcp_connect.clicked.connect(lambda:do_btn_tcp_connect(window))
    window.pushButton_tcp_disconnect.clicked.connect(lambda:do_btn_tcp_disconnect(window))


    return

#自动任务处理
def do_btn_autorun_start(window):
    #do_label(window)
    print("自动任务开始")
    return

def do_btn_autorun_stop():
    print("自动任务结束")
    return

def do_btn_autorun_charge():
    print("自动任务充电")
    return

def do_btn_autorun_add_water():
    print("自动任务加水")
    return

#手动控制处理
def do_btn_drive_forward():
    print("前进")
    robo_speed_set.value = robo_speed_set_manual_forward
    modbus_write(master,robo_speed_set)
    return

def do_btn_drive_backward():
    print("后退")
    robo_speed_set.value = robo_speed_set_manual_backward
    modbus_write(master,robo_speed_set)
    return

def do_btn_drive_pause():
    print("暂停行驶")
    return

def do_btn_turn_left():
    print("左转")
    return

def do_btn_turn_right():
    print("右转")
    return

#机械臂控制处理


#网络设置
def do_btn_tcp_connect(window):
    print("连接网络"+window.lineEdit_ip_addr.text())
    return

def do_btn_tcp_disconnect(window):
    print("断开网络"+window.lineEdit_ip_addr.text())
    return

#标签刷新###############################################################################
def do_label(window):
    modbus_read(master,heartbeat)
    window.label_heartbeat.setText("心跳："+str(heartbeat.value))
    modbus_read(master,robo_speed)
    window.label_robo_speed.setText("速度："+str(robo_speed.value)+"mm/s")
    modbus_read(master,steer_angle)
    window.label_steer_angle.setText("转向："+str(steer_angle.value)+"度")
    modbus_read(master,bat_soc)
    window.label_bat_soc.setText("电量："+str(bat_soc.value)+"%")
    modbus_read(master,water_level)
    window.label_water_level.setText("水位："+str(water_level.value)+"%")
    
    return


