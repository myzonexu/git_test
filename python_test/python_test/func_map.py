#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
File   Name ： func_map.py
Description :  地图
Author      :  simon
Create Time ： 2022.5.23
-------------------------------------------------------------------------------
Change Activity:
               时间:更改内容
-------------------------------------------------------------------------------
"""
__author__ = 'simon'


#classes#######################################################################
from func_defines import *
from func_track import *
import numpy as np

class PathPoint(object):
   
    def __init__(self,pos_path):
        """     
        路径上的点.
     
        :param pos_path: float,在路径上的位置
        :returns: no return
        :raises: no exception
        """
        self.path_pos=pos_path
        self._type=PathPointType.NONE
        #self.x=0.0
        #self.y=0.0

    @property
    def type(self):
        """
        路径点类型.
    
        :returns: enum,点类型
        :raises: no exception
        """
        return self._type

    @type.setter
    def type(self,point_type):
        """
        设置点类型.
     
        :param type: enum,点类型
        :returns: no return
        :raises: no exception
        """
        if isinstance(point_type,PathPointType):
            self._type=point_type
        else:
            print("值类型不匹配，应为PathPointType枚举")
    
    #def get_pos_xy(self,svg_path):
    #    """
    #    路径长度位置转换为xy坐标.
     
    #    :param svg_path: svg_path,svg路径对象
    #    :returns: float,float x坐标，y坐标
    #    :raises: no exception
    #    """
    #    x,y=0.0
    #    pass
    #    return x,y


class RfidPoint(PathPoint):

    def __init__(self,pos_path):
        """     
        路径上的RFID点.
     
        :param pos_path: float,在路径上的位置
        :param unique_id: int,rfid唯一id
        :param rfid_command: int,rfid指令
        :returns: no return
        :raises: no exception
        """
        super().__init__(pos_path)
        self.type=PathPointType.RFID
        self.id=0
        self.command=0
        self.value=None
    
    def set_content(self,unique_id,rfid_command,command_value=None):
        """
        设置标签内容.
     
        :param unique_id: int,rfid唯一id
        :param rfid_command: int,rfid指令
        :param value: 指令值
        :returns: no return
        :raises: no exception
        """
        self.id=unique_id
        self.command=rfid_command
        self.value=command_value

class CleanPoint(PathPoint):
    def __init__(self,pos_path):
        """     
        路径上的清扫点.
     
        :param pos_path: float,在路径上的位置
        :param mark: enum,标记
        :returns: no return
        :raises: no exception
        """
        super().__init__(pos_path)
        self.type=PathPointType.CLEAN
        self.num_wall=0   
        self.num_gnd=0
        self.set_clean_mark_num()
    
    def set_clean_mark_num(self,wall_num=4,gnd_num=1):
        """
        设置清扫点墙面和地面清扫标志数量.
     
        :param wall_num: int,墙面清扫标志数量
        :param gnd_num: int,地面清扫标志数量
        :returns: no return
        :raises: no exception
        """
        self.num_wall=wall_num   
        self.num_gnd=gnd_num
        
class PathPointSeries(object):

    def __init__(self,start_pos,num,space_pos,class_type):
        """
        路径上的连续等间距点.
     
        :param start_pos: float,起始点在路径上的位置
        :param num: int,点的数量
        :param space_pos: float,点间距，可为负数
        :param class_type: class type,路径点类
        :returns: no return
        :raises: no exception
        """
        self.pos_start=start_pos
        self.count=num
        self.pos_space=space_pos
        self.type=class_type

        self.points=[]
        for i in range(0,num):
            _point=class_type(start_pos+i*space_pos)
            self.points.append(_point)

class PathPointGroup(object):

    def __init__(self):
        """路径上的点集合."""
        self.value_type_dict={"all":{"type":PathPoint}}
        self.all=[]
        self._pos_list=[]        
    
    def add_point(self,point):
        """
        添加单一点.
     
        :param point: PathPoint，添加的点
        :returns: no return
        :raises: no exception
        """
        self.all.append(point)

    def add_points(self,points):
        """
        添加连续点.
     
        :param clean_point: CleanPoint，添加的清扫点
        :returns: no return
        :raises: no exception
        """
        self.all+=points.points
    
    def add(self,point):
        """
        添加点或连续点.
     
        :param point: 点或连续点
        :returns: no return
        :raises: no exception
        """
        if isinstance(point,PathPoint):
            self.add_point(point)
        elif isinstance(point,PathPointSeries):
            self.add_points(point)
        else:
            print("路径点类型错误")

    @property
    def pos_list(self):
        """
        所有点位置列表.
    
        :returns: list,所有点位置列表
        :raises: no exception
        """
        self._pos_list=[]
        for p in self.all:
            self._pos_list.append(p.path_pos)
        return self._pos_list
    
