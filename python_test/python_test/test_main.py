
'''
from func_task import *

print(task_plans.new_plan.__dict__)
'''

'''
#测试枚举
from func_defines import *

print(RunState['WORK'])
print(CtrlMode.MANUAL.string)
print(RunState(1).string)
'''
'''
#测试位操作运算
from func_common import *
import struct

if __name__ == "__main__":
    a=0b110101110010
    b=get_bits(a, 2,9)
    print(f'{a:#016b}')
    print(f'{b:#016b}')
'''

"""
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Calendar1.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 667)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.workless_day_fn = None
        self.workless_date_list = []
        self.workless_day_read_path = "workless_day.txt"
        # self.calendarWidget.clicked.connect(self.single_click)  # 关联单击事件
        self.calendarWidget.activated.connect(self.double_click)  # 关联双击事件
        self.calendarWidget.setGeometry(QtCore.QRect(60, 60, 481, 451))
        self.calendarWidget.setFirstDayOfWeek(QtCore.Qt.Sunday)
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.LongDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setDateEditAcceptDelay(1500)
        self.calendarWidget.setObjectName("calendarWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.set_to_red_or_black()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Calender"))

    def double_click(self):
        date = self.calendarWidget.selectedDate()  # 获取当前被选中的日期
        date_str = str(date.toPyDate())
        if date_str in self.workless_date_list:
            self.set_to_blank()
            self.workless_date_list.remove(date_str)
        else:
            self.set_to_red()
            self.workless_date_list.append(date_str)
        self.workless_day_write()

    def workless_day_read(self):
        try:
            self.workless_day_fn = open(self.workless_day_read_path, "r+")
            for line in self.workless_day_fn.readlines():
                if (line.strip("\n") not in self.workless_date_list):
                    self.workless_date_list.append(line.strip("\n"))
        except:
            self.workless_day_write()
        self.workless_day_fn.close()

    def workless_day_write(self):
        self.workless_day_fn = open(self.workless_day_read_path, "w")
        for i in range(len(self.workless_date_list)):
            self.workless_day_fn.write("{}\n".format(self.workless_date_list[i]))
        self.workless_day_fn.close()

    def set_to_red(self):  # 设置颜色为红色
        cmd_fmt = QtGui.QTextCharFormat()
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('Red'))

        cmd_fmt.setForeground(brush)
        self.calendarWidget.setDateTextFormat(self.calendarWidget.selectedDate(), cmd_fmt)

    def set_to_blank(self):  # 去掉背景色
        cmd_fmt = QtGui.QTextCharFormat()
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor('Black'))
        cmd_fmt.setForeground(brush)
        self.calendarWidget.setDateTextFormat(self.calendarWidget.selectedDate(), cmd_fmt)

    def set_to_red_or_black(self):#再次启动程序是对日历控件修改
        first_day = QtCore.QDate()
        first_day.setDate(self.calendarWidget.yearShown(), self.calendarWidget.monthShown(), 1)
        days = first_day.daysInMonth()
        cmd_fmt = QtGui.QTextCharFormat()
        brush = QtGui.QBrush()
        for i in range(days):
            self.workless_day_read()
            date_str = str(first_day.addDays(i).toPyDate())
            if date_str in self.workless_date_list:
                brush.setColor(QtGui.QColor('Red'))
                cmd_fmt.setForeground(brush)
                self.calendarWidget.setDateTextFormat(first_day.addDays(i), cmd_fmt)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()  # 生成类实例对象
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
"""

