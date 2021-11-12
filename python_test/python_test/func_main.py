import time
from func_modbus_tcp import *
from PyQt5.QtCore import QTimer

class FuncMain:
    def __init__(self):
        print("初始化主逻辑")
    def func_main(self):
        print("运行主程序功能")

def do_main_ui(window):
    #设置快捷键
    ui_set_shortcut(window)
    #按钮响应
    do_push_button(window)
    
    #定时刷新界面文字
    window.timer = QTimer(window)  # 初始化一个定时器
    window.timer.timeout.connect(lambda:do_label(window))  # 每次计时到时间时发出信号
    window.timer.start(1000)  # 设置计时间隔并启动；单位毫秒

    return

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
def do_push_button(window):
    #window.pushButton_autorun_start.clicked.connect(lambda:do_btn_autorun_start(window))
    window.pushButton_autorun_start.clicked.connect(do_btn_autorun_start)
    window.pushButton_autorun_stop.clicked.connect(do_btn_autorun_stop)
    window.pushButton_autorun_charge.clicked.connect(do_btn_autorun_charge)
    window.pushButton_autorun_add_water.clicked.connect(do_btn_autorun_add_water)

    #window.pushButton_drive_forward.clicked.connect(do_btn_drive_forward)
    window.pushButton_drive_forward.pressed.connect(do_btn_drive_forward)
    window.pushButton_drive_forward.released.connect(do_btn_drive_forward_straight)
    #window.pushButton_drive_backward.clicked.connect(do_btn_drive_backward)
    window.pushButton_drive_backward.pressed.connect(do_btn_drive_backward)
    window.pushButton_drive_backward.released.connect(do_btn_drive_backward_straight)
    window.pushButton_drive_pause.clicked.connect(do_btn_drive_pause)
    window.pushButton_turn_left.clicked.connect(do_btn_turn_left)
    window.pushButton_turn_right.clicked.connect(do_btn_turn_right)

    window.pushButton_arm_position_origin.clicked.connect(do_btn_arm_position_origin)
    window.pushButton_arm_position_wall_1.clicked.connect(do_btn_arm_position_wall_1)
    window.pushButton_arm_position_wall_2.clicked.connect(do_btn_arm_position_wall_2)
    window.pushButton_arm_position_wall_3.clicked.connect(do_btn_arm_position_wall_3)
    window.pushButton_arm_position_wall_4.clicked.connect(do_btn_arm_position_wall_4)
    window.pushButton_arm_position_ground_1.clicked.connect(do_btn_arm_position_ground_1)
    window.pushButton_work_clean.clicked.connect(do_btn_work_clean)

    window.pushButton_tcp_connect.clicked.connect(lambda:do_btn_tcp_connect(window,master))
    window.pushButton_tcp_disconnect.clicked.connect(lambda:do_btn_tcp_disconnect(window))

    window.verticalScrollBar_robo_speed.valueChanged.connect(do_scroll_robo_speed)
    window.horizontalScrollBar_steer_angle.valueChanged.connect(do_scroll_steer_angle)

    return

def do_scroll_robo_speed(window):
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #手动模式-取消暂停
    drive_ctrl.value = 0
    modbus_write(master,drive_ctrl)
    #手动模式下速度输入
    robo_speed_set.value = float(window.verticalScrollBar_robo_speed.valueChanged())
    modbus_write(master,robo_speed_set)
    return

def do_scroll_steer_angle(window):
    #print(window.horizontalScrollBar_steer_angle.sliderposition)
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #手动模式下转角输入
    #steer_angle_set.value = float(window.horizontalScrollBar_steer_angle.valueChanged())
    modbus_write(master,steer_angle_set)
    return



#自动任务处理
def do_btn_autorun_start(window):
    #do_label(window)
    print("自动任务开始")
    #控制模式-自动
    ctrl_mode.value = 0
    modbus_write(master,ctrl_mode)
    #清洗任务-开始
    start_clean.value = 1
    modbus_write(master,start_clean)
    return

