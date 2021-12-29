from dataclasses import dataclass,field
from typing import List
import socket
from datetime import datetime,timedelta
from PyQt5.QtCore import QObject , pyqtSignal
from func_common import *
from func_camera import *
from func_modbus_tcp import *

#常量定义
robot_run_state = ((0,"关机"),(1,"运行"),(2,"待机"),(3,"休眠"),(4,"停机"),(5,"急停"))
robot_ctrl_mode = ((0,"自动"),(1,"手动"),(2,"遥控器"))
communication_state = ((0,"离线"),(1,"在线"),(2,"掉线重联"))
arm_state = ((0,"报警"),(1,"运行"),(2,"到位"))
clean_task_state = ((0,"无任务"),(1,"墙面1清洗中"),(2,"墙面2清洗中"),(3,"墙面3清洗中"),
                    (4,"墙面4清洗中"),(5,"地面清洗中"),
                    (6,"中途充电"),(7,"中途加水"),(8,"等待下次任务"))
err_level = ((0,"无"),(1,"警告"),(2,"轻微故障"),(3,"严重故障"))
robot_error_code_dict={0:["无","无故障","无需处理"],1:["轻微故障","测试故障描述","测试处理方式"]}


#值-描述 集合
class ValueDescriptionSet(object):
    def __init__(self, tuple_value_description, value=0):
        self.value_set = tuple_value_description
        self.value = value

    def set_value(self,value):
        self.value = value

    def get_value(self):
        return self.value

    def description(self,format="value:description"):
        if self.value<len(self.value_set):
            desc = self.value_set[self.value][1]
        else:
            desc="非法值"
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
    def __init__(self,ip="127.0.0.1",port=502):
        self.is_online = False
        self.state = ValueDescriptionSet(communication_state)
        self.ip = ip
        self.port = port
        self.slave_id=1
        self.heartbeat=None

        


#电池
@dataclass(init=True)
class BatteryState:
    soc : int = 0
    soh :int = 0
    voltage :float = 0.0
    charging:bool=False



#行驶状态
@dataclass
class DriveState:
    speed : float = 0.0
    steer_angle : float = 0.0    
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
    def __init__(self,code=None,code_dict= robot_error_code_dict):
        self.code = code
        self.code_dict=code_dict

    #获取故障等级
    def level(self):
        if self.code in self.code_dict:
            level=self.code_dict.get(self.code)[0]
        else:
            level="无法获取故障等级"
        return level

    #获取故障描述
    def description(self):
        if self.code in self.code_dict:
            description=self.code_dict.get(self.code)[1]
        else:
            description="无法获取故障描述"
            
        return description

    #获取故障处理
    def handle(self):
        if self.code in self.code_dict:
            handle=self.code_dict.get(self.code)[2]
        else:
            handle="无法获取故障处理"
            
        return handle

    

        

#故障事件
class ErrorEvent(ErrorCode):
    def __init__(self,code=None,code_dict= robot_error_code_dict):
        super().__init__(code,code_dict)
        self.time_start = datetime.now()
        self.time_stop = None

#故障状态
class ErrorState(object):
    def __init__(self):
        #ErrorEvent列表
        self.active_error = {}
        self.history_error = []

    def add(self,err_event):
        self.active_error[err_event.code]=err_event
        
    def clear(self):
        for err_code in self.active_error:
            self.active_error[err_code].time_stop=datetime.now()
            self.history_error.append(self.active_error[err_code])
        self.active_error.clear()
       
    def clear_history(self):
        self.history_error.clear()

    #获取现行故障表格信息
    def active_err_info(self):
        list=[]
        for err_code in self.active_error:
            info=["现行故障",self.active_error[err_code].time_start.strftime(TIME_SHOW_ALL),self.active_error[err_code].level(),
                         self.active_error[err_code].code,self.active_error[err_code].description(),
                         self.active_error[err_code].handle()]
            if self.active_error[err_code].time_stop==None:
                info.append(None)
            else:
                info.append(self.active_error[err_code].time_stop.strftime(TIME_SHOW_ALL))
                
            list.append(info)
        return list

    #获取历史故障表格信息
    def history_err_info(self):  
        list=[]
        for err in self.history_error:
            list.append(["历史故障",err.time_start.strftime(TIME_SHOW_ALL),err.level(),err.code,err.description(),err.handle(),err.time_stop.strftime(TIME_SHOW_ALL)])
        return list

