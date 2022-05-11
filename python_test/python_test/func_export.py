#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
File   Name ： func_export.py
Description :  导入导出，配置文件
Author      :  simon
Create Time ： 2022.4.26
-------------------------------------------------------------------------------
Change Activity:
               时间:更改内容
-------------------------------------------------------------------------------
"""
__author__ = 'simon'

import csv
import json
from enum import *
from func_common import *
from func_defines import *

def import_csv(file):
    """
    导入csv文件.
 
    :param file: str,文件路径
    :param head: this is a second param
    :returns: list,list:表头,行内容
    :raises: no exception
    """
    with open(file, newline='') as f:
        f_csv = csv.reader(f)
        header = next(f_csv)
        rows = []
        for row in f_csv:
            rows.append(row)
        #print(header)
        #print(rows)
    return header,rows

def export_csv(file,header,rows):
    """
    导出csv文件.
 
    :param file: str,文件路径
    :param header: list,表头
    :param rows: list,行内容,list成员可为list或dict
    :returns: no return
    :raises: no exception
    """
    with open(file,'w',newline='') as f:
        if len(rows) == 0:
            print("空数据")
        elif type(rows[0]) is list:
            #print("list数据")
            f_csv = csv.writer(f)
            f_csv.writerow(header)
            f_csv.writerows(rows)
        elif type(rows[0]) is dict:
            #print("dict数据")
            f_csv = csv.DictWriter(f,header)
            f_csv.writeheader()
            f_csv.writerows(rows)
        else:
            pass

#head,rows=import_csv('./data/config_robot1.csv')
#export_csv('./data/config_robot2.csv',head,rows)
'''
def obj_attr_to_json_dict(obj,attr_names):
    """
    对象属性导出json数据dict.

    :param obj: 要导出的对象
    :param attr_names: list,要导出的属性名列表
                       list元素：str，属性名
                       多级子对象属性用'.'分隔，例：'child.attrname'
    :returns: dict,数据字典
    :raises: no exception
    """
    export_dict={}
    for name in attr_names:
        attr=getattr_multilevel(obj, name)
        if isinstance(attr,(QDate,)):
            export_dict[name]=attr.toString("yyyy/MM/dd")
        elif isinstance(attr,(QTime,)):
            export_dict[name]=attr.toString("hh:mm")
        elif isinstance(attr,(datetime,)):
            export_dict[name]=attr.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(attr,(timedelta,)):
            export_dict[name]=str(attr)
        elif isinstance(attr,(enum,)):
            export_dict[name]=attr.value
        elif isinstance(attr,(set,)):
            export_dict[name]=list(attr)
        else:
            export_dict[name]=attr
    return export_dict

def objs_to_json_dict(objs,key_objs,attr_names):
    """
    同类型对象集导出json数据dict，导出json示例:
    {key_objs:[{dict_obj1},{dict_obj2},...{dict_objn}]} .
 
    :param objs: list/dict,对象集，可为list或dict，对象同类型
    :param key_objs: str,对象集名称
    :returns: dict,转换的json dict
    :raises: no exception
    """
    json_obj_list=[]
    json_dict={}

    if type(objs) is list:
        for obj in objs:
            json_obj_list.append( obj_attr_to_json_dict(obj,attr_names))
    elif type(objs) is dict:
        for obj in objs.values():
            json_obj_list.append( obj_attr_to_json_dict(obj,attr_names))
    else:
        print("对象集非list或dict")

    json_dict[key_objs]=json_obj_list
    return json_dict
def obj_all_to_json_dict(obj):
    """
    对象所有属性导出json数据dict.

    :param obj: 要导出的对象
    :returns: dict,json数据字典
    :raises: no exception
    """
    for name,value in obj.__dict__:
        pass


def obj_to_json_dict(obj,select="export_attr_names",*,export_all=False):
    """
    对象导出json数据dict.

    :param obj: 要导出的对象
    :param select: str,对象选择要导出的属性名列表名称，默认为类定义的cls.export_attr_names，
                       若无cls.export_attr_names，导出所有属性
    :param export_all: bool,True:导出对象所有属性；False:只导出cls.export_attr_names列表内的属性
    :returns: dict,json数据字典
    :raises: no exception
    """

    attr_names=getattr(obj.__class__,select)

    export_dict={}
    for name in attr_names:
        attr=getattr_multilevel(obj, name)
        if isinstance(attr,(QDate,)):
            export_dict[name]=attr.toString("yyyy/MM/dd")
        elif isinstance(attr,(QTime,)):
            export_dict[name]=attr.toString("hh:mm")
        elif isinstance(attr,(datetime,)):
            export_dict[name]=attr.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(attr,(Enum,)):
            export_dict[name]=attr.value
        elif isinstance(attr,(set,)):
            export_dict[name]=list(attr)
        else:
            export_dict[name]=attr
    return export_dict

def json_dict_to_obj(json_dict,obj):
    """
    json数据dict导入对象.
 
    :param json_dict: dict,json数据dict
    :param obj: class,导入对象
    :returns: no return
    :raises: no exception
    """
    for name,value in json_dict.items():
        print(name,value)
        attr=getattr_multilevel(obj, name)
        attr_json=value
        if isinstance(attr,(QDate,)):
            setattr_multilevel(obj,name,QDate.fromString(attr_json,"yyyy/MM/dd"))
                                  
        elif isinstance(attr,(QTime,)):
            setattr_multilevel(obj,name,QTime.fromString(attr_json,"hh:mm"))
                    
        elif isinstance(attr,(datetime,)):
            setattr_multilevel(obj,name,datetime.strptime(attr_json, '%Y-%m-%d %H:%M:%S'))
                   
        #elif isinstance(attr,(PlanType,)):
        #    setattr_multilevel(obj,name,PlanType(attr_json))
                   
        #elif isinstance(attr,(CycleType,)):
        #    setattr_multilevel(obj,name,CycleType(attr_json))
                  
        elif isinstance(attr,(set,)):
            setattr_multilevel(obj,name,set(attr_json))
                   
        else:
            setattr_multilevel(obj,name,attr_json)


def json_to_obj(json_dict,obj):
    """
    json数据dict导入同类型对象集.
 
    :param json_dict: dict,json数据dict
    :param objs: list/dict,对象集，可为list或dict，对象同类型
    :returns: no return
    :raises: no exception
    """
    for key,value in json_dict.items():
        if isinstance(value, dict):
            json_dict_to_obj(value,obj)
        elif isinstance(value, list):
            _obj=None
            for _value in value:
                json_dict_to_obj(_value,_obj)
                obj.append(_obj)


'''
        


'''
def obj_to_dict(item,dct):
    """
    对象及其子对象属性转换为字典.
 
    :param item: obj/list/dict,待转换对象
    :param dct: dict/list,属性转换后保存的dict或list.
                          若item为字典，相应dct也应为空字典；
                          若item为列表，相应dct也应为空列表；
    :returns: no return
    :raises: no exception
    """
    if isinstance(item,dict):
        for key,value in item.items():            
            if isinstance(value,dict):
                dct[key]={}
                obj_to_dict(value,dct[key])
            elif isinstance(value,(list,tuple,set)):
                dct[key]=[]
                obj_to_dict(value,dct[key])
            elif hasattr(value,"__dict__"):
                dct[key]={}
                obj_to_dict(value.__dict__,dct[key])
            else:
                dct[key]=value
    elif isinstance(item,(list,tuple,set)):
        for value in item:
            if isinstance(value,dict):
                _dict={}
                dct.append(_dict)
                obj_to_dict(value,_dict)
            elif isinstance(value,(list,tuple,set)):
                _list=[]
                dct.append(_list)
                obj_to_dict(value,_list)
            elif hasattr(value,"__dict__"):
                _dict={}
                dct.append(_dict)
                obj_to_dict(value.__dict__,_dict)
            else:
                dct.append(value)
    elif hasattr(item,"__dict__"):        
        obj_to_dict(item.__dict__,dct)
    else:
        pass
'''

#def obj_to_dict(item,dct,_key=None):
#    """
#    对象及其子对象属性转换为字典.
 