def do_btn_autorun_stop():
    print("自动任务结束")
    #控制模式-自动
    ctrl_mode.value = 0
    modbus_write(master,ctrl_mode)
    #清洗任务-结束
    start_clean.value = 0
    modbus_write(master,start_clean)
    return

def do_btn_autorun_charge():
    print("手动任务充电")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #充电
    work_ctrl.value = 2
    modbus_write(master,work_ctrl)    
    return

def do_btn_autorun_add_water():
    print("手动任务加水")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #加水
    work_ctrl.value = 3
    modbus_write(master,work_ctrl)   
    return

#手动控制处理
def do_btn_drive_forward():
    print("前进")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #手动模式-取消暂停
    drive_ctrl.value = 0
    modbus_write(master,drive_ctrl)
    #手动模式下速度输入
    robo_speed_set.value = robo_speed_set_manual_forward
    modbus_write(master,robo_speed_set)
    return

def do_btn_drive_forward_straight():
    print("前进")
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
    robo_speed_set.value = robo_speed_set_manual_forward
    modbus_write(master,robo_speed_set)
    return

def do_btn_drive_backward():
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

def do_btn_drive_backward_straight():
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

def do_btn_drive_pause():
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

def do_btn_turn_left():
    print("左转")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #手动模式下转角输入
    steer_angle_set.value = robo_steer_angle_set_manual_left
    modbus_write(master,steer_angle_set)
    return

def do_btn_turn_right():
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
def do_btn_arm_position_origin():
    print("定位初始位置")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #定位初始位置
    arm_ctrl.value = 0
    modbus_write(master,arm_ctrl)
    return

#定位侧壁-1
def do_btn_arm_position_wall_1():
    print("定位侧壁-1")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #定位侧壁-1
    arm_ctrl.value = 1
    modbus_write(master,arm_ctrl)
    return

#定位侧壁-2
def do_btn_arm_position_wall_2():
    print("定位侧壁-2")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #定位侧壁-2
    arm_ctrl.value = 2
    modbus_write(master,arm_ctrl)
    return

#定位侧壁-3
def do_btn_arm_position_wall_3():
    print("定位侧壁-3")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #定位侧壁-3
    arm_ctrl.value = 3
    modbus_write(master,arm_ctrl)
    return

#定位侧壁-4
def do_btn_arm_position_wall_4():
    print("定位侧壁-4")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #定位侧壁-4
    arm_ctrl.value = 4
    modbus_write(master,arm_ctrl)
    return

#定位地面-1
def do_btn_arm_position_ground_1():
    print("定位地面-1")
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #定位地面-1
    arm_ctrl.value = 5
    modbus_write(master,arm_ctrl)
    return

#控制水泵、刷子
def do_btn_work_clean():
    
    #控制模式-手动
    ctrl_mode.value = 1
    modbus_write(master,ctrl_mode)
    #开关
    if (work_ctrl.value == 0):
        work_ctrl.value = 1 
        print("开水泵、刷子")
    elif (work_ctrl.value == 1):
        work_ctrl.value = 0
        print("关水泵、刷子")
    else:
        brake
    modbus_write(master,work_ctrl)
    return


#网络设置-未实现
def do_btn_tcp_connect(window,master):
    print("连接网络"+window.lineEdit_ip_addr.text())
    master=modbus_tcp.TcpMaster(window.lineEdit_ip_addr.text())
    return 

def do_btn_tcp_disconnect(window):
    print("断开网络"+window.lineEdit_ip_addr.text())
    master.close()
    return

#标签刷新###############################################################################
def do_label(window):
    modbus_read(master,heartbeat)
    window.label_heartbeat.setText("心跳："+str(heartbeat.value))
    modbus_read(master,robo_speed)
    window.label_robo_speed.setText("速度："+str(robo_speed.value)+"mm/s")
    modbus_read(master,steer_angle)
    window.label_steer_angle.setText("转向："+"{:.1f}".format(steer_angle.value)+"度")
    modbus_read(master,bat_soc)
    window.label_bat_soc.setText("电量："+str(bat_soc.value)+"%")
    modbus_read(master,water_level)
    window.label_water_level.setText("水位："+str(water_level.value)+"%")
    
    return


