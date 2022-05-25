#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
File   Name ： func_defines.py
Description :  常量定义
Author      :  simon
Create Time ： 2022.4.13
-------------------------------------------------------------------------------
Change Activity:
               时间:更改内容
-------------------------------------------------------------------------------
"""
__author__ = 'simon'

from enum import Enum,unique
from datetime import datetime

#classes#######################################################################
#官方示例
class Coordinate(bytes, Enum):
    """
    coordinate with binary codes that can be indexed by the int code.
    """
    PX = (0, 'P.X', 'km')
    PY = (1, 'P.Y', 'km')
    VX = (2, 'V.X', 'km/s')
    VY = (3, 'V.Y', 'km/s')

    def __new__(cls, value, label, unit):    
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.label = label
        obj.unit = unit
        return obj


#class EnumDef(bytes, Enum):
#    """枚举定义类."""
#    def __new__(cls, value, string):
#        """
#        构造枚举对象.
         
#        :param value: int,值
#        :param string: str,描述
#        :returns: 枚举对象
#        :raises: no exception
#        """      
#        obj = bytes.__new__(cls, [value])
#        obj._value_ = value
#        obj.string = string
#        return obj

class EnumDef(Enum):
    """枚举自定义类."""
    def __new__(cls, value, string):
        """
        构造枚举对象.
         
        :param value: int,值
        :param string: str,描述
        :returns: 枚举对象
        :raises: no exception
        """      
      
        obj = object.__new__(cls)
        obj._value_ = value
        obj.string = string
        return obj

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

#有问题
#class EnumDef(Enum):
#    """枚举自定义类."""
#    def __init__(self, value, string):
#        """
#        构造枚举对象.
         
#        :param value: int,值
#        :param string: str,描述
#        :returns: 枚举对象
#        :raises: no exception
#        """            
#        self._value_ = value
#        self.string = string

#    @classmethod
#    def has_value(cls, value):
#        return value in cls._value2member_map_

@unique
class RunState(EnumDef):
    """枚举类：运行状态."""
    OFF = (0, '关机')
    WORK = (1, '运行')
    STANDBY = (2, '待机')
    SLEEP = (3, '休眠')
    STOP = (4, '停机')
    EMERGENCY = (5, '急停')
    NOTASK = (6, '无任务')

@unique
class CtrlMode(EnumDef):
    """枚举类：控制模式."""
    AUTO = (0, '自动')
    MANUAL = (1, '手动')
    REMOTE = (2, '遥控')

@unique
class ConnectState(EnumDef):
    """枚举类：通讯状态."""
    OFFLINE = (0, '离线')
    ONLINE = (1, '在线')
    RECONNECT = (2, '掉线重连')

@unique
class ArmState(EnumDef):
    """枚举类：机械臂状态."""
    WARN = (0, '报警')
    WORK = (1, '运行')
    INPOSITION = (2, '到位')

@unique
class CleanTaskState(EnumDef):
    """枚举类：清扫任务状态."""
    NONE = (0, '无任务')
    WALL1 = (1, '墙面1清洗中')
    WALL2 = (2, '墙面2清洗中')
    WALL3 = (3, '墙面3清洗中')
    WALL4 = (4, '墙面4清洗中')
    GND = (5, '地面清洗中')
    RECHARGE = (6, '中途充电')
    ADDWATER = (7, '中途加水')
    STANDBY = (8, '等待下次任务')
    START = (10, '开始任务')
    BACK = (-1, '结束返回')

@unique
class CleanStateMachine(EnumDef):
    """枚举类：清扫状态机."""
    NONE = (0, '无任务')
    START = (1, '开始清扫')
    CLEANING = (2, '清扫中')
    BACKING = (3, '结束返回中')
    END = (4, '结束')

@unique
class ErrLevel(EnumDef):
    """枚举类：故障等级."""
    NONE = (0, '无')
    WARN = (1, '警告')
    LIGHT = (2, '轻微故障')
    SERIOUS = (3, '严重故障')

@unique
class RfidInfo(EnumDef):
    """枚举类：RFID信息."""
    NONE = (0, '无')
    WATER = (1, '加水点')
    CHARGE = (2, '充电点')
    ARM_CLOSE = (3, '手臂缩回')
    ARM_OPEN = (4, '手臂伸出')
    OTHER = (5, '其他')
    IN_BACK = (11, '内弯后退')
    OUT_BACK = (12, '外弯后退')
    START = (21, '起点')
    END = (22, '终点')
    UNDEFINE = (255, '未定义')

@unique
class PlanType(EnumDef):
    Cycle =(0,"定期执行")
    Once = (1,"指定时间执行")
    Ignore = (2,"指定时间不执行")
    NONE=(3,"无")

@unique
class CycleType(EnumDef):
    Nday = (0,"每N天") 
    Weekday = (1,"每周N")
    Monthday = (2,"每月N日")
    NONE=(3,"无")

@unique
class DriveAction(EnumDef):
    """枚举类：行驶动作."""
    STOP = (0, '停止')
    FORWORD = (1, '前进')
    BACKWORD = (2, '后退')
        

@unique
class ArmAction(EnumDef):
    """枚举类：手臂动作."""
    ORIGIN = (0, '原点')
    WALL1 = (1, '侧壁1')
    WALL2 = (2, '侧壁2')
    WALL3 = (3, '侧壁3')
    WALL4 = (4, '侧壁4')
    GND = (5, '地面')

@unique
class PathPointType(EnumDef):
    """枚举类：路径点类型."""
    NONE = (0, '空')
    CHARGE = (1, '充电点')
    WATER = (2, '加水点')
    RFID = (3, 'RFID点')
    CLEAN = (4, '清扫点')
    

#常量#####################################################################


#时间显示格式
TIME_SHOW_ALL = '%Y-%m-%d %H:%M:%S'
TIME_SHOW_Y_M_D='%Y-%m-%d'
TIME_SHOW_H_M_S = '%H:%M:%S'
DEFAULT_DATETIME_STAMP_START=86400
DATETIME_NONE=datetime.fromtimestamp(DEFAULT_DATETIME_STAMP_START)