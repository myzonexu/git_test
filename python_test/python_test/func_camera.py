import cv2
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QObject , pyqtSignal
from func_common import *

#opencv读取监控rtsp
#海康的rtsp协议格式如下：
#rtsp://[username]:[passwd]@[ip]:[port]/[codec]/[channel]/[subtype]/av_stream
#主码流：
#rtsp://admin:12345@192.168.1.64:554/h264/ch1/main/av_stream
#rtsp://admin:12345@192.168.1.64:554/MPEG-4/ch1/main/av_stream
#子码流：
#rtsp://admin:12345@192.168.1.64/mpeg4/ch1/sub/av_stream
#rtsp://admin:12345@192.168.1.64/h264/ch1/sub/av_stream

#实机测试以下两种url均可
#url = "rtsp://admin:ylcx6666@192.168.1.64/Streaming/Channels/1"
#url = "rtsp://admin:ylcx6666@192.168.1.64:554/h264/ch1/main/av_stream"

#海康相机rtsp视频流
#pc_test=True时为使用电脑自带摄像头测试，pc_test=False时使用实机测试
class CameraRtsp(QObject):
    frame_captured = pyqtSignal()
    frame_no_captured = pyqtSignal()
    inited=pyqtSignal()
    export_attr_names=["ip"]
    def __init__(self,username="admin",passwd="ylcx6666",ip="192.168.0.64",port=554,channel=1,codec="h265",pc_test=False):
        super().__init__()
        self._capture_enable=True
        self.url=""
        self.web_url=""
        self.username = username
        self.passwd = passwd
        self.ip = ip
        self.port = port
        self.channel = channel
        self.codec = codec
        self._has_init = False
        self.pc_test = pc_test
        self.ratio_w_h=16/9
        self.show_width=None
        self.show_height=None
        self.is_web_open=False
        self.frame=None
        self.img=QImage()
        self.img_scaled=QImage()

        self.get_rtsp_url()
        self.get_web_url()

    def enable_capture(self):
        self._capture_enable=True
    def disable_capture(self):
        self._capture_enable=False
    def has_init(self):
        return self._has_init
    def get_rtsp_url(self):
        self.url = "rtsp://" + self.username + ":" + self.passwd + "@" + self.ip + ":" + str(self.port) + "/" + self.codec + "/ch" + str(self.channel) + "/sub/av_stream"
        return self.url
    def set_ip(self,ip):
        self.ip = ip
        self.get_url()
        return self.url
    def get_web_url(self):
        self.web_url = "http://" + self.ip
        #print(self.web_url)
        return self.web_url

    def init(self):
        try:
            if self.pc_test:
                self.cap = cv2.VideoCapture(0)
                self.cap.open(0, cv2.CAP_DSHOW)
            else:
                self.cap = cv2.VideoCapture(self.url)

        except Exception as e:             
            print("启动摄像机失败，请检测网络连接或连接配置,异常：",str(e))
        else:
            print("启动摄像机成功")
        finally:
            pass

        if self.cap.isOpened():
            has_frame,frame = self.cap.read()
            if has_frame:
                self.width_camera = frame.shape[1]
                self.height_camera = frame.shape[0]
                self.ratio_w_h = self.width_camera / self.height_camera
                self._has_init = True

                self.inited.emit()
                print("相机原始分辨率：",self.width_camera,self.height_camera)
            else:
                self._has_init = False
                print("初始化捕获视频失败")
        return self.cap

    #获取帧
    #@get_run_time
    def get_frame(self):
        if self.has_init():
            pass
        else:
            self.init()
        
        if self._capture_enable and self.cap.isOpened():
            has_frame,frame = self.cap.read()
            if has_frame:
                #水平翻转
                #frame=cv2.flip(frame,1)
                #opencv 默认图像格式是rgb，qimage要使用BRG,这里进行格式转换
                self.frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)               
                #mat-->qimage
                #self.img = QImage(self.frame.data,self.frame.shape[1],self.frame.shape[0],QImage.Format_RGB888) 
                        
                self.frame_to_img_scale()
                
                self.frame_captured.emit()
                #print("获取到frame")
            else:
                print("未获取到frame",has_frame)
                self._has_init = False
                self.frame_no_captured.emit()
                pass
        else:
            #print("未启动相机")
            pass

    #帧缩放    
    def frame_to_img_scale(self,scale_by_cv=False):
        if self.show_width is None:
            self.img = QImage(self.frame.data,self.frame.shape[1],self.frame.shape[0],QImage.Format_RGB888)
            self.img_scaled =self.img
        else:
            if scale_by_cv:
                frame_scaled = cv2.resize(self.frame, (self.show_width, self.show_height))
                self.img = QImage(frame_scaled.data,frame_scaled.shape[1],frame_scaled.shape[0],QImage.Format_RGB888)
            else:
                self.img = QImage(self.frame.data,self.frame.shape[1],self.frame.shape[0],QImage.Format_RGB888)
                self.img_scaled =self.img.scaled(self.show_width, self.show_height)        
        return self.img_scaled

    def frame_scale(self,height):
        self.img_scaled =self.img.scaled(int(height*self.ratio_w_h),height)
        return self.img_scaled

    #关闭相机
    def close(self):        
        if self.cap.isOpened():
            #断开
            self.cap.release()
        return self.img

    



    ##########################################################################################
    def set_show_width(self,width):
        self.show_width = width
    def set_show_height(self,height):
        self.show_height = height
    #通过显示区域高度计算图像缩放后的宽度、调度
    def set_show_aera_from_height(self,height):
        self.show_height = height
        self.show_width = int(height * self.ratio_w_h)
        return self.show_width,self.show_height


