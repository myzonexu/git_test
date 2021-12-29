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




