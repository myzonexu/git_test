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
from PyQt5.QtCore import QTime,QDate
import random
from func_common import *


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
    
        self.id = random.randint(0,65530)
        self.name=name
        self.type=type
        self.datetime_set=datetime_set

        self.assign=[1,2,3]
        self.received=[1]
        self.not_received=[2,3]
        self.received_progress=0.0
        self.add_time=None

    
    def is_plan_date(self,date):
        """
        判断某一日期是否执行计划.
     
        :param date: QDate()判断日期
        :returns: 0：否，1：是，2：排除
        :raises: no exception
        """
        if self.type is PlanType.Cycle.value:
            if self.datetime_set.type is CycleType.Nday:
                if self.datetime_set.start_date.daysTo(date)%self.datetime_set.cycle==0:
                    return 1
                else:
                    return 0
            elif self.datetime_set.type is CycleType.Weekday:
                if date.dayOfWeek()==self.datetime_set.cycle:
                    return 1
                else:
                    return 0
            elif self.datetime_set.type is CycleType.Monthday:
                if date.day()==self.datetime_set.cycle:
                    return 1
                else:
                    return 0
            
        elif self.type is PlanType.Once.value:
            if date.__eq__(self.datetime_set.do_date):
                return 1
            else:
                return 0

        elif self.type is PlanType.Ignore.value:
            if date.__ge__(self.datetime_set.start_date) and date.__le__(self.datetime_set.end_date):
                return 2
            else:
                return 0


class DatetimeCycle(object):
    """周期执行类."""
    def __init__(self,type,cycle,do_time=QTime()):
        """
        初始化.
         
        :param type: 周期类型
        :param cycle: 周期间隔
        :param do_time: 执行时间
        :returns: no return
        :raises: no exception
        """
     
        self.type=type
        self.cycle=cycle
        self.do_time=do_time
        self.start_date=None
        self.end_date=None
    
    def datetime_str(self):
        """
        时间说明.
    
        :returns: 时间说明string
        :raises: no exception
        """              
        if self.end_date is None:
            self.valid_time_str=f'从{self.start_date.toString("yyyy/MM/dd")}之后'
          
        else:
            self.valid_time_str=f'从{self.start_date.toString("yyyy/MM/dd")}至{self.end_date.toString("yyyy/MM/dd")}'
        
        if self.type is CycleType.Nday:
            self.cycle_str=f'每{self.cycle}天'
        elif self.type is CycleType.Weekday:
            _weekday_str_list=["一","二","三","四","五","六","日"]
            self.cycle_str=f'每周{_weekday_str_list[self.cycle]}'
        elif self.type is CycleType.Monthday:
            self.cycle_str=f'每月{self.cycle}日'

        self.str_datetime=f'{self.valid_time_str}，{self.cycle_str}的{self.do_time.toString("hh:mm")}执行'
        return self.str_datetime

class DatetimeOnce(object):
    """指定时间执行类."""
    def __init__(self,do_date,do_time): 
        """
        初始化.
         
        :param do_time: 执行时间
        :returns: no return
        :raises: no exception
        """
        self.do_date=do_date
        self.do_time=do_time

    def datetime_str(self):
        """
        时间说明.
    
        :returns: 时间说明string
        :raises: no exception
        """
        self.str_datetime=f'在{self.do_date.toString("yyyy/MM/dd")}的{self.do_time.toString("hh:mm")}执行'
        return self.str_datetime

class DatetimeIgnore(object):
    """指定时间不执行类."""
    
    def __init__(self,start_date,end_date):
        """
        初始化.
     
        :param start_date: 起始时间
        :param end_time: 截止时间
        :returns: no return
        :raises: no exception
        """
        self.start_date=start_date
        self.end_date=end_date
    
    def datetime_str(self):
        """
        时间说明.
    
        :returns: 时间说明string
        :raises: no exception
        """
        self.str_datetime=f'在{self.start_date.toString("yyyy/MM/dd")}至{self.end_date.toString("yyyy/MM/dd")}期间不执行'
        return self.str_datetime

class TaskPlans(object):
    """计划任务列表类."""
    
    def __init__(self):
        """初始化."""
        self.new_plan=None
        self.plan_list=[]

    def list_info(self):
        list_info = []
        str_plan_type=["周期执行","指定时间执行","指定时间不执行"]
        if self.plan_list == []:
            pass
        else:               
            for plan in self.plan_list:
                list_info.append([plan.id,plan.name,str_plan_type[plan.type],plan.datetime_set.datetime_str(),\
                    all_list_str(plan.assign),all_list_str(plan.received),plan.received_progress,\
                    plan.add_time.strftime("%Y-%m-%d %H:%M:%S")])
        return list_info

#functions#####################################################################
def set_calendar_date_format(calendar,date,color):
    """
    设定日历部件某个日期背景颜色.
     
    :param calendar: QCalendar()日历部件
    :param date: QDate()设定日期
    :param color: str设定颜色
    :returns: no return
    :raises: no exception
    """
    fmt = QTextCharFormat()
    brush = QBrush()
    brush.setColor(QColor(color))
    fmt.setBackground(brush)
    calendar.setDateTextFormat(date,fmt)
    

def mark_calendar_plan_date(calendar,task_plan):
    """
    标记日历中计划执行日期.
     
    :param calendar: QCalendar()日历部件
    :param task_plan: 计划任务
    :returns: no return
    :raises: no exception
    """
    days=QDate(calendar.yearShown(),calendar.monthShown(),1).daysInMonth()
    print(days)
    for day in range(1,days+1):
        date=QDate(calendar.yearShown(),calendar.monthShown(),day)
        if task_plan.is_plan_date(date)==1:
            set_calendar_date_format(calendar,date,"green")
        elif task_plan.is_plan_date(date)==2:
            set_calendar_date_format(calendar,date,"yellow")

   



task_plans=TaskPlans()
