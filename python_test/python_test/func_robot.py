from dataclasses import dataclass,field
from typing import List
import time
from datetime import datetime,timedelta

from func_camera import *
from func_modbus_tcp import *

#值-描述 集合
class ValueDescriptionSet(object):
    def __init__(self, tuple_value_description, value=0):
        self.set = tuple_value_description
        self.value = value

    def set_value(self,value):
        self.value = value

    def get_value(self):
        return self.value

    def description(self,format="value:description"):
        desc = self.set[self.value][1]
        if format == "description":
            description = str(desc)
        elif format == "value:description":
            description = str(self.value) + ":" + str(desc)
        elif format == "value-description":
            description = str(self.value) + "-" + str(desc)
        elif format == "description(value)":
            description = str(desc) + "(" + str(self.value) + ")"
        return description
    

#基本状态
class BaseState(object):
    def __init__(self):
        self._type = ""
        self.tag = 0
        self.run_state = ValueDescriptionSet(robot_run_state)
        self.ctrl_mode = ValueDescriptionSet(robot_ctrl_mode)


#版本
@dataclass(init=True)
class VersionState:
    #主版本、次版本、修订
    major :int = 0
    minor :int = 0
    patch :int = 0

    def get(self):
        return str(self.major) + "." + str(self.minor) + "." + str(self.patch)


#通讯
class CommunicationState(object):
    def __init__(self):
        self.is_online = False
        self.state = ValueDescriptionSet(communication_state)
        self.ip = "127.0.0.1"
        self.port = 502


#电池
@dataclass(init=True)
class BatteryState:
    soc : int = 0
    soh :int = 0
    voltage :float = 0.0


#行驶状态
@dataclass
class DriveState:
    speed : float = 0.0
    angle : float = 0.0    
    mileage :float = 0.0


#导航
@dataclass(init=True)
class NaviState:
    #避障 前，后
    avoide_front :int = 0
    avoide_rear :int = 0
    position :float = 0.0


#清扫附件
@dataclass
class CleanerState:
    is_open :bool = False
    water_level :int = 0


#机械臂
class ArmState(object):
    def __init__(self):
        self.state = ValueDescriptionSet(arm_state)
        self.position = 0


#故障码
class ErrorCode(object):
    def __init__(self):
        self.err_level = ValueDescriptionSet(err_level)
        self.err_code = 0
        self.description = ""
        self.handle = ""
        

#故障事件
class ErrorEvent(object):
    def __init__(self):
        self.err_code = ErrorCode()
        self.time_start = datetime(1970,1,1)
        self.time_stop = datetime(1970,1,1)

#故障状态
class ErrorState(object):
    def __init__(self):
        self.active_count = 0
        self.history_count = 0
        #ErrorEvent列表
        self.active_error_list = []
        self.history_error_list = []


#清扫任务
class CleanTaskState(object):
    def __init__(self):
        self.state = ValueDescriptionSet(clean_task_state)
        self.start_time = datetime(1970,1,1)
        self.stop_time = datetime(1970,1,1)
        self.mileage_driven = 0.0
        self.mileage_total = 0.0
        self.mileage_estimate = 0.0
        self.mileage_remain = 0.0
        self.count_cleaned = 0
        self.count_add_water = 0
        self.count_charged = 0
        self.progress = 0
        self.time_worked = 0
        self.time_total = 0
        self.time_estimate = 0
        self.time_remain = 0


#日志
@dataclass
class LogState:
    #['ID', '时间', '模块', '功能']
    id : int
    log_time : int
    module : int
    log_function : int

class Robot(object):
    def __init__(self):
        self.unique_id = 0
        self.base = BaseState()
        self.version = VersionState()
        self.communication = CommunicationState()
        self.battery = BatteryState()
        self.drive = DriveState()
        self.navi = NaviState()
        self.cleaner = CleanerState()
        self.arm = ArmState()
        self.self_time = datetime(1970,1,1)
        self.error_chassis = ErrorState()
        self.error_arm = ErrorState()
        self.task = CleanTaskState()
        self.master = SpnTcpMaster()
        self.camera = CameraRtsp()

    def init(self,ip):
        set_ip("")
        self.master.open()

    def set_ip(self,ip):
        self.communication.ip = ip
        self.master.set_host(ip)
        #self.camera.set_ip(ip)

    def err_count(self):
        return self.error_chassis.active_count + self.error_arm.active_count

    def robot_info(self):
        robot_info = [["ID编号",self.unique_id],["运行状态",self.base.run_state.description()],
              ["速度",self.drive.speed],["转角",self.drive.angle],["电量",self.battery.soc],
              ["水位",self.cleaner.water_level],["总里程",self.drive.mileage],["控制模式",self.base.ctrl_mode.description()],
              ["ip地址",self.communication.ip],["连接状态",self.communication.state.description()],["程序版本",self.version.get()]]
        return robot_info
    def task_info(self):
        task_info = [["状态",self.task.state.description()],["开始时间",self.task.start_time.strftime(TIME_SHOW_H_M_S)],["工作时长",self.task.time_worked],["行驶里程",self.task.mileage_driven],
                   ["清扫数量",self.task.count_cleaned],["加水次数",self.task.count_add_water],["充电次数",self.task.count_charged],
                   ["结束时间",self.task.stop_time.strftime(TIME_SHOW_H_M_S)]]            
        return task_info
    def list_info(self):
        list_info = [self.base.id,self.communication.ip,self.camera.ip,self.communication.state]
        return list_info
#机器人
class RobotGroup(object):
    def __init__(self):
        self.robot = []
        self.select = 0

    def list_info(self):
        list_info = []
        count = len(self.robot)
        for x in range(count):
            list_info.insert(x,[self.robot[x].unique_id,self.robot[x].communication.ip,self.robot[x].communication.state.description(),
                                self.robot[x].base.run_state.description(),self.robot[x].task.state.description(),self.robot[x].err_count()])
        return list_info


#状态值定义
robot_run_state = ((0,"关机"),(1,"运行"),(2,"待机"),(3,"休眠"),(4,"停机"),(5,"急停"))
robot_ctrl_mode = ((0,"自动"),(1,"手动"),(2,"遥控器"))
communication_state = ((0,"离线"),(1,"在线"),(2,"掉线重联"))
arm_state = ((0,"到位"),(1,"运行"))
clean_task_state = ((0,"无"),(1,"自动"),(2,"清洗"),(3,"充电"),(4,"加水"),(5,"等待下次任务"))
err_level = ((0,"无"),(1,"警告"),(2,"轻微故障"),(3,"严重故障"))
#时间显示格式
TIME_SHOW_ALL = '%Y-%m-%d %H:%M:%S'
TIME_SHOW_H_M_S = '%H:%M:%S'

#变量定义
robot_group = RobotGroup()


#test
robot1 = Robot()
robot1.unique_id = 10
robot1.base.run_state.value = 2
robot1.task.state.value = 5
robot1.set_ip("192.168.2.107")
robot2 = Robot()
robot2.unique_id = 11
robot2.base.run_state.value = 1
robot2.set_ip("192.168.2.114")
robot_group.robot.append(robot1)
robot_group.robot.append(robot2)

#print(robot1.__dict__)
#new_robot.master.write(protocol.arm_ctrl,3)
