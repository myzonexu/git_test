import cv2
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *
import threading


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
class CameraRtsp():
    def __init__(self,username,passwd,ip,port=554,channel=1,codec="h264",pc_test=False):
        self.username = username
        self.passwd = passwd
        self.ip = ip
        self.port = port
        self.channel = channel
        self.codec = codec
        self._has_init = False
        self.pc_test = pc_test
        self.get_url()
        self.web_url()
    def has_init(self):
        return self._has_init
    def get_url(self):
        self.url = "rtsp://" + self.username + ":" + self.passwd + "@" + self.ip + ":" + str(self.port) + "/" + self.codec + "/ch" + str(self.channel) + "/main/av_stream"
        return self.url
    def set_ip(self,ip):
        self.ip = ip
        self.get_url()
        return self.url
    def web_url(self):
        self.web_url = "http://" + self.ip
        return self.web_url

    def init(self):
        try:
            if self.pc_test:
                self.cap = cv2.VideoCapture(0)
                self.cap.open(0, cv2.CAP_DSHOW)
            else:
                self.cap = cv2.VideoCapture(self.url)
            
        #except cv2.error as e:
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
                print("相机原始分辨率：",self.width_camera,self.height_camera)
            else:
                self._has_init = False
                print("初始化捕获视频失败")
        return self.cap

    def set_show_width(self,width):
        self.show_width = width
    def set_show_height(self,height):
        self.show_height = height
    #通过显示区域高度计算图像缩放后的宽度、调度
    def set_show_aera_from_height(self,height):
        self.show_height = height
        self.show_width = int(height * self.ratio_w_h)
        return self.show_width,self.show_height
    #在label中显示捕获视频，自动缩放使视频高度适应父显示区高度
    def show_on_label(self,show_label):
        if self.has_init():
            pass
        else:
            self.init()
        
        if self.cap.isOpened():
            has_frame,frame = self.cap.read()
            if has_frame:
                #获取父件高度
                #self.set_show_aera_from_height(show_label.parentWidget().parentWidget().height())
                self.set_show_width(show_label.parentWidget().parentWidget().width())
                self.set_show_height(show_label.parentWidget().parentWidget().height())

                #使用opencv缩放有可能出错，不用
                #frame=cv2.resize(frame, (width,height))

                #水平翻转
                #frame=cv2.flip(frame,1)

                #opencv 默认图像格式是rgb，qimage要使用BRG,这里进行格式转换
                frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

                #mat-->qimage
                img = QImage(frame.data,frame.shape[1],frame.shape[0],QImage.Format_RGB888)

                #图像缩放
                img = img.scaled(self.show_width,self.show_height)
                
                show_label.setPixmap(QPixmap.fromImage(img))
            else:
                print("未获取到frame",has_frame)
                pass
        else:
            print("未启动相机")
        #关闭相机
        def close(self):        
            if self.cap.isOpened():
                #断开
                self.cap.release()


#显示视频
def do_show_camera(window,master,camera):
    while 1:
        if master.is_opened() and master.is_reconnect() == False and window.tabWidget_main.currentIndex()==0:
        #if True :
            camera.show_on_label(window.label_camera)

        else:
            pass



#相机web页面
def set_camera_browser(camera,show_area):
    browser = QWebEngineView()
    browser.load(QUrl(camera.web_url))
    show_area.setWidget(browser)


#变量定义
#海康相机rtsp地址username,passwd,ip
camera_robo = CameraRtsp(username="admin",passwd="ylcx6666",ip="192.168.1.64",pc_test=True)
#print(camera.url)