#    :param item: obj/list/dict,待转换对象
#    :param dct: dict/list,属性转换后保存的dict或list.
#                          若item为字典，相应dct也应为空字典；
#                          若item为列表，相应dct也应为空列表；
#    :returns: no return
#    :raises: no exception
#    """
#    _type_const=(int,float,str,bool)
#    _type_bool=(None,True,False)

#    if isinstance(item,dict):
#        for key,value in item.items():
#            if isinstance(value,dict):
#                dct[key]={}
#                obj_to_dict(value,dct[key],key)
#            elif isinstance(value,(list,tuple,set)):
#                dct[key]=[]
#                obj_to_dict(value,dct[key])
#            #elif hasattr(value,"__dict__"):
#            elif value in _type_bool:
#                dct[key]=value
#            elif value.__class__ not in _type_const:
#                print(key,value)
#                _item=type_py_to_json(value)
#                if _item is None:
#                    if hasattr(value,"__dict__"):
#                        obj_to_dict(value.__dict__,dct[key],key)
#                else:
#                    dct[key]=_item

#                #dct[key]={}
#                #print(key)
#                #obj_to_dict(value.__dict__,dct[key],key)
#            else:
#                dct[key]=value
#    elif isinstance(item,(list,tuple,set)):
#        for value in item:
#            if isinstance(value,dict):
#                _dict={}
#                dct.append(_dict)
#                obj_to_dict(value,_dict)
#            elif isinstance(value,(list,tuple,set)):
#                _list=[]
#                dct.append(_list)
#                obj_to_dict(value,_list)
#            #elif hasattr(value,"__dict__"):
#            elif value in _type_bool:
#                dct.append(value)
#            elif value.__class__ not in _type_const:
#                _item=type_py_to_json(value)
#                if _item is None:
#                    _dict={}
#                    dct.append(_dict)
#                    if hasattr(value,"__dict__"):
#                        obj_to_dict(value.__dict__,_dict)
#                else:
                    