'''
import sys
import os
from PyQt5.Qt import QMainWindow,QApplication
from ui_test import Ui_MainWindow
from PyQt5.QtSvg import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QFile, QIODevice, QModelIndex, QAbstractItemModel
from PyQt5.QtXml import QDomDocument
from PyQt5 import QtSvg
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, Close
from svg.path import parse_path
#class RenderArea(QWidget):
#    def __init__(self):
#        super().__init__()

#    def paintEvent(self, event):
        
#        painter = QPainter(self)
#        painter.save()
                
#        self.draw(event,painter)
#        painter.restore()
#    def draw(self,event,painter):
#        #self.renderer =QSvgRenderer("map.svg")
#        self.renderer =QSvgRenderer(doc.toByteArray())
#        #self.renderer.render(painter)
#        self.map_item = QGraphicsSvgItem()
#        self.map_item.setSharedRenderer(self.renderer)
#        self.map_item.setElementId("path1937")
#        #self.renderer.render(painter,QRectF(0,0,100,100))
#        self.renderer.render(painter)


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    #加载地图
    def load_map(self):
        self.svgWidget = QtSvg.QSvgWidget()
        self.scrollArea_2.setWidget(self.svgWidget)
        
        with open('./map/map.svg', 'r',encoding='UTF-8') as f:
            file_size=os.path.getsize('./map/map.svg')
            #file=QString(f.read())
            file=f.read()
            print(type(file))
        
        #self.map_svg=QByteArray()
        #self.map_svg.append(file)
        #self.svgWidget.load(self.map_svg)

        self.doc = QDomDocument('map')
        self.doc.setContent(file)
        #self.docElem = self.doc.documentElement()
        self.elem_robot=self.doc.elementsByTagName("ellipse").item(0).toElement()
        self.elem_path=self.doc.elementsByTagName("path").item(0).toElement()
        self.svgWidget.load(self.doc.toByteArray())
        

    @pyqtSlot(int)
    def on_horizontalSlider_valueChanged(self,cx):
        #path1 = parse_path('m 105.55796,42.191564 -49.859422,10e-7 -7.688792,-8.525182 H 33.376242 l -9.300956,8.525182 -23.31859798,-10e-7')
        path1 = parse_path(self.elem_path.attribute("d"))
        length=path1.length()        
        pos=path1.point(cx/length)
        print(pos.real,pos.imag )
        self.elem_robot.setAttribute("cx",str(pos.real))
        self.elem_robot.setAttribute("cy",str(pos.imag))

        #self.elem_robot.setAttribute("cx",str(cx))
        self.svgWidget.load(self.doc.toByteArray())
        #self.scrollArea_2.repaint()
        pass

    ##显示SVG地图
    #x=0
    #def show_map(self):
    #    render=self.svgWidget.renderer()
    #    global x
    #    x=x+1
    #    render.setAspectRatioMode(Qt.KeepAspectRatio)
    #    render.setViewBox(QRect(x,10,100,80))
    #    self.scrollArea_map.repaint()
    #    #render.repaintNeeded.connect(window.scrollArea_map.repaint)



def test_svg_length():
    #path1 = parse_path('M100,100L300,100L200,300z')
    path1 = parse_path('m 105.55796,42.191564 -49.859422,10e-7 -7.688792,-8.525182 H 33.376242 l -9.300956,8.525182 -23.31859798,-10e-7')
    print(path1.length())
    pos=path1.point(1)
    print(pos.real,pos.imag )


    pass


if __name__ == '__main__':    
    #doc = QDomDocument('map')
    #load_xml(doc)
    app = QApplication(sys.argv)
    window = Window()
    window.load_map()
    window.show()
    #test_svg_length()

    
    sys.exit(app.exec_())

'''






'''
#测试海康相机###############################################################
import cv2
import argparse
url = "rtsp://admin:ylcx6666@192.168.1.64/Streaming/Channels/1"
#url = "rtsp://admin:ylcx6666@192.168.1.64:554/h264/ch1/main/av_stream"
cap = cv2.VideoCapture(0)
cap.open(0, cv2.CAP_DSHOW)
ret, frame = cap.read()
while ret:
    ret,frame = cap.read()
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
#测试海康相机###############################################################
'''

'''
#测试svg读取显示###############################################################
import sys
from PyQt5 import QtGui, QtSvg
from PyQt5.Qt import QMainWindow,QApplication

app = QApplication(sys.argv) 
svgWidget = QtSvg.QSvgWidget('map.svg')
#svgWidget.setGeometry(50,50,759,668)
svgWidget.show()

sys.exit(app.exec_())



#测试svg读取显示###############################################################
'''
'''
#测试相机，多线程，信号槽###############################################################
import sys
from PyQt5.Qt import QMainWindow,QApplication
import threading
from ui_test import Ui_MainWindow

from func_camera import *

#线程管理
def get_camera_frame(camera):
    while True:
        camera.get_frame()
        

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':    
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    camera=CameraRtsp(pc_test=True)
    camera.frame_captured.connect(lambda:window.label.setPixmap(QPixmap.fromImage(camera.img)))
    thread_camera = threading.Thread(target=get_camera_frame, args=(camera,),name='thread_camera')
    thread_camera.start()
    sys.exit(app.exec_())
#测试相机，多线程，信号槽###############################################################
'''
'''
#测试JSON转换###############################################################

import json
from dataclasses import dataclass

@dataclass
class TaskState:
    #['任务ID', 'robot_ID', '起点', '终点','途经点', '优先级', '等待信号']
    id : int
    robot_id : int=0
    start_point : int=0
    end_point : int=0
    way_point :int=0
    priority : int=0
    wait_button : int =0


table_task_state=[]

for id in range(10):
    table_task_state.append(TaskState(id))

print(table_task_state[0].__dict__)
json_str = json.dumps(table_task_state[0], default=lambda o: o.__dict__, indent=4)
print(json_str)

with open('data.json', 'w') as f:
    json.dump(table_task_state[0],f, default=lambda o: o.__dict__,  indent=4)
with open('data.json', 'r') as ff:
    data = json.load(ff)
print(data.get("id"))

#测试JSON转换###############################################################

'''