class CleanPointGroup(PathPointGroup):
    
    def __init__(self):
        """清扫点集合."""
        super().__init__()
        self._set_current=False

        self.array_pos=None
        self.array_cleaned=None

        self._count_cleaned=0
    
    def init_array_pos(self):
        """
        初始化位置一维数组.
    
        :returns: np.array,位置一维数组
        :raises: no exception
        """
        self.array_pos=np.array(self.pos_list)
        return self.array_pos

    def init_array_cleaned(self):
        """
        初始化清扫点状态二维数组.
    
        :returns: np.array,清扫点状态二维数组，
                            行：每个清扫点n个清扫标状态；
                            列：清扫点
        :raises: no exception
        """
        _num_point=len(self.all)
        if _num_point:
            _num_mark=self.all[0].num_wall+self.all[0].num_gnd
            self.array_cleaned=np.zeros((_num_point,_num_mark), dtype = bool)
        return self.array_cleaned
    
    def set_track_cleaned(self,track):
        """
        设置轨迹已清理.
     
        :param track: Track，轨迹
        :returns: no return
        :raises: no exception
        """
        if self.array_pos is None:
            self.init_array_pos()
        if self.array_cleaned is None:
            self.init_array_cleaned()

        _arm_pos=track.action_arm.value-1

        _index_pos=np.where((self.array_pos>=min(track.pos_start,track.pos_end))&(self.array_pos<=max(track.pos_start,track.pos_end)))

        self.array_cleaned[_index_pos,_arm_pos]=True
        
    def set_cleaned(self,tracks,reset_all=False):
        """
        设置轨迹已清理.
     
        :param tracks: Tracks，轨迹集合
        :param reset_all: bool，False:已结束轨迹设置清理点只执行一次，此后只设置当前轨迹清理点
                                True:设置已结束轨迹和当前轨迹清理点
        :returns: no return
        :raises: no exception
        """
        if reset_all is True:
            self._set_current=False

        if isinstance(tracks,Tracks):
            if self._set_current is False:
                for _track in tracks.all:
                    self.set_track_cleaned(_track)
                self._set_current=True
            else:
                pass

            self.set_track_cleaned(tracks.current)
        else:
            print("轨迹集合类型错误")
    
    @property
    def count_cleaned(self):
        """
        清扫标志计数.
    
        :returns: int,已清扫标志数量
        :raises: no exception
        """
        self._count_cleaned=np.count_nonzero(self.array_cleaned)
        #self._count_cleaned=np.nonzero(self.array_cleaned)[0].shape[0]
        return self._count_cleaned


class Path(object):
    
    def __init__(self):
        """
        地图路径类.
     
        :returns: no return
        :raises: no exception
        """
        self.id=""
        self._path=None
        self.clean_points=CleanPointGroup()
        self.charge_points=PathPointGroup()
        self.water_points=PathPointGroup()
        self.rfid_points=PathPointGroup()
        self.rfid_points.value_type_dict={"all":{"type":RfidPoint}}

    @property
    def path(self):
        """
        获取路径.
        
        :returns: str,svg路径
        :raises: no exception
        """
        return self._path

    @path.setter
    def path(self,str_svg_path):
        """
        设置路径.
         
        :param str_svg_path: str,svg路径
        :returns: no return
        :raises: no exception
        """
        if isinstance(str_svg_path,str):
            self._path=str_svg_path
        else:
            print("path类型错误")

class Map(object):
    
    def __init__(self):
        """
        地图类.
    
        :returns: no return
        :raises: no exception
        """
        self.value_type_dict={"paths":{"type":Path,"key":"id"}}
        self.id=""
        self.viewbox=None

        self.paths={}

#变量定义#####################################################################

map_1=Map()
map_1.id="map_1"

path_1=Path()
path_1.id="path_1"
path_1.path="m0 10  300 0 240 190"

map_1.paths[path_1.id]=path_1

clean_points_1=PathPointSeries(100,6,50,CleanPoint)
path_1.clean_points.add(clean_points_1)
path_1.clean_points.init_array_pos()
path_1.clean_points.init_array_cleaned()

charge_point_1=PathPoint(5)
charge_point_1.type=PathPointType.CHARGE
path_1.charge_points.add(charge_point_1)

water_point_1=PathPoint(550)
water_point_1.type=PathPointType.WATER
path_1.water_points.add(water_point_1)


rfid_points_1=PathPointSeries(10,5,100,RfidPoint)
path_1.rfid_points.add(rfid_points_1)