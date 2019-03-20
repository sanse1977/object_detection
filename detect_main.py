import sys
import os
import cv2
import pickle
import time
import inspect
import ctypes
import datetime
import threading
import numpy as np
import data_access as da
from utils import Timer
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from UI_xiao import Ui_MainWindow
from PyQt5.QtGui import QImage, QPixmap
from opcua import Client
from opcua import ua


class XiaoAll(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(XiaoAll, self).__init__(parent)
        self.setupUi(self)
        # self.textBrowser.append('系统启动中....')
        self.i = 0
        self.imgLabel.setText(' 当前无异常')
        self.cap = None
        self.frame = None
        self.res1 = False
        self.res2 = False
        self.count = 0
        self.count1 = 0
        self.count2 = 0
        self.result = False
        self.string = ''
        self.es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        self.threshold_1 = 250000
        # self.threshold_2 = 10000000
        self.text = 'No Person!!!'
        self.flag = False  # 保存一帧图像后flag = False
        self.flag1 = False
        self.mask1 = cv2.imread('imgCut/mask.jpg')
        self.back = None
        self.background = None
        # self.ndarray = self.loadImg('img/img.pkl')
        self.ndarrayleft = self.loadRoiImage('img/leftImg.pkl')
        self.ndarrayright = self.loadRoiImage('img/rightImg.pkl')
        self.ndarraymiddle = self.loadRoiImage('img/middleImg.pkl')
        self.flagStop = False
        self.client = Client("ocp.tcp://10.19.3.35:49320")
        self.node_info = "ns=2;s=xinsawaninihoudaoxianti.QCPU.光栅触发暂停标志"
        self.isStopFlag = True
        self.node = None
        self.threadFlag = 1
        # self.stopBtn.clicked.connect(self.stop)
        # self.startBtn.clicked.connect(self.start)
        gray = cv2.cvtColor(self.mask1, cv2.COLOR_BGR2GRAY)
        binary = cv2.threshold(gray, 55, 255, cv2.THRESH_BINARY)[1]
        self.contours = cv2.findContours(binary.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        self.count00 = 0
        self.thread_video_receive = threading.Thread(target=self.video_receive_rstp)  # 该线程用来读取视频流
        # self.thread_video_receive = threading.Thread(target=self.video_receive_local)  # 该线程用来读取视频流
        self.thread_video_receive.start()

        self.thread_time = Timer('updatePlay', sleep_time=0.07)  # 该线程用来每隔0.04秒在label上绘图
        self.thread_time.updateTime.connect(self.video_play)
        self.thread_time.start()

        self.thread_video_deal = Timer('drawVideo', sleep_time=0.04)  # 该线程用来处理视频
        self.thread_video_deal.updateTime.connect(self.deal_frame)
        self.thread_video_deal.start()

        # self.thread_video_diff = Timer('frameDiff', sleep_time=0.5)  # 该线程用来右上角帧差
        # self.thread_video_diff.updateTime.connect(self.frameDelta)
        # self.thread_video_diff.start()

        self.thread_video_stop = Timer('stopFlag', sleep_time=3)
        self.thread_video_stop.updateTime.connect(self.detect_isStopFlag)  # 读取机器是否停机信号
        self.thread_video_stop.start()
        # self.textBrowser.append('系统已经启动！！！！')

        self.thread_opc_stop = Timer('stopOpc', sleep_time=180)
        self.thread_opc_stop.updateTime.connect(self.connect)
        self.thread_opc_stop.start()



    def stop(self):

        reply = QMessageBox.question(self, '信息', '确认停止检测吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.flagStop = True
            self.textBrowser.append('停止检测！！！')
        else:
            pass

    def start(self):

        reply = QMessageBox.question(self, '信息', '确认重新检测吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.flagStop = False
            self.textBrowser.append('重新检测！！！')
        else:
            pass

    def closeEvent(self, event):

        reply = QMessageBox.question(self, '信息', '确认退出吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            os._exit(0)
        else:
            event.ignore()

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)

    def connect(self):
        try:
            self.client.connect()
            self.node = self.client.get_node(self.node_info)
            # self.isStopFlag = self.node.get_value()
        except Exception as e:
            self.textBrowser.append('opc断开连接,正在尝试连接！')
            # self.isStopFlag = True

        # try:
            # self.count = 1
        # except Exception as e:
        #     self.flagStop = True
        #     print(e)
            # self.thread_opc_stop.start()
            # self.thread_video_stop.stop_thread()
            # self.stop_machine()
            # self.count00 = 0


    def reconnect(self):
        try:
            self.client.connect()
            self.textBrowser.append('重新连接成功!')
            self.stop_thread(self.thread_opc_stop)
            # self.count = 1
        except Exception as e:
            self.textBrowser.append('opc断开连接,正在尝试连接！')
            # self.thread_video_stop.stop_thread()
            # self.stop_machine()
            # self.count00 = 0


    def stop_machine(self):

        self.node.set_attribute(ua.AttributeIds.Value, ua.DataValue(variant=ua.Variant(True)))
        self.isStopFlag = self.node.get_value()
        self.textBrowser.append('机器停机,停止检测！！！')
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.textBrowser.append('时间:' + time)
        # self.flag1 = False
        # self.textBrowser.append(str(self.node.get_value()))
        # self.node.set_attribute(ua.AttributeIds.Value, ua.DataValue(variant=ua.Variant(False)))时间

    def detect_isStopFlag(self):

        if self.isStopFlag is False and self.count00 == 0:
            self.textBrowser.append('机器启动,开始检测！！！！')
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.textBrowser.append('时间:' + time)
            self.count00 = 1
            # self.res1 = False
            # self.thread_video_diff.resume()
        try:
            self.isStopFlag = self.node.get_value()
            if self.threadFlag == 1:
                self.textBrowser.append('opc连接成功！')
                self.threadFlag = 0
        except Exception as e:
            self.isStopFlag = True

    def deal_frame(self):

        if self.result or self.res1:
            self.res1 = False
            self.result = False

        if self.flagStop is False and self.frame is not None:

            self.count += 1
            self.count = self.count % 10

            if self.count == 0 and self.isStopFlag is False:

                self.video_recog()

            # if self.isStopFlag is False and self.result is True:
            #     self.stop_machine()
            #     self.count00 = 0
            #     # self.count = self.count % 10

            # if self.result:
            #     self.save_img(self.frame)
            # else:
            #     self.text = 'No Person!!!'

            # time.sleep(20)
            # self.node.set_attribute(ua.AttributeIds.Value, ua.DataValue(variant=ua.Variant(False)))
            # self.isStopFlag = self.node.get_value()
            # self.textBrowser.append(str(self.isStopFlag))

        # else:
        #     cv2.putText(self.frame, "Room Status: No Person!!!", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
        #                 (0, 255, 0), 2)
        # elif self.flagStop is True and self.isStopFlag is False:
        #     self.stop_machine() # flagStop = True
        # else:
        #     print(123)
        #     pass

    def video_receive_local(self, cam='testvideo/mixVideo.avi', time_flag=True):
        '''该方法用来接收本地视频
        :param cam: 摄像头数据源
        :return: None
        '''

        self.cap = cv2.VideoCapture(cam)
        if self.cap.isOpened() is False:
            self.stop_machine()
            self.textBrowser.append('摄像头连接不上,请检查网络摄像头后重新启动系统!')
            f1 = open('time.txt', 'w')
            currenttime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            f1.writelines(currenttime+'摄像头连接不上!')
            self.cap = cv2.VideoCapture(cam)
            f1.close()

        ret, frame = self.cap.read()
        while self.cap.isOpened():
            self.frame = frame

            while ret is False:
                self.cap = cv2.VideoCapture(cam)
                ret, frame = self.cap.read()
                self.frame = frame

            ret, frame = self.cap.read()
            if time_flag is True:
                time.sleep(0.01)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        # if self.count2 == 0:
        #     self.textBrowser.append('系统已经启动！！！')
        #     self.count2 += 1


    def video_receive_rstp(self, cam='rtsp://user:xiolift123@10.19.31.154:554/ch2'):
        '''该方法用来接收网络视频
        :param time_flag:
        :param cam: 左摄像头数据源
        :return: None
        '''
        self.video_receive_local(cam=cam, time_flag=False)

    def video_recog(self):
        '''
        视频识别部分
        :return:
        '''
        frame = self.frame  # 原始彩色图，摄像头

        # Xentire = self.imgProcess(frame, (260, 612, 470, 1110), (3, 3), self.ndarray, 10)
        Xleft = self.imgProcess(frame, (420, 612, 470, 570), (3, 3), self.ndarrayleft, 11)
        Xright = self.imgProcess(frame, (260, 340, 1010, 1110), (3, 3), self.ndarrayright, 14)
        Xmiddle = self.imgProcess(frame, (310, 400, 550, 650), (3, 3), self.ndarraymiddle, 15)

        self.frameDelta()
        self.result = self.detect_person(Xleft, Xright, Xmiddle)
        if self.isStopFlag is False and self.result is True:
            self.stop_machine()
            self.count00 = 0
            self.save_img(frame)
        else:
            self.text = 'No Person!!!'

    def save_img(self, frame):

            self.text = 'Detecting Person!!!'

            #self.textBrowser.append('有人进入！')

            currenttime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            self.string = 'detectimg/img' + str(currenttime) + '.png'
            cv2.imwrite(self.string, frame)
            jpg = QPixmap(self.string) #.scaled(self.imgLabel.width(), self.imgLabel.height())
            self.imgLabel.setPixmap(jpg)
            self.imgLabel.setScaledContents(True)
            # detectTime = da.detectTime()
            # detectTime.insert(self.string)
            # self.flag = True

            # self.count1 = self.count

        # elif self.count - self.count1 > 10:
        #     self.text = 'No Person!!!'
        #     self.flag = False


    def video_play(self):

        if self.frame is not None:

            if self.text == 'No Person!!!':
                cv2.putText(self.frame, "Room Status: {}".format(self.text), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                            (0, 255, 0), 2)
            else:
                cv2.putText(self.frame, "Room Status: {}".format(self.text), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
                            (0, 0, 255), 2)

            cv2.rectangle(self.frame, (450, 240), (1130, 632), (0, 255, 0), 10)
            cv2.rectangle(self.frame, (230, 300), (440, 740), (255, 0, 0), 10)
            cv2.rectangle(self.frame, (580, 100), (1110, 230), (255, 0, 0), 10)
            cv2.rectangle(self.frame, (1140, 200), (1300, 600), (255, 0, 0), 10)
            cv2.rectangle(self.frame, (400, 900), (1550, 1080), (0, 255, 0), 10)
            for c in self.contours:
                cv2.drawContours(self.frame, c, -1, (0, 255, 0), 6)

            # height, width, _ = self.frame.shape
            frame_change = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            # frame_resize = cv2.resize(frame_change, (40, 200), interpolation=cv2.INTER_AREA) # 381, 221
            image = QImage(frame_change.data, frame_change.shape[1], frame_change.shape[0],
                                 QImage.Format_RGB888)
            self.videoLabel.setScaledContents(True)                                                       #.scaled(self.imgLabel.width(), self.imgLabel.height())  # 处理成QImage
            self.videoLabel.setPixmap(QPixmap.fromImage(image))


    #加载图片数据
    def loadimg(self, dir):
        List = []
        length = sum([len(x) for _, _, x in os.walk(dir)])
        for i in range(0, length):
            img = cv2.imread(dir + '/imgX' + str(i) + '.png')
            gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            dct1 = cv2.dct(np.float32(gray1))
            dct1_roi = dct1[0:8, 0:8]
            hash1 = self.getHash(dct1_roi)
            List.append(hash1)
        ndarray = np.array(List)
        return ndarray

    def loadroiimg(self, dir):
        List = []
        length = sum([len(x) for _, _, x in os.walk(dir)])
        for i in range(0, length):
            img = cv2.imread(dir + '/imgX' + str(i) + '.png')
            gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            hash1 = self.getHash(gray1)
            List.append(hash1)
        ndarray = np.array(List)
        return ndarray

    def imgProcess(self, frame, loc, size, ndarray, K):

        G = np.empty(shape=[0, ])
        frame = frame[loc[0]:loc[1], loc[2]:loc[3]]
        frame = cv2.GaussianBlur(frame, size, 0)
        # if K == 10:
        #     frame = self.gamma_trans(frame, 0.45)
        #     frame = cv2.resize(frame, (32, 32))
        # else:
        frame = self.gamma_trans(frame, 0.75)
        frame = cv2.resize(frame, (8, 8))

        framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # if K == 10:
        # dct2 = cv2.dct(np.float32(framegray))
        # dct2_roi = dct2[0:8, 0:8]
        # hash2 = self.getHash(dct2_roi)
        # else:
        hash2 = self.getHash(framegray)
        for i in ndarray:
            degree = self.classify_pHash(i, hash2)
            if degree <= K:
                return degree
            G = np.append(G, degree)

        return min(G)

    def detect_person(self, Xleft, Xright, Xmiddle):

        # print('Xleft:', Xleft, 'Xright:', Xright, 'Xmiddle:', Xmiddle, 'res1:', self.res1, 'res2:', self.res2)

        if Xleft > 11:
            self.textBrowser.append('左边有人！')
            return True
            # print('minleft:', minleft, 'minright:', minright, 'minmiddle:', minmiddle, 'minentire:', minentire)
        elif Xright > 14:
            self.textBrowser.append('右边有人！')
            return True
        elif Xmiddle > 15:
            self.textBrowser.append('中间有人！')
            return True
        # elif Xentire > 10:
        #     self.textBrowser.append('机器身边有人！')
        #     return True
        elif self.res1:
            self.textBrowser.append('右上角有人！')
            self.background = None
            return True
        # elif self.res2:
        #     self.textBrowser.append('下面有人！')
        #     return True
        # else:
        #     pass

        return False

    # 平均哈希算法计算
    def classify_aHash(self, hash1, hash2):
        return self.Hamming_distance(hash1, hash2)

    def classify_pHash(self, hash1, hash2):
        return self.Hamming_distance(hash1, hash2)

    # 输入灰度图，返回hash
    def getHash(self, image):
        average = np.mean(image)
        hash = []
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if image[i, j] > average:
                    hash.append(1)
                else:
                    hash.append(0)
        return hash

    # 计算汉明距离
    def Hamming_distance(self, hash1, hash2):
        num = 0
        for index in range(len(hash1)):
            if hash1[index] != hash2[index]:
                num += 1
        return num

    def gamma_trans(self, img, gamma):
        '''
        将图像光照归一化
        :param img:
        :param gamma:
        :return:
        '''
        # 具体做法先归一化到1，然后gamma作为指数值求出新的像素值再还原
        gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
        # 实现映射用的是Opencv的查表函数
        return cv2.LUT(img, gamma_table)

    def loadRoiImage(self, dir):
        List = []
        read_file = open(dir, 'rb')
        faces = pickle.load(read_file)
        read_file.close()
        for i in range(0, faces.shape[0]):
            gray1 = cv2.cvtColor(faces[i], cv2.COLOR_BGR2GRAY)
            hash1 = self.getHash(gray1)
            List.append(hash1)
        ndarray = np.array(List)
        return ndarray

    def loadImg(self, dir):
        List = []
        read_file = open(dir, 'rb')
        faces = pickle.load(read_file)
        read_file.close()
        for i in range(0, faces.shape[0]):
            gray1 = cv2.cvtColor(faces[i], cv2.COLOR_BGR2GRAY)
            dct1 = cv2.dct(np.float32(gray1))
            dct1_roi = dct1[0:8, 0:8]
            hash1 = self.getHash(dct1_roi)
            List.append(hash1)
        ndarray = np.array(List)
        return ndarray

    def diff_one(self, frame, background, threshold):

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
        # gray_frame_roi=gray_frame[a:b,i:j]

        diff = cv2.absdiff(background, gray_frame)
        diff = cv2.threshold(diff, 180, 255, cv2.THRESH_BINARY)[1]
        diff = cv2.dilate(diff, self.es, iterations=2)
        diff_sum = np.sum(diff)

        # return diff_sum
        # return diff
        if diff_sum >= threshold:
            print(diff_sum)
            return True

        else:
            return False

    def diff_two(self, frame, background, threshold):

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
        # gray_frame_roi=gray_frame[a:b,i:j]

        diff = cv2.absdiff(background, gray_frame)
        diff = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY)[1]
        diff = cv2.dilate(diff, self.es, iterations=2)
        diff_sum = np.sum(diff)

        # return diff_sum
        # return diff

        if diff_sum >= threshold:
            print(diff_sum)
            return True

        else:
            return False

    def frameDelta(self):
        if self.frame is not None:
            if self.background is not None:
                # self.back = self.background[420:612, 470:570]
                # self.back = cv2.cvtColor(self.back, cv2.COLOR_BGR2GRAY)
                # self.back = cv2.GaussianBlur(self.back, (21, 21), 0)
                self.background = cv2.bitwise_and(self.background, self.mask1)
                self.background = cv2.cvtColor(self.background, cv2.COLOR_BGR2GRAY)
                self.background = cv2.GaussianBlur(self.background, (21, 21), 0)
                frame1 = cv2.bitwise_and(self.frame, self.mask1)
                self.res1 = self.diff_one(frame1, self.background, self.threshold_1)
                # if self.res1 and self.isStopFlag is False:
                #     self.stop_machine()
                #     self.textBrowser.append('右上角有人！')
                #     self.save_img(self.frame)
                #     # self.thread_video_diff.pause()
                # else:
                #     self.text = 'No Person!!!'
                # self.res2 = self.diff_two(frame[900:1080, 400:1550], self.back, self.threshold_2)

            self.background = self.frame


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = XiaoAll()
    app.setQuitOnLastWindowClosed(True)
    qssStyle = '''
            
            QMainWindow {
                background-color: black
            }
            
            QTextBrowser {
                background-color: #D3D3D3;
                color: red;
            }
            
            QLabel{
                color:red;
            }
            '''
    main_app.setStyleSheet(qssStyle)
    main_app.show()
    sys.exit(app.exec_())
