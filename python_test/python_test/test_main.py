'''
#测试海康相机###############################################################
import cv2
#url = "rtsp://admin:ylcx6666@192.168.1.64/Streaming/Channels/1"
url = "rtsp://admin:ylcx6666@192.168.1.64:554/h264/ch1/main/av_stream"
cap = cv2.VideoCapture(url)
ret, frame = cap.read()
while ret:
    ret, frame = cap.read()
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
#测试海康相机###############################################################
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