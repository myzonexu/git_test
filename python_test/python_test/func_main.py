import time
import main

class FuncMain:
    def __init__(self):
        print("初始化主逻辑")
    def func_main(self):
        print("运行主程序功能")

def do_main_ui(window):
    #按钮响应
    do_push_button(window)

    return

def do_push_button(window):
    #按钮响应
    window.pushButton_autorun_start.clicked.connect(do_btn_autorun_start)
    window.pushButton_autorun_stop.clicked.connect(do_btn_autorun_stop)
    window.pushButton_autorun_charge.clicked.connect(do_btn_autorun_charge)
    window.pushButton_autorun_add_water.clicked.connect(do_btn_autorun_add_water)

    window.pushButton_drive_forward.clicked.connect(do_btn_drive_forward)
    window.pushButton_drive_backward.clicked.connect(do_btn_drive_backward)
    window.pushButton_drive_pause.clicked.connect(do_btn_drive_pause)
    window.pushButton_turn_left.clicked.connect(do_btn_turn_left)
    window.pushButton_turn_right.clicked.connect(do_btn_turn_right)

    return

#自动任务处理
def do_btn_autorun_start():
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
    return

def do_btn_drive_backward():
    print("后退")
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