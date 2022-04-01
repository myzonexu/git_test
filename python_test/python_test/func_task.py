#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
File   Name ： func_task.py
Description :  任务调度
Author      :  simon
Create Time ： 2022.03.10
-------------------------------------------------------------------------------
Change Activity:
               时间:更改内容
-------------------------------------------------------------------------------
"""
__author__ = 'simon'

from datetime import datetime
from enum import Enum,unique

#classes#######################################################################
@unique
class PlanType(Enum):
    Cycle = 0 
    Once = 1
    Ignore = 2

@unique
class CycleType(Enum):
    Nday = 0 
    Weekday = 1
    Monthday = 2
    
class PlcDatetime(datetime):
    """PLC时间类."""
    pass

class TaskPlan(object):
    """计划任务类."""
    def __init__(self,name,type,datetime_set):
        """
        初始化.
         
        :param name: 计划任务名称
        :param type: 计划任务类型
        :param type: 计划任务时间
        :returns: no return
        :raises: no exception
        """
    
        self.name=name
        self.type=type
        self.datetime_set=datetime_set

    
    def init_id(self):
        """
        初始化id.
    
        :returns: id
        :raises: no exception
        """
        self.id=""
        return self.id

class DatetimeCycle(object):
    """周期执行类."""
    def __init__(self,type,cycle,do_time,start_time,end_time):
        """
        初始化.
         
        :param type: 周期类型
        :param cycle: 周期间隔
        :param do_time: 执行时间
        :param start_time: 起始时间
        :param end_time: 截止时间
        :returns: no return
        :raises: no exception
        """
     
        self.type=type
        self.cycle=cycle
        self.do_time=do_time
        self.start_time=start_time
        self.end_time=end_time
    
    def datetime_str(self):
        """
        时间说明.
    
        :returns: 时间说明string
        :raises: no exception
        """
        pass

class DatetimeOnce(object):
    """指定时间执行类."""
    def __init__(self,do_time): 
        """
        初始化.
         
        :param do_time: 执行时间
        :returns: no return
        :raises: no exception
        """
        self.do_time=do_time

    def datetime_str(self):
        """
        时间说明.
    
        :returns: 时间说明string
        :raises: no exception
        """
        pass

class DatetimeIgnore(object):
    """指定时间不执行类."""
    
    def __init__(self,start_time,end_time):
        """
        初始化.
     
        :param start_time: 起始时间
        :param end_time: 截止时间
        :returns: no return
        :raises: no exception
        """
        self.start_time=start_time
        self.end_time=end_time
    
    def datetime_str(self):
        """
        时间说明.
    
        :returns: 时间说明string
        :raises: no exception
        """
        pass






