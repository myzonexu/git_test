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
from lxml import etree

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
        self.width=30
        self.height=30
        self.offset_x=-self.width/2
        self.offset_y=-self.height/2


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
        self.is_zero_reverse= True
        self.init()
        self.layer_charge=None
        self.layer_water=None
        self.layer_clean=None
        self.layer_robot=None
        self.offset_x=0.0
        self.offset_y=0.0
    
    def init(self):
        """
        初始化.
    
        :returns: no return
        :raises: no exception
        """
        self.id = self.element.root.get("id")
        self.parse = parse_path(self.track_path.root.get("d"))
        self.length = self.parse.length()
        #print(self.id,self.track_path.root.get("d"),self.length)

    def get_layer(self):
        """
        获取图层.
    
        :returns: no return
        :raises: no exception
        """
        
        self.layer_charge=self.element.root.find(".//*[@class='charge_point']")
        self.layer_water=self.element.root.find(".//*[@class='water_point']")
        self.layer_clean=self.element.root.find(".//*[@class='clean_point']")
        self.layer_robot=self.element.root.find(".//*[@class='robot']")
        
    
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
        #print(_x,_y)
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
    def add_path_point(self,svg_path_point,id,layer,offset_x=0,offset_y=0):
        """
        添加路径点.
     
        :param svg_path_point: SvgPathPoint,路径点
        :param id: str,点在svg中元素id
        :param layer: element,点添加在路径的哪个层
        :param offset_x: float,x偏移
        :param offset_y: float,y偏移
        :returns: no return
        :raises: no exception
        """
        
        layer.append(svg_path_point.element.root)
        svg_path_point.element.root.set("id",id)
        svg_path_point.x,svg_path_point.y=self.pos_to_xy(svg_path_point.point.path_pos)        
        
        svg_path_point.element.moveto(svg_path_point.x+svg_path_point.icon.offset_x+offset_x,svg_path_point.y+svg_path_point.icon.offset_y+offset_y)


