#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
File   Name ： func_svg.py
Description :  svg功能
Author      :  simon
Create Time ： 2022.03.29
-------------------------------------------------------------------------------
Change Activity:
               时间:更改内容
-------------------------------------------------------------------------------
"""
__author__ = 'simon'

from PyQt5.QtXml import QDomDocument
from PyQt5 import QtSvg
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, Close
from svg.path import parse_path
from svgutils.compose import *
import svgutils.transform as sg
import xml.etree.ElementTree as ET
from func_map import *

#classes#######################################################################
'''
class SvgPath(object):
    """SVG路径类."""
    
    def __init__(self,element):
        """
        初始化类.
     
        :param element: 路径svg元素
        :returns: no return
        :raises: no exception
        """
        self.element = element
        self.id = self.element.attribute("id")
        self.parse = parse_path(self.element.attribute("d"))
        self.length = self.parse.length()


class SvgMap(object):
    """SVG地图类."""
    
    def __init__(self,svg_file):
        """
        初始化类.
     
        :param svg_file: svg文件名
        :returns: no return
        :raises: no exception
        """
        self.doc = QDomDocument('map')
        self.paths = []
        self.all = []
        self.load(svg_file)
        #self.load_str(svg_file)
        self.init_path()
        self.init_robot()
    
    def load(self,svg_file):
        """
        加载svg文件.
     
        :param svg_file: svg文件名
        :returns: no return
        :raises: no exception
        """
        with open(svg_file, 'r',encoding='UTF-8') as f:
            file = f.read()
            self.doc.setContent(file)

    def load_str(self,svg_str):
        """
        加载svg文件.
     
        :param svg_file: svg文件名
        :returns: no return
        :raises: no exception
        """
        self.doc.setContent(svg_str)
    
    def init_path(self):
        """初始化路径."""
       
        for i in range(self.doc.elementsByTagName("path").length()):
            self.paths.append(SvgPath(self.doc.elementsByTagName("path").item(i).toElement()))
    
    def init_robot(self):
        """初始化机器人."""
        
        for i in range(self.doc.elementsByTagName("circle").length()):
            self.all.append(self.doc.elementsByTagName("circle").item(i).toElement())
    
    def update_robot_pos(self,path_length,reverse=False):
        """
        更新机器人位置.
     
        :param path_length: 机器人在路径上行走的长度
        :param reverse: 机器人在路径上反向
        :returns: no return
        :raises: no exception
        """
        if reverse:
            _pos = 1 - path_length / self.paths[0].length
        else:
            _pos = path_length / self.paths[0].length
         
        if _pos > 1.0:
            _pos = 1.0
        elif _pos < 0.0:
            _pos = 0.0

        pos = self.paths[0].parse.point(_pos)
        #print(pos.real,pos.imag )
        self.all[0].setAttribute("cx",str(pos.real))
        self.all[0].setAttribute("cy",str(pos.imag))
'''   
class SvgIcon(object):
    def __init__(self):
        """
        SVG图标.
     
        :returns: no return
        :raises: no exception
        """
        self.element=None
        self.width=50
        self.height=50

class SvgPathPoint(object):
    
    def __init__(self,path_point):
        """
        SVG路径上的点.
     
        :param element: 路径svg元素
        :returns: no return
        :raises: no exception
        """
        self.point=path_point
        self.x=0.0
        self.y=0.0
        self.element=None
        self.icon=None
        
     

class SvgPath(object):
     
    def __init__(self,figure_element):
        """
        SVG路径.
     
        :param element: 路径svg元素
        :returns: no return
        :raises: no exception
        """
        self.element=figure_element
        self.track_path=self.element.find_id("path_1")
        #print(self.track_path.tostr())
        self.id = None
        self.parse = None
        self.length = 0.0
        self.is_zero_reverse= False
        self.init()
        self.layer_charge=None
        self.layer_water=None
        self.layer_clean=None
        self.layer_robot=None
    
    def init(self):
        """
        初始化.
    
        :returns: no return
        :raises: no exception
        """
        self.id = self.element.root.get("id")
        self.parse = parse_path(self.track_path.root.get("d"))
        self.length = self.parse.length()
        print(self.id,self.track_path.root.get("d"),self.length)

    def get_layer(self):
        """
        获取图层.
    
        :returns: no return
        :raises: no exception
        """
        
        self.layer_charge=self.element.root.find("*")
        print(self.layer_charge)
        
    
    def pos_to_xy(self,pos_length):
        """
        路径长度转换为xy坐标.
     
        :param pos_length: float,路径长度
        :returns: no return
        :raises: no exception
        """
        if self.is_zero_reverse:
            _pos = 1 - pos_length / self.length
        else:
            _pos = pos_length / self.length
         
        if _pos > 1.0:
            _pos = 1.0
        elif _pos < 0.0:
            _pos = 0.0

        pos_xy = self.parse.point(_pos)
        _x=pos_xy.real
        _y=pos_xy.imag
        print(_x,_y)
        return _x,_y
    
    #def add_path_point(self,copy_point,pos,offset_x,offset_y):
    #    """
    #    添加路径点.
     
    #    :param copy_point: element,xml元素
    #    :param pos: float,路径长度
    #    :param offset_x: float,x偏移
    #    :param offset_y: float,y偏移
    #    :returns: no return
    #    :raises: no exception
    #    """
    #    pass
    def add_path_point(self,svg_path_point):
        """
        添加路径点.
     
        :param copy_point: element,xml元素
        :param pos: float,路径长度
        :param offset_x: float,x偏移
        :param offset_y: float,y偏移
        :returns: no return
        :raises: no exception
        """
        svg_path_point.x,svg_path_point.y=self.pos_to_xy(svg_path_point.point.path_pos)


