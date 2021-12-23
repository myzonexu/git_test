from datetime import datetime,timedelta
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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
    return (hi<<bit_count | lo)

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


#表格操作####################################################################
#表格填充数据-二维数组
def table_fill_data_list_2d(table_widget,list_2d,decimal_places=2,fill="new"):
    if fill=="new":
        start_row=0
    elif fill=="append":
        start_row=table_widget.rowCount()

    if list_2d==[]:
        table_widget.clearContents()
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
    table_widget.viewport().update()


#日志
class LogEvent(object):
    def __init__(self):
        self.type = ValueDescriptionSet(log_type)
        self.time=datetime(2000,1,1)
        self.event=""


class LogState(object):
    def __init__(self):
        #LogEvent列表
        self.log_list=[]
        
    def type_count(self,log_type,time_start=datetime(2000,1,1)):
        count=0
        #do
        return count