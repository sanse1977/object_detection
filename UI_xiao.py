# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_xiao.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(900, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(900, 720))
        MainWindow.setMaximumSize(QtCore.QSize(900, 720))
        font = QtGui.QFont()
        font.setFamily("楷体")
        # font.setBold(True)
        font.setItalic(False)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.videoLabel = QtWidgets.QLabel(self.centralwidget)
        self.videoLabel.setGeometry(QtCore.QRect(50, 105, 630, 390))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoLabel.sizePolicy().hasHeightForWidth())
        self.videoLabel.setSizePolicy(sizePolicy)
        self.videoLabel.setText("")
        self.videoLabel.setObjectName("videoLabel")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(295, 503, 121, 24))
        font = QtGui.QFont()
        font.setFamily("楷体")
        # font.setBold(True)
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("*{\n"
"color: #009ACD;\n"
"}")
        self.label_2.setObjectName("label_2")

        font1 = QtGui.QFont()
        font1.setFamily("楷体")
        font1.setPointSize(15)

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(150, 540, 500, 24))
        self.label_7.setStyleSheet("*{\n"
                                   "color: #009ACD;\n""}")
        self.label_7.setObjectName("label_7")
        self.label_7.setWordWrap(True)
        self.label_7.setFont(font1)


        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(150, 570, 500, 24))
        self.label_8.setStyleSheet("*{\n"
                                   "color: #009ACD;\n""}")
        self.label_8.setObjectName("label_7")
        self.label_8.setWordWrap(True)
        self.label_8.setFont(font1)

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(150, 600, 500, 24))
        self.label_9.setStyleSheet("*{\n"
                                   "color: #009ACD;\n""}")
        self.label_9.setObjectName("label_7")
        self.label_9.setWordWrap(True)
        self.label_9.setFont(font1)

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(680, 105, 20, 645))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.stopBtn = QtWidgets.QPushButton(self.centralwidget)
        self.stopBtn.setGeometry(QtCore.QRect(180, 650, 111, 41))
        self.stopBtn.setObjectName("stopBtn")
        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(430, 650, 111, 41))
        self.startBtn.setObjectName("startBtn")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(280, 30, 301, 51))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(28)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("*{color: #009ACD;}")
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setObjectName("label_5")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(700, 105, 190, 590))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        # self.label_4.setFont(font)
        # self.label_4.setStyleSheet("*{\n"
        #                            "color: red;\n"
        #                            "}")
        # self.label_4.setObjectName("label_4")
        # self.verticalLayout_2.addWidget(self.label_4)

        self.textBrowser = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)

        self.imgLabel = QtWidgets.QLabel(self.layoutWidget)
        #self.imgLabel.setGeometry(QtCore.QRect(1, 420, 200, 500))  # 180, 130, 451, 261
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imgLabel.sizePolicy().hasHeightForWidth())
        self.imgLabel.setSizePolicy(sizePolicy)
        self.imgLabel.setText("")
        self.imgLabel.setObjectName("imgLabel")
        self.imgLabel.setFixedSize(190, 180)
        self.imgLabel.setStyleSheet(
            "font:'楷体';border-width: 1px;border-style: solid;border-color: rgb(255, 255, 255);")
        self.verticalLayout_2.addWidget(self.imgLabel)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.imgLabel.setFont(font)
        font.setPointSize(10)
        self.textBrowser.setFont(font)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(3, 250, 121, 24))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("*{color: #009ACD;}\n"
"\n"
"\n"
"")
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "监控视频异常检测"))
        self.label_2.setText(_translate("MainWindow", "系统说明"))
        self.stopBtn.setText(_translate("MainWindow", "停止检测"))
        self.startBtn.setText(_translate("MainWindow", "重新检测"))
        self.label_5.setText(_translate("MainWindow", "监控视频异常检测"))
        # self.label_4.setText(_translate("MainWindow", "系统状态："))
        self.label_3.setText(_translate("MainWindow", "检测源："))
        self.label_7.setText(_translate("MainWindow", "1.本系统用于监控视频下的异常人员进行检测；"))
        self.label_8.setText(_translate("MainWindow","2.本系统采用了一种基于均值哈希匹配的算法；"))
        self.label_9.setText(_translate("MainWindow", "3.本系统通过调用OPC服务器控制机器的运行状态。"))