#清扫任务
class CleanTaskState(object):
    def __init__(self):
        self.state = ValueDescriptionSet(clean_task_state)
        self.start_time = None
        self.stop_time = None
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

  
#机器人集合
class RobotGroup(QObject):
    #current_inited=pyqtSignal(int)
    #current_changed=pyqtSignal(int)
    current_inited=pyqtSignal()
    current_changed=pyqtSignal()

    def __init__(self):
        super().__init__()
        self.robots = {}
        self.addrs_online=set([])
        #新检测到的ip列表，[[id1,ip1],[id2,ip2]]
        self.addrs_new_scanned=[]
        self.current=None
        self.local_ip = None
        self.local_ip_strlist=None

        self.get_local_ip()

    def add_robot_new_scanned(self):
        for n in range(len(self.addrs_new_scanned)):
            new_id=self.addrs_new_scanned[n][0]
            new_ip=self.addrs_new_scanned[n][1]
            if new_id in self.robots:
                self.robots.get(new_id).set_ip(new_ip)
            else:
                self.robots[new_id]=Robot(ip=new_ip)
                print("检测到机器人id",new_id,new_ip)
            self.robots.get(new_id).init()
            self.addrs_online.add(new_ip)
            self.addrs_new_scanned.pop(n)

            if self.current==None:
                self.current=self.robots.get(new_id)
     

    def add(self,robot):
        robot.get_state()
        if robot.unique_id is None:
            print("获取ID失败")
        else:
            self.robots[robot.unique_id]=robot
            print("获取ID,添加机器人",robot.unique_id)

    def delete(self,unique_id):
        self.robots.pop(unique_id)

    def init_current(self,unique_id):
        if self.current is None:
            if unique_id in self.robots:        
                self.current=self.robots.get(unique_id)
                #self.current_inited.emit(unique_id)
                self.current_inited.emit()
                print("设定当前机器人")
                return self.current
            else:
                print("无法找到此机器人")
                return None
        else:
            print("已有当前机器人")

    def set_current(self,unique_id):
        
        if unique_id in self.robots:        
            self.current=self.robots.get(unique_id)
            #self.current_changed.emit(unique_id)
            self.current_changed.emit()
            print("设定当前机器人ID为：",unique_id)
            return self.current
            
        else:
            print("无法找到此机器人")
            return None

    def check_addrs_online(self,robot):
        if robot.communication.is_online:
            self.addrs_online.add(robot.communication.ip)
            self.addrs_online.add(robot.camera.ip)
        else:
            if robot.communication.ip in self.addrs_online:
                self.addrs_online.remove(robot.communication.ip)
                self.addrs_online.remove(robot.camera.ip)

    def get_local_ip(self):
        hostname = socket.gethostname()
        # 获取本机ip
        self.local_ip = socket.gethostbyname(hostname)
        #self.local_ip ="192.168.1.1"
        self.local_ip_strlist=self.local_ip.split('.')
        print("ip：",self.local_ip)
        return self.local_ip_strlist
    def setup_scan_ip(self,ip_4th):
        self.local_ip_strlist[3]=str(ip_4th)
        scan_ip='.'.join(self.local_ip_strlist)
        return scan_ip

    def list_info(self):
        list_info = []
        if self.robots == {}:
            #print("没有机器人")
            pass
        else:
            count = len(self.robots)       
            for id in self.robots:
                list_info.append([self.robots.get(id).unique_id,self.robots.get(id).communication.ip,self.robots.get(id).communication.state.description(),
                                  self.robots.get(id).base.run_state.description(),self.robots.get(id).task.state.description(),self.robots.get(id).err_count(),self.robots.get(id).warning_count()])

        return list_info