class SvgMap(object):
    
    def __init__(self):
        """
        svg地图.
    
        :returns: no return
        :raises: no exception
        """
        self.map=None
        self.root=None
        self.string=""
        self.doc = QDomDocument('map')
        self.load_map=None
        self.load_root=None
        self.charge_point_0=None
        self.water_point_0=None
        self.robot_point_0=None
        self.clean_points=[]
        self.path_1=None
        self.icon_robot=SvgIcon()
        self.icon_charge=SvgIcon()
        self.icon_water=SvgIcon()
        self.icon_clean=SvgIcon()
        self.icon_obstacle=SvgIcon()
        self.copy_charge=None
        self.copy_water=None
        self.copy_clean=None
        self.copy_robot=None
        self.layer_charge=None
        self.layer_water=None
        self.layer_clean=None
        self.layer_robot=None
        self.element_robot=None
        self.element_robot_point=None
        self.element_robot_avoid_f=None
        self.element_robot_avoid_r=None
        self.element_clean_points=[]

    
    def load(self,svg_file):
        """
        加载svg文件.
     
        :param file: 文件路径，svg文件
        :returns: no return
        :raises: no exception
        """
        self.map=sg.SVGFigure()
        #self.load_root=self.map.getroot()
        self.map.root.set("viewBox","0 0 700 400")
        #self.map.root.set("width","600")
        #self.map.root.set("height","300")
        
        self.load_map = sg.fromfile(svg_file)
        self.root =self.load_map.getroot()
        self.map.append(self.root)        
        #self.map.save("test1.svg")
    
    def get_tunnel_path(self):
        """
        获取隧路径.
    
        :returns: no return
        :raises: no exception
        """
        self.tunnel_path=self.root.find_id("tunnel_path.0")        
        #print(self.tunnel_path.tostr())
        self.path_1=SvgPath(self.tunnel_path)
        self.path_1.offset_x=20
        self.path_1.offset_y=150
        self.tunnel_path.moveto(self.path_1.offset_x,self.path_1.offset_y)
        self.path_1.get_layer()
        
    
    def get_icon(self):
        """
        获取图标.
    
        :returns: no return
        :raises: no exception
        """
        pass
          
        
    def get_copy(self):
        """
        获取复制项.
    
        :returns: no return
        :raises: no exception
        """
        
        self.copy_charge=self.root.find_id("copy_charge_point")
        self.copy_water=self.root.find_id("copy_water_point")
        self.copy_clean=self.root.find_id("copy_clean_point")
        self.copy_robot=self.root.find_id("copy_robot_point")

    
    def set_charge_point(self):
        """
        设定充电点.
    
        :returns: no return
        :raises: no exception
        """
        #self.charge_point_0=SvgPathPoint(charge_point_1)        
        #self.charge_point_0.icon=self.icon_charge
        #self.path_1.add_path_point(self.charge_point_0)
        #self.charge_point_0.element=copy.deepcopy(self.copy_charge)
        #self.charge_point_0.element.root.set("id","charge_point.0.1")

        #self.charge_point_0.element.moveto(self.charge_point_0.x,self.charge_point_0.y)
        self.charge_point_0=SvgPathPoint(charge_point_1)
        self.charge_point_0.element=copy.deepcopy(self.copy_charge)
        self.copy_charge.root.set("display","none")
        self.charge_point_0.icon=self.icon_charge
        self.path_1.add_path_point(self.charge_point_0,"charge_point.0.0",self.path_1.layer_charge,offset_y=-50)
        #print(self.charge_point_0.element.tostr())
        self.charge_point_0.element=self.map.root.find(f".//*[@id='charge_point.0.0']")
        self.charge_point_0.element.set("fill","#1296db")

    def set_water_point(self):
        """
        设定充电点.
    
        :returns: no return
        :raises: no exception
        """
        self.water_point_0=SvgPathPoint(water_point_1)
        self.water_point_0.element=copy.deepcopy(self.copy_water)
        self.copy_water.root.set("display","none")
        self.water_point_0.icon=self.icon_water
        self.path_1.add_path_point(self.water_point_0,"water_point.0.0",self.path_1.layer_water,offset_y=-50)
        #print(self.water_point_0.element.tostr())
        self.water_point_0.element=self.map.root.find(f".//*[@id='water_point.0.0']")
        self.water_point_0.element.set("fill","#1296db")

    def set_clean_point(self):
        """
        设定清扫点.
    
        :returns: no return
        :raises: no exception
        """
        #_point=SvgPathPoint(path_1.clean_points.all[0])
        #_point.element=copy.deepcopy(self.copy_clean)
        #_point.icon=self.icon_water

        self.icon_clean.offset_x=-5
        self.icon_clean.offset_y=-5

        _num=0
        for p in path_1.clean_points.all:
            for i in range(5):
                _point=SvgPathPoint(p)
                _point.element=copy.deepcopy(self.copy_clean)
                _point.icon=self.icon_clean
                if i<4:
                    self.path_1.add_path_point(_point,f"clean_point.0.{_num}.{i}",self.path_1.layer_clean,offset_x=0,offset_y=-30*(3-i)-35)
                else:
                    self.path_1.add_path_point(_point,f"clean_point.0.{_num}.{i}",self.path_1.layer_clean,offset_x=0,offset_y=45)
            _num=_num+1
        self.copy_clean.root.set("display","none")

    def set_clean_element(self):
        """
        设定清扫点元素.
    
        :returns: no return
        :raises: no exception
        """    
        pass
        
        _pos=path_1.clean_points.array_cleaned.shape[0]
        _num=path_1.clean_points.array_cleaned.shape[1]
        #print(_pos,_num)
        _element=None
        for i in range(_pos):
            for j in range(_num):
                #self.map.root.find_id(f"clean_point.0.{i}.{j}")
                _element=self.map.root.find(f".//*[@id='clean_point.0.{i}.{j}']")
                
                self.element_clean_points.append(_element) 
                pass

    def set_robot_point(self):
        """
        设定机器人点.
    
        :returns: no return
        :raises: no exception
        """

        self.robot_point_0=SvgPathPoint(robot_point_1)
        self.robot_point_0.element=copy.deepcopy(self.copy_robot)
        self.copy_robot.root.set("display","none")
        #self.icon_robot.offset_x=-10
        #self.icon_robot.offset_y=-10
        self.robot_point_0.icon=self.icon_robot
        self.path_1.add_path_point(self.robot_point_0,"robot.0.0",self.path_1.layer_robot)
        #self.element_robot=self.map.getroot().find_id("robot.0.0")
        self.element_robot=self.map.root.find(f".//*[@id='robot.0.0']")
        self.element_robot_point=self.element_robot.find(".//*[@class='icon_robot']")
        self.element_robot_avoid_f=self.element_robot.find(".//*[@class='icon_avoid_f']")
        self.element_robot_avoid_r=self.element_robot.find(".//*[@class='icon_avoid_r']")
        self.element_robot_point.set("fill","green")
        self.element_robot_avoid_f.set("fill","red")
        self.element_robot_avoid_r.set("fill","red")

    def update_robot_point(self,path_pos,robot_state=RobotMapState.OK):
        """
        更新机器人点.
    
        :returns: no return
        :raises: no exception
        """
        _x,_y=self.path_1.pos_to_xy(path_pos)
        _x=_x+self.icon_robot.offset_x
        _y=_y+self.icon_robot.offset_y
        
        #print(_x,_y)
        #self.element_robot.moveto(_x,_y)
        self.element_robot.set("transform",f"translate({_x}, {_y})")
        #print(self.element_robot.tostr())
        if robot_state==RobotMapState.OK:
            self.element_robot_point.set("fill","green")
            self.element_robot_avoid_f.set("display","none")
            self.element_robot_avoid_r.set("display","none")
        elif robot_state==RobotMapState.OFFLINE:
            self.element_robot_point.set("fill","gray")
            self.element_robot_avoid_f.set("display","none")
            self.element_robot_avoid_r.set("display","none")
        elif robot_state==RobotMapState.WARNING:
            self.element_robot_point.set("fill","yellow")
            self.element_robot_avoid_f.set("display","none")
            self.element_robot_avoid_r.set("display","none")
        elif robot_state==RobotMapState.ERROR:
            self.element_robot_point.set("fill","red")
            self.element_robot_avoid_f.set("display","none")
            self.element_robot_avoid_r.set("display","none")
        elif robot_state==RobotMapState.AVOID_F:
            self.element_robot_point.set("fill","red")
            self.element_robot_avoid_f.set("display","block")
            self.element_robot_avoid_r.set("display","none")
        elif robot_state==RobotMapState.AVOID_R:
            self.element_robot_point.set("fill","red")
            self.element_robot_avoid_f.set("display","none")
            self.element_robot_avoid_r.set("display","block")
        elif robot_state==RobotMapState.AVOID_FR:
            self.element_robot_point.set("fill","red")
            self.element_robot_avoid_f.set("display","block")
            self.element_robot_avoid_r.set("display","block")

    def update_clean_point(self):
        """
        更新清扫点.
    
        :returns: no return
        :raises: no exception
        """        
        i=0
        for _state in np.nditer(path_1.clean_points.array_cleaned):
            
            if _state:
                self.element_clean_points[i].set("fill","#FCA311")
            else:
                self.element_clean_points[i].set("fill","#8D99AE")
            i=i+1

    def update_charge_point(self,charge_state=False):
        """
        更新充电点.
    
        :returns: no return
        :raises: no exception
        """
        if charge_state:
            self.charge_point_0.element.set("fill","green")
                       
        else:
            self.charge_point_0.element.set("fill","#1296db")

    def update_water_point(self,water_state=False):
        """
        更新加水点.
    
        :returns: no return
        :raises: no exception
        """
        if water_state:
            self.water_point_0.element.set("fill","green")
                       
        else:
            self.water_point_0.element.set("fill","#1296db")        

    def append_map(self):
        """
        合成地图.
    
        :returns: no return
        :raises: no exception
        """
        self.map.append(self.root)
        
        #print(self.map.to_str())
        self.map.save("test.svg")


    def update_map(self):
        """
        更新地图.
    
        :returns: no return
        :raises: no exception
        """
        #self.string=self.map.to_str() #需改encoding='UTF-8'
        self.string=etree.tostring(self.map.root,encoding='UTF-8')
        #self.doc.setContent(self.string)
        #print(self.doc.toByteArray())
      



#functions#####################################################################
svg_map = SvgMap()
svg_map.load('./map/map_base.svg')
svg_map.get_tunnel_path()
svg_map.get_copy()
svg_map.get_icon()
svg_map.set_charge_point()
svg_map.set_water_point()
svg_map.set_clean_point()
svg_map.set_clean_element()
svg_map.set_robot_point()

svg_map.append_map()
svg_map.update_map()
#svg_map.map.save("test.svg")





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