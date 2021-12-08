from dataclasses import dataclass

#机器人状态
@dataclass
class RobotState:
    #['型号', 'ID', '标签号', '速度', '角度', '任务状态', '电量', '升降状态', 'robot状态', '避障', '模式', '在线状态', '数据时间']版本
    _type: str
    id: int
    tag: int
    speed: int
    angle: int
    task_state: int
    soc: int
    soh:int
    up_down_state: int
    robot_state: int
    avoide: int
    mode: int
    is_online: bool
    data_time: int
    软件版本
    总里程

#通讯

#上装


#机械臂

#任务

#时间

#通讯矩阵



@dataclass
class CallDeviceState:
    #['型号', 'ID', '在线状态', '叫料', '放行']
    _type: str
    id: int
    is_online: bool
    call: bool
    let_run: bool

@dataclass
class PadDeviceState:
    #['型号', 'ID', '在线状态', '叫料', '放行']
    _type: str
    id: int
    is_online: bool
    call: bool
    let_run: bool

@dataclass
class LiftAndDoorState:
    #['型号', 'ID', '在线状态', '开门']
    _type: str
    id: int
    is_online: bool
    is_open: bool

@dataclass
class TaskState:
    #['任务ID', 'robot_ID', '起点', '终点', '优先级', '状态']
    id: int
    robot_id: int
    start_point: int
    end_point: int
    priority: int
    state: int

@dataclass
class LogState:
    #['ID', '时间', '模块', '功能']
    id: int
    log_time: int
    module: int
    log_function: int
