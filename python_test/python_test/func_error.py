#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
File   Name ： func_error.py
Description :  故障
Author      :  simon
Create Time ： 2022.5.19
-------------------------------------------------------------------------------
Change Activity:
               时间:更改内容
-------------------------------------------------------------------------------
"""
__author__ = 'simon'

from datetime import datetime,timedelta
from func_defines import *
from func_export import *


#classes#######################################################################
class ErrorCode(object):
    #error_dict={"code1":[code,level,description,solution],"code2":[code,level,description,solution]}
    error_dict={}
    _index_code=0
    _index_level=1
    _index_description=2
    _index_solution=3

    def __init__(self,code):
        if isinstance(code,str):
            self.code = code
        elif isinstance(code,int):
            self.code = str(code)
        else:
            print(f"故障码应为str类型")

    @property
    def level(self):
        if ErrorCode.error_dict.get(self.code):
            #return ErrorCode.error_dict.get(self.code).get("level")
            return ErrorCode.error_dict.get(self.code)[ErrorCode._index_level]
        else:
            return "--" 

    @property
    def description(self):
        if ErrorCode.error_dict.get(self.code):
            #return ErrorCode.error_dict.get(self.code).get("description")
            return ErrorCode.error_dict.get(self.code)[ErrorCode._index_description]
        else:
            return "--"        

    @property
    def solution(self):
        if ErrorCode.error_dict.get(self.code):
            #return ErrorCode.error_dict.get(self.code).get("solution")
            return ErrorCode.error_dict.get(self.code)[ErrorCode._index_solution]
        else:
            return "--"  
        
    @classmethod
    def import_file(cls,file):
        """
        从文件导入故障码.       
     
        :param file: str,导入文件路径，csv格式
        :returns: no return
        :raises: no exception
        """
        header,rows=import_csv(file)
        if header:
            cls._index_code=header.index("code")
            cls._index_level=header.index("level")
            cls._index_description=header.index("description")
            cls._index_solution=header.index("solution")

            for _row in rows:
                cls.error_dict[_row[cls._index_code]]=_row


class ErrorEvent(object):
    def __init__(self,code):
        self.error=ErrorCode(code)
        self.is_active=True
        self.time_start = datetime.now()
        self.time_stop = datetime.fromtimestamp(DEFAULT_DATETIME_STAMP_START)
    
    def stop(self):
        """
        故障结束.
    
        :returns: no return
        :raises: no exception
        """
        self.time_stop = datetime.now()
        self.is_active=False

class Error(object):
    def __init__(self):
        #self.all={}
        self.active = {}
        self.history = []

    @property
    def active_count(self):
        """
        现行故障数量.
    
        :returns: int,现行故障数量
        :raises: no exception
        """
        return len(self.active)

    @property
    def history_count(self):
        """
        历史故障数量.
    
        :returns: int,历史故障数量
        :raises: no exception
        """
        return len(self.history)

    def recv_code(self,code_list):
        """
        接收处理故障列表.
            
        :param code_list: list,接收到的故障码列表
        :returns: no return
        :raises: no exception
        """
        _active=set(self.active.keys())
        _new=set(code_list)

        _stop=_active-_new        
        _add=_new-_active

        for _code in _add:
            self.active[_code]=ErrorEvent(_code)

        for _code in _stop:
            _event=self.active.get(_code)
            _event.stop()
            self.active.pop(_code)
            self.history.append(_event)

    def clear_history(self):
        """清除历史故障."""
        self.history.clear()

    @property
    def active_err_info(self):
        """获取现行故障表格信息."""
        _infos=[]
        for _code,_err in self.active.items():
            _info=["现行",_err.error.level,_err.error.code,_err.error.description,_err.error.solution,_err.time_start.strftime(TIME_SHOW_ALL),"--"]
            _infos.append(_info)

        return _infos

    @property
    def history_err_info(self): 
        """获取历史故障表格信息."""
        _infos=[]
        for _err in self.history:
            _info=["历史",_err.error.level,_err.error.code,_err.error.description,_err.error.solution,_err.time_start.strftime(TIME_SHOW_ALL),_err.time_stop.strftime(TIME_SHOW_ALL)]
            _infos.append(_info)
        
        return _infos




ErrorCode.import_file('./data/error_code.csv')