#机器人
class Robot(QObject):
    state_updated=pyqtSignal()
    def __init__(self,ip="127.0.0.1",port=502):
        super().__init__()
        self.unique_id = None
        self.base = BaseState()
        self.version = VersionState()
        self.communication = CommunicationState(ip,port)
        self.protocol=CommunicationProtocol()
        self.battery = BatteryState()
        self.drive = DriveState()
        self.navi = NaviState()
        self.cleaner = CleanerState()
        self.arm = ArmState()
        self.robot_time = None
        self.error_chassis = ErrorState()
        self.error_arm = ErrorState()
        self.task = CleanTaskState()
        self.master = SpnTcpMaster(host=ip,port=port)
        self.camera = CameraRtsp(pc_test=True)
        #self.camera = CameraRtsp()
        self.log=LogState()
        #self.init(ip)

    def init(self):        
        #self.master.open()
        self.get_state()
        self.sync_time()
        #self.set_ip("")

    def set_ip(self,ip):
        self.communication.ip = ip
        self.master.set_host(ip)
        #self.camera.set_ip(ip)

    def err_count(self):
        count=len(self.error_chassis.active_error)+len(self.error_arm.active_error)
        return count

    def warning_count(self):
        pass

    def get_communication_state(self):
            self.communication.is_online=self.master.is_opened()
            if self.master.is_opened():
                self.communication.state.value=1
            else:
                if self.master.is_reconnect():
                    self.communication.state.value=2
                else:
                    self.communication.state.value=0

    #获取机器人信息参数列表
    def robot_info(self):
        robot_info = [["ID编号",self.unique_id],["连接状态",self.communication.state.description()],["运行状态",self.base.run_state.description()],
              ["速度(mm/s)    ",self.drive.speed],["转角(°)",self.drive.steer_angle],["电量(%)",self.battery.soc],["水位(%)",self.cleaner.water_level],
              ["总里程(m)",self.drive.mileage],["控制模式",self.base.ctrl_mode.description()],
              ["ip地址",self.communication.ip],["程序版本",self.version.get()],["机器人时间",check_time_info(self.robot_time)]]
        return robot_info

    #获取任务信息参数列表
    def task_info(self):
        task_info = [["状态",self.task.state.description()],["开始时间",check_time_info(self.task.start_time)],["工作时长",self.task.time_worked],["行驶里程(m)    ",self.task.mileage_driven],
                   ["清扫数量",self.task.count_cleaned],["加水次数",self.task.count_add_water],["充电次数",self.task.count_charged],
                   ["结束时间",check_time_info(self.task.stop_time)]]            
        return task_info

    #获取机器人状态，一次性读取所有只读部分并解析
    #@get_run_time
    def get_state(self):        
        self.read_all_readonly()
        self.parse_readonly_data()
        self.get_communication_state()

        self.state_updated.emit()

    #一次性读所有只读
    def read_all_readonly(self):
        recv_datas=self.master.read_multiple(self.protocol.addr_read_start,self.protocol.len_read)
        if recv_datas==None:
            pass
        else:
            for attr in self.protocol.attrs_readonly:
                recv_data=recv_datas[attr.addr-self.protocol.addr_read_start]
                attr.recv(recv_data)

    #解析读取数据
    def parse_readonly_data(self):
        self.unique_id=self.protocol.robot_id.value
        self.get_run_state()
        self.get_ctrl_mode()
        self.version.patch=self.protocol.soft_version.value
        self.communication.heartbeat=self.protocol.heartbeat.value
        self.battery.soc = self.protocol.bat_soc.value
        self.battery.soh = self.protocol.bat_soh.value
        self.battery.voltage= self.protocol.bat_voltage.value
        self.drive.speed = self.protocol.robot_speed.value
        self.drive.steer_angle = self.protocol.steer_angle.value
        self.drive.mileage = join_byte_hi_lo(self.protocol.mileage_hi.value,self.protocol.mileage_lo.value,16)
        self.get_avoide_state()
        self.navi.position=self.protocol.position_mark.value
        self.cleaner.water_level=self.protocol.water_level.value
        self.cleaner.is_open=(self.protocol.clean_state.value > 0)
        self.arm.position = self.protocol.clean_state.value
        self.get_arm_state()
        self.get_error_chassis()
        self.get_task_state()
        self.task.count_add_water = self.protocol.count_add_water.value
        self.task.count_charged = self.protocol.count_charged.value
        self.task.time_worked = self.protocol.clean_time_s.value                

    def get_run_state(self):
        if test_bit(self.protocol.robot_state.value,4):
            self.base.run_state.value = 1
        if test_bit(self.protocol.robot_state.value,6):
            self.base.run_state.value = 2
        if test_bit(self.protocol.robot_state.value,3):
            self.base.run_state.value = 5

    def get_ctrl_mode(self):
        if test_bit(self.protocol.robot_state.value,0):
            self.base.ctrl_mode.value = 0
        if test_bit(self.protocol.robot_state.value,1):
            self.base.ctrl_mode.value = 1
        if test_bit(self.protocol.robot_state.value,2):
            self.base.ctrl_mode.value = 2
        pass
    def get_avoide_state(self):
        if test_bit(self.protocol.chassis_state.value,9):
            self.navi.avoide_front=1
        else:
            self.navi.avoide_front=0
        if test_bit(self.protocol.chassis_state.value,10):
            self.navi.avoide_rear=1
        else:
            self.navi.avoide_rear=0
        pass
    def get_arm_state(self):
        #如何定义？
        pass
    def get_task_state(self):        
        self.task.state.value = self.protocol.clean_state.value
        pass
    
    #同步时间
    def sync_time(self):
        self.get_robot_time()
        time_now=datetime.now()
        if isinstance(self.robot_time,datetime):
            time_offset=datetime.now().timestamp()-self.robot_time.timestamp()
            if abs(time_offset)>5:
                self.set_robot_time()
                print("时间偏差:",time_offset,"同步时间")
        else:
            self.set_robot_time()

    #获取机器人时间
    def get_robot_time(self):
        #self.master.write(self.protocol.time_sync_rw,0)
        self.master.read(self.protocol.time_year)
        self.master.read(self.protocol.time_month)
        self.master.read(self.protocol.time_day)
        self.master.read(self.protocol.time_hour)
        self.master.read(self.protocol.time_min)
        self.master.read(self.protocol.time_sec)
        self.master.read(self.protocol.time_weekday)
        try:
            self.robot_time = datetime(self.protocol.time_year.value+2000,self.protocol.time_month.value,
                                       self.protocol.time_day.value,self.protocol.time_hour.value,
                                       self.protocol.time_min.value,self.protocol.time_sec.value)
        except Exception as e:
            print("时间值异常：",str(e))


        #if self.protocol.time_year.value<1970:
        #if self.protocol.time_year.value>99:
        #    print("非法时间值",self.protocol.time_year.value) 
        #    self.robot_time = False
        #else:
        #    self.robot_time = datetime(self.protocol.time_year.value+2000,self.protocol.time_month.value,
        #                               self.protocol.time_day.value,self.protocol.time_hour.value,
        #                               self.protocol.time_min.value,self.protocol.time_sec.value)
    
    #设置机器人时间为当前时间
    def set_robot_time(self):
        #time_now=datetime.now()
        self.master.write(self.protocol.time_sync_rw,1)
        time.sleep(1)
        time_now=datetime.now()
        self.master.write(self.protocol.time_year,time_now.year-2000)
        self.master.write(self.protocol.time_month,time_now.month)
        self.master.write(self.protocol.time_day,time_now.day)
        self.master.write(self.protocol.time_hour,time_now.hour)
        self.master.write(self.protocol.time_min,time_now.minute)
        self.master.write(self.protocol.time_sec,time_now.second)
        self.master.write(self.protocol.time_weekday,time_now.weekday())
        time.sleep(1)
        self.master.write(self.protocol.time_sync_rw,0)

        pass

    #获取故障信息
    def get_error_chassis(self):
        err_code=join_byte_hi_lo(self.protocol.error_chassis_hi.value,self.protocol.error_chassis_lo.value,16)
        if err_code==0 :
            self.error_chassis.clear()            
        elif err_code not in self.error_chassis.active_error:
            self.error_chassis.add(ErrorEvent(err_code))

    #界面控制机器人##########################################################################################################################
    #清除现行故障
    def clear_active_error(self):
        #清除底盘故障
        self.master.write(self.protocol.chassis_set,3)
        #清除手臂故障
        self.master.write(self.protocol.chassis_set,4)
    #任务-开始
    def clean_task_start(self):
        self.master.write(self.protocol.ctrl_mode,0)
        self.master.write(self.protocol.start_clean,1)
    #任务-结束
    def clean_task_stop(self):
        self.master.write(self.protocol.ctrl_mode,0)
        self.master.write(self.protocol.start_clean,2)
    ##手动-暂停
    #def clean_task_pause(self):
    #    self.master.write(self.protocol.ctrl_mode,1)
    #    self.master.write(self.protocol.start_clean,3)
    
    #手动-充电
    def charge_battery(self):
        self.master.write(self.protocol.ctrl_mode,1)
        self.master.write(self.protocol.work_ctrl,2)
    #手动-加水
    def add_water(self):
        self.master.write(self.protocol.ctrl_mode,1)
        self.master.write(self.protocol.work_ctrl,3)
    #手动-清洗 on_off:0-关闭；1-打开
    def pump_brush_ctrl(self,on_off):
        self.master.write(self.protocol.ctrl_mode,1)
        self.master.write(self.protocol.work_ctrl,on_off)
    #轨道行走-控制：1-前进；2-后退；3-暂停
    def on_track_drive_ctrl(self,ctrl_mode):
        self.master.write(self.protocol.ctrl_mode,1)
        self.master.write(self.protocol.drive_ctrl,ctrl_mode)
      
    #自由行走-速度
    def free_drive_ctrl_speed(self,speed):
        self.master.write(self.protocol.drive_ctrl,0)
        self.master.write(self.protocol.robot_speed_set,speed)
        #self.master.write_buffer(self.protocol.drive_ctrl,0)
        #self.master.write_buffer(self.protocol.robot_speed_set,speed)

    #自由行走-角度
    def free_drive_ctrl_angle(self,angle):
        self.master.write(self.protocol.drive_ctrl,0)
        self.master.write(self.protocol.steer_angle_set,angle)
    #底盘重新上电
    def restart_chassis(self):
        self.master.write(self.protocol.ctrl_mode,1)
        self.master.write(self.protocol.chassis_set,7)
    #机械臂重新上电
    def restart_arm(self):
        self.master.write(self.protocol.ctrl_mode,1)
        self.master.write(self.protocol.chassis_set,6)
    #机械臂位置-0~5
    def arm_ctrl_position(self,position):
        self.master.write(self.protocol.ctrl_mode,1)
        self.master.write(self.protocol.arm_ctrl,position)
    
#变量定义
robots = RobotGroup()
robot1=Robot()
robot2=Robot("192.168.2.107")
robots.add(robot1)
#robots.add(robot2)
#robots.init_current(robot1.unique_id)
#robots.current=robot1