class SvgMap(object):
    
    def __init__(self):
        """
        svg地图.
    
        :returns: no return
        :raises: no exception
        """
        self.map=None
        self.root=None
        self.charge_point_0=None
        self.path_1=None
        self.icon_robot=SvgIcon()
        self.icon_charge=SvgIcon()
        self.icon_water=SvgIcon()
        self.icon_clean=SvgIcon()
        self.icon_obstacle=SvgIcon()
        self.copy_charge=None
        self.copy_water=None
        self.copy_clean=None
        self.layer_charge=None
        self.layer_water=None
        self.layer_clean=None
        self.layer_robot=None

    
    def load(self,svg_file):
        """
        加载svg文件.
     
        :param file: 文件路径，svg文件
        :returns: no return
        :raises: no exception
        """
        self.map = sg.fromfile(svg_file)
        self.root =self.map.getroot()
        #print(self.root[0].tostr())

    
    def get_tunnel_path(self):
        """
        获取隧路径.
    
        :returns: no return
        :raises: no exception
        """
        self.tunnel_path=self.root.find_id("tunnel_path.0")
        #print(self.tunnel_path.tostr())
        self.path_1=SvgPath(self.tunnel_path)
        self.path_1.get_layer()
    
    def get_icon(self):
        """
        获取图标.
    
        :returns: no return
        :raises: no exception
        """
        self.layer_charge=None
        self.layer_water=None
        self.layer_clean=None
        self.layer_robot=None
          
        
    def get_copy(self):
        """
        获取复制项.
    
        :returns: no return
        :raises: no exception
        """
        
        self.copy_charge=self.root.find_id("charge_point.0.0")
        self.copy_water=self.root.find_id("water_point.0.0")
        self.copy_clean=self.root.find_id("clean_point.0.0.0")

    def get_layer(self):
        """
        获取复制项.
    
        :returns: no return
        :raises: no exception
        """
        
        self.copy_charge=self.root.find_id("charge_point.0.0")
        self.copy_water=self.root.find_id("water_point.0.0")
        self.copy_clean=self.root.find_id("clean_point.0.0.0")
    
    def set_charge_point(self):
        """
        设定充电点.
    
        :returns: no return
        :raises: no exception
        """
        self.charge_point_0=SvgPathPoint(charge_point_1)        
        self.charge_point_0.icon=self.icon_charge
        self.path_1.add_path_point(self.charge_point_0)
        self.charge_point_0.element=copy.deepcopy(self.copy_charge)
        self.charge_point_0.element.root.set("id","charge_point.0.1")
        self.charge_point_0.element.moveto(self.charge_point_0.x,self.charge_point_0.y)
        print(self.charge_point_0.element.tostr())


        

    def add_point_charge(self,pos):
        """
        添加充电点.
     
        :param pos: float,点在路径上的长度位置
        :returns: no return
        :raises: no exception
        """
        self.charge_point_0=self.map.find_id("charge_point.0.0")



#functions#####################################################################
svg_map = SvgMap()
svg_map.load('./map/map - 副本.svg')
svg_map.get_tunnel_path()
svg_map.get_icon()
svg_map.get_copy()
svg_map.set_charge_point()
svg_map.path_1.add_path_point()




#svg_map = SvgMap('./map/map.svg')
#svg_map = SvgMap('./map/map - 副本.svg')

'''
#create new SVG figure
fig = sg.SVGFigure("600", "400")

# load matpotlib-generated figures
fig1 = sg.fromfile('./map/map.svg')
fig2 = sg.fromfile('./map/无线充电.svg')

# get the plot objects
plot1 = fig1.getroot()
plot2 = fig2.getroot()
#plot2.moveto(50, 0, scale=0.2)
plot2.moveto(50, 0)

# add text labels
txt1 = sg.TextElement(25,20, "A", size=12, weight="bold")
txt2 = sg.TextElement(305,20, "B", size=12, weight="bold")

# append plots and labels to figure
fig.append([plot1, plot2])
fig.append([txt1, txt2])
svg_str=fig.to_str()
fig.save("fig_final.svg")

from svgutils.compose import *
Figure("700", "400",
       SVG("./map/map.svg"),
       SVG("./map/圆角矩形.svg").scale(0.02)
                          .move(50,100)
       ).save("fig_final_compose.svg")

svg_map = SvgMap(svg_str)
'''