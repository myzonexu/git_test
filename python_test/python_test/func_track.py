#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
File   Name ： func_track.py
Description :  轨迹
Author      :  simon
Create Time ： 2022.5.23
-------------------------------------------------------------------------------
Change Activity:
               时间:更改内容
-------------------------------------------------------------------------------
"""

__author__ = 'simon'

import datetime
import copy
from func_defines import *

#classes#######################################################################
class Track(object):  
    """类定义，一段轨迹."""
    def __init__(self):
        """初始化."""
        self.pos_start=0
        self.pos_end=0
        self.time_start = DATETIME_NONE
        self.time_end = DATETIME_NONE
        self.action_drive=DriveAction.STOP
        self.action_arm=ArmAction.ORIGIN
    
    def start(self,pos,drive_action,arm_action):
        """
        轨迹开始.
    
        :param pos: float,路径位置
        :param drive_action: enum,行驶动作
        :param arm_action: enum,机械臂动作
        :returns: no return
        :raises: no exception
        """
        self.time_start = datetime.now()
        self.pos_start=pos
        self.pos_end=pos
        self.action_drive=drive_action
        self.action_arm=arm_action
            
    def end(self):
        """
        轨迹结束.
    
        :returns: no return
        :raises: no exception
        """
        self.time_end = datetime.now()

class Tracks(object):
    """类定义，轨迹集合."""
    def __init__(self):
        """初始化."""
        #self.new=Track()
        self.current=Track()
        self.all=[]    
 
    def record(self,speed,pos,arm_action):
        """
        记录轨迹.
     
        :param speed: float,速度
        :param pos: float,位置
        :param arm_action: enum,机械臂动作
        :returns: no return
        :raises: no exception
        """
        action_drive_last=self.current.action_drive
        action_arm_last=self.current.action_arm
        
        if speed>2:
            drive_action=DriveAction.FORWORD
        elif speed<-2:
            drive_action=DriveAction.BACKWORD
        else:
            drive_action=DriveAction.STOP
        
        if self.current.time_start == DATETIME_NONE:
            self.current.start(pos,drive_action,arm_action)
        else:
            if drive_action==action_drive_last and arm_action==action_arm_last:
                self.current.pos_end=pos
                self.current.time_end = datetime.now()
            else:
                self.all.append(copy.deepcopy(self.current))
                self.current.__init__()
                self.current.start(pos,drive_action,arm_action)


#functions#####################################################################






