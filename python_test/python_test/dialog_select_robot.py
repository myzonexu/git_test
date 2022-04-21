#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
File   Name ： dialog_select_robot.py
Description :  选择机器人对话框
Author      :  simon
Create Time ： 2022.4.17
-------------------------------------------------------------------------------
Change Activity:
               时间:更改内容
-------------------------------------------------------------------------------
"""
__author__ = 'simon'


from ui_select_robot import Ui_Dialog_select_robot
from PyQt5.Qt import *

class Dialog(QDialog,Ui_Dialog_select_robot):
    #初始化###################################################################################################
    def __init__(self):
        super().__init__()
        self.setupUi(self)
       

    def func_list(self):
        pass

#dialog_select_robot=Dialog()