#                    dct.append(_item)

#                #dct.append(_dict)
#                #obj_to_dict(value.__dict__,_dict)
#            else:
#                dct.append(value)

#    #elif hasattr(item,"__dict__"):
#    elif item.__class__ not in _type_const:
#        _item=type_py_to_json(item)
#        if _item is None:
#            if hasattr(item,"__dict__"):
#                obj_to_dict(item.__dict__,dct)
#        else:
#            dct[_key]=_item
#    else:
#        pass
def type_json_to_py(json_data,py):
    """
    json类型转换为python类型.
 
    :param json_data: json待转换数据
    :param py: 转换为python类型
    :returns: 转换后python数据
    :raises: no exception
    """
    if isinstance(py,(Enum,)):
        return py.__class__(json_data)
    elif isinstance(py,(datetime,)):
        return datetime.strptime(json_data, '%Y-%m-%d %H:%M:%S')
    elif isinstance(py,(timedelta,)):
        pass
        return True
    elif isinstance(py,(QDate,)):
        return QDate.fromString(json_data,"yyyy/MM/dd")
    elif isinstance(py,(QTime,)):
        return QTime.fromString(json_data,"hh:mm")
    elif isinstance(py,(set,)):
        if isinstance(json_data,(list,)):
            return set(json_data)
    else:
        #print(f"未定义的json转python类型{type(py)}")
        return None



def type_py_to_json(py):
    """
    python中json不能转换的类型变为可被json转换的类型.
 
    :param py: 待转换对象
    :returns: json可转换类型
    :raises: no exception
    """
  
    if isinstance(py,(Enum,)):
        return py.value
    elif isinstance(py,(datetime,)):
        return py.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(py,(timedelta,)):
        return str(py)
    elif isinstance(py,(QDate,)):
        return py.toString("yyyy/MM/dd")
    elif isinstance(py,(QTime,)):
        return py.toString("hh:mm")
    else:
        #print(f"未定义的python转json类型{type(py)}")
        return None

def add_item(item,after_trans,key):
    if isinstance(after_trans,(list,)):
        after_trans.append(item)
        return True
    elif isinstance(after_trans,(dict,)):
        after_trans[key] = item
        return True
    else:
        print(f"after_trans类型为{type(after_trans)},类型错误，应为list或dict")
        return False

