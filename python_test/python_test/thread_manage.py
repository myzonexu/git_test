import threading
import time
import copy
from func_robot import *

def get_camera_frame():
    while window_main.tabWidget_main.currentIndex()==0:
        if robots.now.master.is_opened():
            robots.now.camera.get_frame()
            robots.now.camera.frame_scale(window_main.label_camera.height())
        else:
            pass

def camera_frame_scale():
    while 1:
        if robots.now.master.is_opened()  and window_main.tabWidget_main.currentIndex()==0:
        #if True :
            robots.now.camera.frame_scale(window_main.label_camera.height())
        else:
            pass
def get_robots_state():    
    sec=0
    while 1:
        if robots.now==None:
            pass
        else:
            if robots.now.communication.is_online:
                robots.now.get_robot_time()
        for id in robots.robots:
            if robots.robots.get(id).communication.is_online:
                robots.robots.get(id).get_state()
                robots.check_addrs_online(robots.robots.get(id))

                #同步时间，间隔1分钟
                if sec>60:
                    robots.robots.get(id).sync_time()
                    sec=0
        time.sleep(1)
        sec=sec+1

def scan_robots():
    #robots.local_ip
    exit=1
    while exit:
        for n in range(110,120):
            scan_ip=robots.setup_scan_ip(n)
            if scan_ip not in robots.addrs_online:
                new_robot=Robot(ip=scan_ip)
                new_robot.master.set_timeout(1)
                new_robot.master.read(new_robot.protocol.robot_id)
                if new_robot.master.is_opened():
                    #lock
                    new_id=new_robot.protocol.robot_id.value
                    robots.robots[new_id]=Robot(ip=scan_ip)
                    robots.robots.get(new_id).get_state()
                    robots.robots.get(new_id).sync_time()
                    robots.addrs_online.add(scan_ip)
                    print("检测到机器人id",new_id,scan_ip)

                    if robots.now==None:
                        robots.now=robots.robots.get(new_id)
                        exit=0
            else:
                print("ip已连接，跳过",scan_ip)
                    
               
    

def send_modbus_write_buffer():
    while 1:
        for id in robots.robots:
            robots.robots.get(id).master.send_write_buffer()

#线程管理
def thread_manage():
    #thread_get_camera_frame.start()
    thread_get_robots_state.start()
    #thread_send_modbus_write_buffer.start()
    thread_scan_robots.start()

def thread_close():
    #thread_get_camera_frame.join()
    thread_get_robots_state.join()
    thread_send_modbus_write_buffer.join()

#线程：相机采集视频
#thread_get_camera_frame = threading.Thread(target=get_camera_frame, name='get_camera_frame')
#线程：读取机器人状态
thread_get_robots_state = threading.Thread(target=get_robots_state, name='get_robots_state')
#线程：发送modbus写缓存中的数据
thread_send_modbus_write_buffer = threading.Thread(target=send_modbus_write_buffer, name='send_modbus_write_buffer')
#线程：扫描局域网机器人
thread_scan_robots = threading.Thread(target=scan_robots, name='scan_robots')
