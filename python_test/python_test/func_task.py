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
from func_defines import *
from func_export import *
import copy
import json

#classes#######################################################################
#@unique
#class PlanType(Enum):
#    Cycle = 0 
#    Once = 1
#    Ignore = 2
#    NONE=3

#@unique
#class CycleType(Enum):
#    Nday = 0 
#    Weekday = 1
#    Monthday = 2
#    NONE=3

class TaskPlan(object):
    """计划任务类."""

    filter_attr_names=["id","enable","name","plan_type","cycle_type","cycle_value","do_time","start_date","end_date","assign","received","add_time"]
    def __init__(self):
        """
        初始化.
         
        :param name: 计划任务名称
        :param type: 计划任务类型
        :param type: 计划任务时间
        :returns: no return
        :raises: no exception
        """
        self.value_type_dict={"assign":{"type":str},"received":{"type":str},"not_received":{"type":str}}

        self.id = 0
        self.enable = False
        self.name = ""
        #PlanType枚举
        self.plan_type = PlanType.NONE
        #CycleType枚举
        self.cycle_type = CycleType.NONE
        self.cycle_value = 0
        self.do_time = QTime()
        self.start_date = QDate()
        self.end_date = QDate()
        self.str_plan_time = ""

        self.assign = set([])
        self.received = set([])
        self.not_received = set([])
        self.received_progress = 0.0
        self.add_time = datetime.now()
        self.message_frame = []
        self.check_state = False

        self.info_output = ""
    
    def init_id(self):
        """初始化id,1~32760随机数."""
        if self.id == 0:
            self.id = random.randint(1,32760)
        else:
            pass
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
                cycle_str = f'每周{_weekday_str_list[self.cycle_value-1]}'
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
    
    def get_received_progress(self):
        """
        获取下发进度.
    
        :returns: float,下发进度百分比
        :raises: no exception
        """
        if len(self.assign)==0:
            self.received_progress=0.0
        else:
            self.received_progress=len(self.received)/len(self.assign)
        return self.received_progress
    
    def get_not_received(self):
        """
        获取未下发机器人.
    
        :returns: set,未下发机器人
        :raises: no exception
        """
        self.not_received=self.assign-self.received
        return self.not_received
    
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

    
    def get_message_frame(self,frame_len=20):
        """
        生成通讯数据.
    
        :param len: int 数据长度
        :returns: 通讯数据数组
        :raises: no exception
        """
        self.message_frame = [self.id,int(self.enable),self.plan_type.value,self.cycle_type.value,self.cycle_value,\
            self.do_time.hour(),self.do_time.minute(),\
            self.start_date.year(),self.start_date.month(),self.start_date.day(),\
            self.end_date.year(),self.end_date.month(),self.end_date.day()]
        for i in range(frame_len - len(self.message_frame)):
            self.message_frame.append(0)
        #print(self.message_frame)
        return self.message_frame
    
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
    
    def output_info(self):
        """
        输出下发信息.
    
        :returns: str,信息内容
        :raises: no exception
        """
        self.info_output=""
        return self.info_output

    
    #def export(self):
    #    """
    #    导出数据.
    
    #    :returns: dict,数据字典
    #    :raises: no exception
    #    """
    #    #export_name=["id","enable","name","plan_type","cycle_type","cycle_value","do_time","start_date","end_date","assign","received","add_time"]
    #    export_dict={}
    #    for name in self.export_name:
    #        attr=getattr(self, name,None)
    #        if isinstance(attr,(QDate,)):
    #            export_dict[name]=attr.toString("yyyy/MM/dd")
    #        elif isinstance(attr,(QTime,)):
    #            export_dict[name]=attr.toString("hh:mm")
    #        elif isinstance(attr,(datetime,)):
    #            export_dict[name]=attr.strftime("%Y-%m-%d %H:%M:%S")
    #        elif isinstance(attr,(Enum,)):
    #            export_dict[name]=attr.value
    #        elif isinstance(attr,(set,)):
    #            export_dict[name]=list(attr)
    #        else:
    #            export_dict[name]=attr
    #    return export_dict

    #@staticmethod
    #def json_hook(dct):
    #    pass
        
    #    return None


class TaskPlans(QObject):
    """计划任务列表类."""
    #current_inited=pyqtSignal()
    current_changed = pyqtSignal()
    filter_attr_names=["all"]

    def __init__(self):
        """初始化."""
        super().__init__()
        self.value_type_dict={"all":{"type":TaskPlan,"key":"id"}}
        self.new = TaskPlan()
        #self.plan_list = []
        self.all = {}
        self.current = None
        self.dict_trans={}
        
        import os
        filename = './data/task_plans.json'
        if os.path.exists(filename): 
            self.import_json_file(filename)
            self.import_json_plans()


    def set_current(self,id):        
        if id in self.all:        
            self.current = self.all.get(id)
            self.current_changed.emit(id)
            print("当前id为：",id)
            return self.current
            
        else:
            print("无法找到id")
            return None

    
    
    def enable_checked(self,enable):
        """
        开启、关闭选中任务.
     
        :param enable: bool,开启、关闭
        :returns: no return
        :raises: no exception
        """
        for id,item in self.all.items():
            if item.check_state is True:
                item.enable=enable
            else:
                pass
    
    def del_checked(self):
        """
        删除选中任务.
    
        :returns: no return
        :raises: no exception
        """
        for id in list(self.all.keys()):
            if self.all.get(id).check_state is True:
                self.all.pop(id)
            else:
                pass

    def list_info(self):
        list_info = []
        str_plan_type = ["周期执行","指定时间执行","指定时间不执行"]
        if self.all == {}:
            #print("no info")
            pass
        else:
            count = len(self.all)       
            for id,item in self.all.items():
                list_info.append([f'{id}',item.enable,item.name,str_plan_type[item.plan_type.value],item.plan_time_str(),\
                    all_list_str(item.assign),all_list_str(item.get_not_received()),f'{item.get_received_progress():.0%}',item.info_output,\
                    item.add_time.strftime("%Y-%m-%d %H:%M:%S")])
                    
        return list_info

    
    def import_json_file(self,file):
        """
        导入json文件.
     
        :param file: file,json文件地址
        :returns: no return
        :raises: no exception
        """
        with open(file, 'r') as f:
            self.dict_trans=json.load(f)

    def import_json_plans(self):
        """
        从json导入计划任务.
     
        :returns: no return
        :raises: no exception
        """
        _plans=self.dict_trans.get("task_plans").get("all")
        if _plans:
            for _id,_plan in _plans.items():
                json_to_obj(_plan,self.new)
                self.all[_id]=copy.deepcopy(self.new)
            self.new.__init__()

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

def mark_calendar_plans_date(calendar,task_plans,clear_old_format=True):
    """
    标记日历中多个计划执行日期.
     
    :param calendar: QCalendar(),日历部件
    :param task_plans: dict,多个计划任务
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
        for id,item in task_plans.items():
            if item.check_state and item.enable:
                if item.is_plan_date(date) == 2:
                    set_calendar_date_format(calendar,date,"yellow")
                    break
                elif item.is_plan_date(date) == 1:
                    set_calendar_date_format(calendar,date,"green",item.do_time.toString("hh:mm"))
        


task_plans = TaskPlans()