def obj_to_dict(item,after_trans,key="unnamed_obj",*,filter="filter_attr_names",trans_all=False):
    """
    对象及其子对象属性转换为字典.
 
    :param item: obj/list/dict,待转换对象
    :param after_trans: dict/list,属性转换后保存的dict或list.
                          若item为字典，相应after_trans也应为空字典；
                          若item为列表，相应after_trans也应为空列表；
    :param filter: str,对象转换属性过滤器。
                    如需只转换部分属性，需在类（非实例）中定义一个包含这些属性名的list,例：
                    class Example(object):
                        filter_attr_names=["attr_1","attr_2"]
                        def __init__(self):
                            self.attr_1=0
                            self.attr_2=0.0
                            self.attr_3=""
    :returns: no return
    :raises: no exception
    """
    if isinstance(item,(int,float,str,bool)):
        add_item(item,after_trans,key)
    elif item is None:
        add_item(item,after_trans,key)
    elif isinstance(item,(dict,)):
        _after_trans = {}
        if isinstance(after_trans,(dict,)):
            after_trans[key] = _after_trans
        elif isinstance(after_trans,(list,)):
            after_trans.append(_after_trans)
        for _key,_value in item.items():
            if trans_all is True:
                obj_to_dict(_value,_after_trans,_key,trans_all=True)
            else:
                obj_to_dict(_value,_after_trans,_key)
    elif isinstance(item,(list,tuple,set)):
        _after_trans = []
        if isinstance(after_trans,(dict,)):
            after_trans[key] = _after_trans
        elif isinstance(after_trans,(list,)):
            after_trans.append(_after_trans)
        for _value in item:
            obj_to_dict(_value,_after_trans,key)
    elif type_py_to_json(item) != None:
        obj_to_dict(type_py_to_json(item),after_trans,key)
    elif hasattr(item,"__dict__"): 
        if trans_all is True:
            obj_to_dict(item.__dict__,after_trans,key,trans_all=True)
        else:
            _item = {}
            if hasattr(item.__class__,filter):
                _filter = getattr(item.__class__,filter)
                if isinstance(_filter,list):
                    for name in _filter:
                        _item[name] = item.__dict__.get(name)
                    obj_to_dict(_item,after_trans,key)
                else:
                    print(f"{type(_filter)}非list类型的选取属性集")
            else:
                obj_to_dict(item.__dict__,after_trans,key)
        
    else:
        print(f"不支持的转换类型{type(item)}")


def obj_to_json_file(file,obj,dict_json,obj_name,filter="filter_attr_names"):
    """
    对象转换为json保存.
 
    :param file: str,文件路径
    :param obj: obj,待转换对象
    :param dict_json: dict/list,保存对象转换为json可解析dict/list
    :param obj_name: str,转换对象名称，用作json根
    :param filter: str,对象转换属性过滤器。
    :returns: no return
    :raises: no exception
    """
    obj_to_dict(obj,dict_json,obj_name,filter=filter,trans_all=False)
    with open(file, 'w') as f:
        json.dump(dict_json,f,ensure_ascii=False,indent=4)
    #print(json.dumps(dict_json,ensure_ascii=False, indent=4))

def json_to_obj(json_dict,obj,attr_name="",filter="filter_attr_names"):
    """
    json数据导入对象.
 
    :param json_dict: dict,json数据字典
    :param obj: obj,待导入对象
    :returns: no return
    :raises: no exception
    """
    if isinstance(json_dict,(dict,)):
        for key,value in json_dict.items():
            if isinstance(obj,dict):
                json_to_obj(value,getattr(obj,key))
                #if obj.get(key) is None:
                #    obj[key]={}
                #    json_to_obj(value,obj[key])
            else:
                json_to_obj(value,obj,key)
                #setattr(obj,key,value)

    elif type_json_to_py(json_dict,getattr(obj,attr_name)) != None:
        setattr(obj,attr_name,type_json_to_py(json_dict,getattr(obj,attr_name)))
    elif isinstance(getattr(obj,attr_name),(int,float,str,bool,list)):
        #obj=json_dict
        setattr(obj,attr_name,json_dict)
    elif json_dict is None:
        #obj=None
        setattr(obj,attr_name,None)
    #elif isinstance(json_dict,(dict,)):
    #    for key,value in json_dict.items():
    #        if isinstance(obj,dict):
    #            if obj.get(key) is None:
    #                obj[key]={}
    #                json_to_obj(value,obj[key])
    #        else:
    #            json_to_obj(value,getattr(obj,key))
        
    else:
        pass