#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
File   Name ： dialog_about.py
Description :  关于对话框
Author      :  simon
Create Time ： 2022.5.20
-------------------------------------------------------------------------------
Change Activity:
               时间:更改内容
-------------------------------------------------------------------------------
"""
__author__ = 'simon'


from ui_about import Ui_Dialog_about
from PyQt5.Qt import *

class DialogAbout(QDialog,Ui_Dialog_about):
    #初始化###################################################################################################
    def __init__(self):
        super().__init__()
        self.setupUi(self)
       
       

    def func_list(self):
        pass


