from PyQt5.Qt import *
import sys
from PyQt5.QtWebEngineWidgets import *

# ui_main是.ui文件生成的.py文件名
from ui_main import Ui_mainWindow
 
class Window(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
 
    def slot1(self):
        print('QQQQQ')
 
    def func_list(self):
        self.func()
 
    def func(self):
        print("hello")
        #self.widget_monitor=QWebEngineView()
        #self.widget_monitor.load(QUrl("https://www.baidu.com/"))
        

        #self.browser=QWebEngineView()
        #self.browser.load(QUrl("http://www.baidu.com/"))

        #web = QWebEngineView(self.widget_monitor)
        #web.load(QUrl("http://www.baidu.com/"))
        #web.show()
        pass
 
 
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.func_list()
    window.show()
    sys.exit(app.exec_())

