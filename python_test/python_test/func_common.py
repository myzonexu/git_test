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
from func_defines import *


#classes#######################################################################
class IdItems(QObject):
    """ID项目组类."""
    #current_inited=pyqtSignal()
    current_changed = pyqtSignal()
    filter_attr_names=["all"]

    def __init__(self):
        """初始化."""
        super().__init__()
        self.all = {}
        self.new = None
        self.current = None
        self.dict_trans={}

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

def set_bit(int_type, offset):
    """
    将某一位置为1.
 
    :param int_type: int，待处理数据
    :param offset: int,要置1的位，最低位为0
    :returns: int,处理后的数据
    :raises: no exception
    """
    mask = 1 << offset
    return(int_type | mask)

def clear_bit(int_type, offset):
    """
    将某一位清除为0.
 
    :param int_type: int，待处理数据
    :param offset: int,要置0的位，最低位为0
    :returns: int,处理后的数据
    :raises: no exception
    """
    mask = ~(1 << offset)
    return(int_type & mask)

def test_bit(int_type, offset):
    """
    测试某一位是否位1.
 
    :param int_type: int，待处理数据
    :param offset: int,要测试的位，最低位为0
    :returns: int,0：否；其他：是
    :raises: no exception
    """
    mask = 1 << offset
    return(int_type & mask)

def join_byte_hi_lo(hi,lo,bit_count):
    """
    组合高低字节.
 
    :param hi: int,高字节
    :param lo: int,低字节
    :param bit_count: int,每个字节位数
    :returns: int,组合后的数据
    :raises: no exception
    """
    return (hi<<bit_count) | lo

def get_bits(int_type, get_low_bit,get_hi_bit):
    """
    取其中连续几位.
 
    :param get_low_bit: int,从第几位开始取
    :param get_hi_bit: int,取至第几位
    :returns: int,处理后的数据
    :raises: no exception
    """
    mask=0
    for i in range(get_hi_bit-get_low_bit+1):
        mask=mask<<1
        mask=mask|1
    int_type=int_type>>get_low_bit
    return (int_type & mask)
   

#时间相关###################################################################
#时间显示格式
#TIME_SHOW_ALL = '%Y-%m-%d %H:%M:%S'
#TIME_SHOW_H_M_S = '%H:%M:%S'

def check_time_info(time):
    """
    检查时间变量，返回信息.
 
    :param time: 时间变量
    :returns: str,时间信息
    :raises: no exception
    """
    if isinstance(time,datetime):
        info_time=time.strftime(TIME_SHOW_ALL)
    elif time==None:
        info_time="--:--:--"
    else:
        info_time="错误时间值"
    return info_time



#装饰器###################################################################
def get_run_time(func):
    """
    装饰器，输出程序执行时间.
 
    :param func: function，函数
    :returns: time,执行时间
    :raises: no exception
    """
    def call_func(*args, **kwargs):
        begin_time = time.time()
        ret = func(*args, **kwargs)
        end_time = time.time()
        Run_time = end_time - begin_time
        print(str(func.__name__)+"函数运行时间为"+str(Run_time))
        return ret
    return call_func

#表格操作####################################################################
def table_fill_data_list_2d(table_widget,list_2d,decimal_places=2,fill="new",checkable=False):
    """
    表格控件填充数据（二维数组）.
 
    :param table_widget: QTableWidget,要填充的表格控件
    :param list_2d: list,二维数组数据
    :param decimal_places: int,表格显示小数位数
    :param fill: str,填充方式："new":从0行填充；"append":保留表格原有显示，追加填充
    :param checkable: bool,第1列是否设置复选框
    :returns: no return
    :raises: no exception
    """
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

def set_table_check_state(table_widget,state,col=0):
    """
    设置表格控件某一列全选或全不选.
 
    :param table_widget: QTableWidget,要设置的表格控件
    :param state: int,要设置的复选框状态，0：不选中；1：部分选中；2：选中
    :param col: int,要设置的列数
    :returns: no return
    :raises: no exception
    """
    for row in range(table_widget.rowCount()):
        if table_widget.item(row,col):
            table_widget.item(row,col).setCheckState(state)

def all_list_str(list,str_join=","):  
    """
    组合list所有元素为字符串.
 
    :param list: list,待组合的列表
    :param str_join: str,组合连接字符串
    :returns: str,组合后的字符串
    :raises: no exception
    """
    return str_join.join('%s' %e for e in list)

def getattr_multilevel(obj,name):
    """
    根据属性名获取对象或子对象属性，子对象属性用'.'分隔.
 
    :param obj: class，对象
    :param name: str,属性名，多级属性用'.'分隔，例：'child.attrname'
    :returns: 属性值
    :raises: no exception
    """
    name_list=name.split(".")
    if len(name_list)==1:
        return getattr(obj,name_list[0])
    else:
        _obj=obj
        for _name in name_list:
            _obj=getattr(_obj,_name)
            if _obj is None:
                break

        return _obj

def setattr_multilevel(obj,name,value):
    """
    根据属性名设置对象或子对象属性值，子对象属性用'.'分隔.
 
    :param obj: class，对象
    :param name: str,属性名，多级属性用'.'分隔，例：'child.attrname'
    :param value: 对象值
    :returns: no returns
    :raises: no exception
    """
    name_list=name.split(".")
    print(name_list)
    if len(name_list)==1:
        return setattr(obj,name_list[0],value)
    else:
        _obj=obj
        for _name in name_list:
            _obj=getattr(_obj,_name)
            #if _obj is None:
            #    break
        _obj=value


def get_export_attr_names(name_class_export_attr="export_attr_names"):
    """
    获取类及子对象的导出属性名.
 
    :param name_class_export_attr: str,类及子对象存储导出属性名的变量名
    :param param2: this is a second param
    :returns: list,类导出属性名list
    :raises: no exception
    """
    pass
    

def str_list_add_prefix_suffix(str_list,str_add,str_join=".",prefix=True):
    """
    字符串列表内每个字符串增加前缀或后缀.
 
    :param str_list: list,待处理字符串列表
    :param str_add: str,增加的前缀或后缀
    :param str_join: str,连接字符串
    :param prefix: bool,前缀还是后缀，True:前缀；False:后缀
    :returns: str,处理后的字符串
    :raises: no exception
    """
    _str_list=[]
    if prefix is True:
        for _str in str_list:
            _str_list.append(str_add+str_join+_str)
    else:
        for _str in str_list:
            _str_list.append(_str+str_join+str_add)
    return _str_list

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