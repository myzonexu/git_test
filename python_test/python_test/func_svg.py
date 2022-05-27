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

#classes#######################################################################
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
        



#functions#####################################################################




svg_map = SvgMap('./map/map.svg')

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