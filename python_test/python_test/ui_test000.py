# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_test.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
import time
from PyQt5.Qt import QApplication,QMainWindow

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(QMainWindow,object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(818, 663)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 818, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.num=0
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "新建列"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "序号"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "描述"))

    def set_timer(self):
        self.timer2 = QtCore.QTimer()  # 初始化一个定时器
        self.timer2.timeout.connect(lambda:self.test())  # 每次计时到时间时发出信号
        self.timer2.start(1000)

    def test(self):
        #self.tableWidget.setRowCount(100)
        #self.tableWidget.setItem(self.num,0,QtWidgets.QTableWidgetItem(str(self.num)))

        self.model.setItem(self.num,0,QtGui.QStandardItem(str(self.num)))

        #self.tableWidget.viewport().update()
        print(self.num)
        self.num=self.num+1

    def set_tableview(self):
        #设置数据层次结构，4行4列
        self.model=QtGui.QStandardItemModel(10,4)
        #设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['标题1','标题2','标题3','标题4'])

        for row in range(10):
            for column in range(4):
                item=QtGui.QStandardItem('row %s,column %s'%(row,column))
                #设置每个位置的文本值
                self.model.setItem(row,column,item)

        #实例化表格视图，设置模型为自定义的模型

        self.tableView.setModel(self.model)



if __name__ == '__main__':  
    
    app = QApplication(sys.argv)
    win = Ui_MainWindow()
    win.setupUi(win)
    win.set_tableview()
    win.show()
    win.test()
    win.test()
    win.test()
    win.set_timer()
    sys.exit(app.exec_())