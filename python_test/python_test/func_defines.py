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


class EnumDef(bytes, Enum):
    """枚举定义类."""
    def __new__(cls, value, string):
        """
        构造枚举对象.
         
        :param value: int,值
        :param string: str,描述
        :returns: 枚举对象
        :raises: no exception
        """      
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.string = string
        return obj


@unique
class RunState(EnumDef):
    """枚举类：运行状态."""
    OFF = (0, '关机')
    WORK = (1, '运行')
    STANDBY = (2, '待机')
    SLEEP = (3, '休眠')
    STOP = (4, '停机')
    EMERGENCY = (5, '急停')

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

@unique
class ErrLevel(EnumDef):
    """枚举类：故障等级."""
    NONE = (0, '无')
    WARN = (1, '警告')
    LIGHT = (2, '轻微故障')
    SERIOUS = (3, '严重故障')


