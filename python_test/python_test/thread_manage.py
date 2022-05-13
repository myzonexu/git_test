import threading
import time
import copy
from func_robot import *
from func_common import *
from multiprocessing import Process

def get_camera_frame():
    while True:
        if robots.current==None:
            pass
        else:
            if robots.current.master.is_opened():
                robots.current.camera.get_frame()
            else:
                pass


#def get_robots_state_():    
#    sec=0
#    while True:
#        robots.add_robot_new_scanned()
#        if robots.current==None:
#            pass
#        else:
#            if robots.current.connect.is_online:
#                robots.current.get_robot_time()
#                pass
#        for id in robots.all:
#            robots.check_addrs_online(robots.all.get(id))
#            robots.all.get(id).get_state()
#            if sec>60:
#                    robots.all.get(id).sync_time()
#                    sec=0
#            #if robots.all.get(id).connect.is_online:
#            #    robots.all.get(id).get_state()
#            #    robots.check_addrs_online(robots.all.get(id))

#                ##同步时间，间隔1分钟
#                #if sec>60:
#                #    robots.all.get(id).sync_time()
#                #    sec=0
#        time.sleep(1)
#        sec=sec+1

def get_robots_state():    
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

#def scan_robots_():
#    #robots.local_ip
#    exit=1
#    while exit:
#        for n in range(113,120):
#            scan_ip=robots.setup_scan_ip(n)
#            if scan_ip not in robots.addrs_online:
#                new_robot=Robot(ip=scan_ip)
#                new_robot.master.set_timeout(1)
#                new_robot.master.read(new_robot.protocol.robot_id)
#                if new_robot.master.is_opened():
#                    #lock
#                    new_id=new_robot.protocol.robot_id.value
#                    robots.addrs_new_scanned.append([new_id,scan_ip])
#                    #robots.all[new_id]=Robot(ip=scan_ip)
#                    #robots.all.get(new_id).get_state()
#                    #robots.all.get(new_id).sync_time()
#                    #robots.addrs_online.add(scan_ip)
#                    #print("检测到机器人id",new_id,scan_ip)

#                    #if robots.current==None:
#                    #    robots.current=robots.all.get(new_id)
#                    #    exit=0
#                    if robots.current is None:
#                        pass
#                    else:                        
#                        exit=0
#                        break
#            else:
#                print("ip已连接，跳过",scan_ip)
#                exit=0
#                break
#            time.sleep(1)

def scan_robots():
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

 

def send_modbus_write_buffer():
    while True:
        #for id in robots.all: 
        #for id in list(robots.all.keys()):
        for _robot in list(robots.all.values()):
            if _robot.master.is_opened():
                _robot.master.send_write_buffer()

            time.sleep(1)
           

#线程管理
def thread_manage():
    #thread_get_camera_frame.setDaemon(True)
    #thread_get_camera_frame.start()
    thread_get_robots_state.setDaemon(True)
    thread_get_robots_state.start()
    thread_send_modbus_write_buffer.setDaemon(True)
    thread_send_modbus_write_buffer.start()
    thread_scan_robots.setDaemon(True)
    thread_scan_robots.start()
    process_scan_robots.daemon=True
    #process_scan_robots.start()

def thread_close():
    #thread_get_camera_frame.join()
    thread_get_robots_state.join()
    thread_send_modbus_write_buffer.join()


#进程管理
def process_manage():    
    process_scan_robots.daemon=True
    process_scan_robots.start()
    process_get_robots_state.daemon=True
    process_get_robots_state.start()
    process_send_modbus_write_buffer.daemon=True
    #process_send_modbus_write_buffer.start()


#app_exit=False
#线程：相机采集视频
#thread_get_camera_frame = threading.Thread(target=get_camera_frame, name='get_camera_frame')
#线程：读取机器人状态
thread_get_robots_state = threading.Thread(target=get_robots_state, name='get_robots_state')
#线程：发送modbus写缓存中的数据
thread_send_modbus_write_buffer = threading.Thread(target=send_modbus_write_buffer, name='send_modbus_write_buffer')
#线程：扫描局域网机器人
thread_scan_robots = threading.Thread(target=scan_robots, name='scan_robots')


process_scan_robots = Process(target=scan_robots)
process_get_robots_state = Process(target=get_robots_state)
process_send_modbus_write_buffer = Process(target=send_modbus_write_buffer)