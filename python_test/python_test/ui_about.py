# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_about.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_about(object):
    def setupUi(self, Dialog_about):
        Dialog_about.setObjectName("Dialog_about")
        Dialog_about.resize(400, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_about.sizePolicy().hasHeightForWidth())
        Dialog_about.setSizePolicy(sizePolicy)
        Dialog_about.setMinimumSize(QtCore.QSize(400, 300))
        Dialog_about.setMaximumSize(QtCore.QSize(400, 300))
        self.label = QtWidgets.QLabel(Dialog_about)
        self.label.setGeometry(QtCore.QRect(5, 0, 390, 81))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/main_window/img/logo1.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(Dialog_about)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 100, 134, 50))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)

        self.retranslateUi(Dialog_about)
        QtCore.QMetaObject.connectSlotsByName(Dialog_about)

    def retranslateUi(self, Dialog_about):
        _translate = QtCore.QCoreApplication.translate
        Dialog_about.setWindowTitle(_translate("Dialog_about", "关于"))
        self.label_2.setText(_translate("Dialog_about", "隧道清扫机器人控制系统"))
        self.label_3.setText(_translate("Dialog_about", "版本：0.1.0"))
        self.label_4.setText(_translate("Dialog_about", "更新时间：2022.5.20"))
import image_rc
