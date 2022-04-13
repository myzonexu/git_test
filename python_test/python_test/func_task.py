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
               2022.4.11:计划类合并为1个类
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

class TaskPlan(object):
    """计划任务类."""
    def __init__(self):
        """
        初始化.
         
        :param name: 计划任务名称
        :param type: 计划任务类型
        :param type: 计划任务时间
        :returns: no return
        :raises: no exception
        """
    
        self.id = 0
        self.enable = False
        self.name = ""
        #PlanType枚举
        self.plan_type = None
        #self.datetime_set=datetime_set
        #CycleType枚举
        self.cycle_type = None
        self.cycle_value = 0
        self.do_time = QTime()
        self.start_date = QDate()
        self.end_date = QDate()
        self.str_plan_time = ""

        self.assign = [1,2,3]
        self.received = [1]
        self.not_received = [2,3]
        self.received_progress = 0.0
        self.add_time = None
    
    def init_id(self):
        """初始化id,1~65530随机数."""
        self.id = random.randint(1,65530)
        return self.id

    def plan_time_str(self):        
        """
        计划时间说明.
    
        :returns: 时间说明string
        :raises: no exception
        """  
        self.str_plan_time = ""
        valid_time_str = ""
        cycle_str = ""

        if self.plan_type is PlanType.Cycle:
            if self.end_date.isNull():
                valid_time_str = f'从{self.start_date.toString("yyyy/MM/dd")}之后'          
            else:
                valid_time_str = f'从{self.start_date.toString("yyyy/MM/dd")}至{self.end_date.toString("yyyy/MM/dd")}'
        
            if self.cycle_type is CycleType.Nday:
                cycle_str = f'每{self.cycle_value}天'
            elif self.cycle_type is CycleType.Weekday:
                _weekday_str_list = ["一","二","三","四","五","六","日"]
                cycle_str = f'每周{_weekday_str_list[self.cycle_value]}'
            elif self.cycle_type is CycleType.Monthday:
                cycle_str = f'每月{self.cycle_value}日'

            self.str_plan_time = f'{valid_time_str}，{cycle_str}的{self.do_time.toString("hh:mm")}执行'

        elif self.plan_type is PlanType.Once:
            self.str_plan_time = f'在{self.start_date.toString("yyyy/MM/dd")}的{self.do_time.toString("hh:mm")}执行'

        elif self.plan_type is PlanType.Ignore:
            self.str_plan_time = f'在{self.start_date.toString("yyyy/MM/dd")}至{self.end_date.toString("yyyy/MM/dd")}期间不执行'

        else:
            pass

        return self.str_plan_time
    
    def is_cycle_day(self,date):
        """
        判断某一日期是否是周期日期.
     
        :param date: QDate()判断日期
        :returns: True:是；False:否
        :raises: no exception
        """
        if self.cycle_type is CycleType.Nday:
            if self.start_date.daysTo(date) % self.cycle_value == 0:
                return True
            else:
                return False
        elif self.cycle_type is CycleType.Weekday:
            if date.dayOfWeek() == self.cycle_value:
                return True
            else:
                return False
        elif self.cycle_type is CycleType.Monthday:
            if date.day() == self.cycle_value:
                return True
            else:
                return False
    
    def is_plan_date(self,date):
        """
        判断某一日期是否执行计划.
     
        :param date: QDate()判断日期
        :returns: 0：否，1：是，2：排除
        :raises: no exception
        """
        if self.plan_type is PlanType.Cycle:
            if date.__lt__(self.start_date):
                return 0
            else:
                if self.end_date.isNull():
                    if self.is_cycle_day(date):
                        return 1
                    else:
                        return 0
                else:
                    if date.__gt__(self.end_date):
                        return 0
                    else:
                        if self.is_cycle_day(date):
                            return 1
                        else:
                            return 0
            
        elif self.plan_type is PlanType.Once:
            if date.__eq__(self.start_date):
                return 1
            else:
                return 0

        elif self.plan_type is PlanType.Ignore:
            if date.__ge__(self.start_date) and date.__le__(self.end_date):
                return 2
            else:
                return 0


class TaskPlans(object):
    """计划任务列表类."""
    
    def __init__(self):
        """初始化."""
        self.new_plan = TaskPlan()
        self.plan_list = []

    def list_info(self):
        list_info = []
        str_plan_type = ["周期执行","指定时间执行","指定时间不执行"]
        if self.plan_list == []:
            pass
        else:               
            for plan in self.plan_list:
                list_info.append([plan.id,plan.name,str_plan_type[plan.plan_type.value],plan.plan_time_str(),\
                    all_list_str(plan.assign),all_list_str(plan.received),plan.received_progress,\
                    plan.add_time.strftime("%Y-%m-%d %H:%M:%S")])
        return list_info

#functions#####################################################################
def set_calendar_date_format(calendar,date,color,tooltip=""):
    """
    设定日历部件某个日期背景颜色，提示信息.
     
    :param calendar: QCalendar(),日历部件
    :param date: QDate(),设定日期
    :param color: str,设定颜色
    :param tooltip: str,提示信息
    :returns: no return
    :raises: no exception
    """

    fmt = QTextCharFormat()
    brush = QBrush()
    brush.setColor(QColor(color))
    fmt.setBackground(brush)
    fmt.setToolTip(tooltip)
    calendar.setDateTextFormat(date,fmt)

def clear_calendar_date_format(calendar,date):
    """
    清空日历部件某个日期显示.
     
    :param calendar: QCalendar(),日历部件
    :param date: QDate(),设定日期
    :returns: no return
    :raises: no exception
    """
    fmt_clear = calendar.dateTextFormat(QDate())
    calendar.setDateTextFormat(date,fmt_clear)  

def mark_calendar_plan_date(calendar,task_plan,clear_old_format=True):
    """
    标记日历中计划执行日期.
     
    :param calendar: QCalendar(),日历部件
    :param task_plan: 计划任务
    :param clear_old_format: True:清除日历原有格式；False:保留日历原有格式
    :returns: no return
    :raises: no exception
    """

    date_1 = QDate(calendar.yearShown(),calendar.monthShown(),1)
    for i in range(-7,38):
        date = date_1.addDays(i)
        if clear_old_format is True:
            calendar.setDateTextFormat(date,QTextCharFormat()) 
        else:
            pass

        if task_plan.is_plan_date(date) == 1:
            set_calendar_date_format(calendar,date,"green",task_plan.do_time.toString("hh:mm"))
        elif task_plan.is_plan_date(date) == 2:
            set_calendar_date_format(calendar,date,"yellow")



task_plans = TaskPlans()
