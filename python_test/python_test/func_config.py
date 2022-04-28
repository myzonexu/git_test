#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
File   Name ： func_config.py
Description :  配置文件功能
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
from enum import Enum,unique
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
        rows=[]
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
        if len(rows)==0:
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
        elif isinstance(attr,(Enum,)):
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


#def import_json(self,json_dict):
#    #print(json_dict)
#    plan_list=json_dict.get("task_plans")
#    #print(plan_list)
#    for dct in plan_list:
#        plan=TaskPlan()
#        for name in plan.export_name:                
#            attr=getattr(plan, name)
#            attr_json=dct.get(name)
#            if isinstance(attr,(QDate,)):
#                setattr(plan,name,QDate.fromString(attr_json,"yyyy/MM/dd"))
                                  
#            elif isinstance(attr,(QTime,)):
#                setattr(plan,name,QTime.fromString(attr_json,"hh:mm"))
                    
#            elif isinstance(attr,(datetime,)):
#                setattr(plan,name,datetime.strptime(attr_json, '%Y-%m-%d %H:%M:%S'))
                   
#            elif isinstance(attr,(PlanType,)):
#                setattr(plan,name,PlanType(attr_json))
                   
#            elif isinstance(attr,(CycleType,)):
#                setattr(plan,name,CycleType(attr_json))
                  
#            elif isinstance(attr,(set,)):
#                setattr(plan,name,set(attr_json))
                   
#            else:
#                setattr(plan,name,attr_json)
                
#        self.all[plan.id]=plan