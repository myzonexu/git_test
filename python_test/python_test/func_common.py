#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
File   Name ： func_common.py
Description :  通用函数实现
Author      :  simon
Create Time ： 20220105
-------------------------------------------------------------------------------
Change Activity:
               时间:更改内容
-------------------------------------------------------------------------------
"""
__author__ = 'simon'


from datetime import datetime,timedelta
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#classes#######################################################################
class IdItems(QObject):
    """ID项目组类."""
    #current_inited=pyqtSignal()
    current_changed = pyqtSignal()

    def __init__(self):
        """初始化."""
        super().__init__()
        self.all = {}
        self.new = None
        self.current = None

    def set_current(self,id):        
        if id in self.all:        
            self.current = self.all.get(id)
            self.current_changed.emit(id)
            print("当前id为：",id)
            return self.current            
        else:
            print("无法找到id")
            return None

    
    def add(self,item):
        """
        增加项目成员.
     
        :param item: 要增加的项目成员
        :returns: no return
        :raises: no exception
        """
        pass
    
    def delete(self,id):
        """
        删除项目成员.
     
        :param item: 要删除的项目成员id
        :returns: no return
        :raises: no exception
        """
        pass

    def list_info(self):
        list_info = []
        if self.all == {}:
            #print("no info")
            pass
        else:
            for id,item in self.all.items():
                list_info.append([f'{id:>10}'])
                    
        return list_info


#位操作######################################################################
#offset从0开始
#将某一位置为1
def set_bit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)
#将某一位清除为0
def clear_bit(int_type, offset):
    mask = ~(1 << offset)
    return(int_type & mask)
#测试某一位是否位1
def test_bit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)
#组合高低字节
def join_byte_hi_lo(hi,lo,bit_count):
    return (hi<<bit_count) | lo
#取其中连续几位
def get_bits(int_type, get_low_bit,get_hi_bit):
    mask=0
    for i in range(get_hi_bit-get_low_bit+1):
        mask=mask<<1
        mask=mask|1
    int_type=int_type>>get_low_bit
    return (int_type & mask)

    #n=int_type<<(15-get_hi_bit)
    #n=n>>get_low_bit
    #return n

#时间相关###################################################################
#时间显示格式
TIME_SHOW_ALL = '%Y-%m-%d %H:%M:%S'
TIME_SHOW_H_M_S = '%H:%M:%S'

#检查时间变量，返回信息
def check_time_info(time):
    if isinstance(time,datetime):
        info_time=time.strftime(TIME_SHOW_ALL)
    elif time==None:
        info_time="--:--:--"
    else:
        info_time="错误时间值"
    return info_time

import time

#装饰器###################################################################
#输出程序执行时间
def get_run_time(func):
    def call_func(*args, **kwargs):
        begin_time = time.time()
        ret = func(*args, **kwargs)
        end_time = time.time()
        Run_time = end_time - begin_time
        print(str(func.__name__)+"函数运行时间为"+str(Run_time))
        return ret
    return call_func

#表格操作####################################################################
#表格填充数据-二维数组
def table_fill_data_list_2d(table_widget,list_2d,decimal_places=2,fill="new",checkable=False):
    if fill=="new":
        start_row=0
    elif fill=="append":
        start_row=table_widget.rowCount()

    if list_2d==[]:
        table_widget.clearContents()
        table_widget.setRowCount(0)
    elif list_2d==[[]]:
        table_widget.clearContents()
        table_widget.setRowCount(0)

    else:
        len_row=len(list_2d)
        len_col=len(list_2d[0])
        table_widget.setRowCount(start_row+len_row)
        table_widget.setColumnCount(len_col)
        for row in range(len_row):
            for col in range(len_col):
                data=list_2d[row][col]            
                if isinstance(data,float):
                    data=round(data,decimal_places)
                item=QTableWidgetItem(str(data))
                table_widget.setItem(start_row+row,col,item)
        if checkable is True:
            for row in range(len_row):
                    table_widget.item(row,0).setCheckState(Qt.Unchecked)
        else:
            pass
    table_widget.viewport().update()

def set_table_check_state(table,state,col=0):
        """设置表格全选全不选."""
        for row in range(table.rowCount()):
            if table.item(row,col):
                table.item(row,col).setCheckState(state)



#list所有元素组合为字符串
def all_list_str(list,str_join=","):    
    return str_join.join('%s' %e for e in list)




#日志
class LogEvent(object):
    def __init__(self):
        self.type = ValueDescriptionSet(log_type)
        self.time=datetime(2000,1,1)
        self.event=""


class Log(object):
    def __init__(self):
        #LogEvent列表
        self.log_list=[]
        
    def type_count(self,log_type,time_start=datetime(2000,1,1)):
        count=0
        #do
        return count