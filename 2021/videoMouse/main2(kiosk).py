import cv2
import mediapipe as mp
import pynput
import pyrealsense2 as rs
import numpy as np
from multiprocessing import Process, Queue
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
import pyautogui
import time


cantclick = False

global valid
valid = [0, 0, 0, 0, 0]

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

mouse_drag = pynput.mouse.Controller()
mouse_button = pynput.mouse.Button
Controller = pynput.keyboard.Controller()

global first
first = 1

global hangul
hangul = 1

modqueue = Queue()
pqueue = Queue()
pointmodqueue = Queue()
pointpqueue = Queue()
valiqueue = Queue()
gqueue = Queue()


class finger():

    def __init__(self, landmark_Right, i, aligned_depth_frame, pqueue, pointpqueue):

        i = (4 * i + 1)
        if landmark_Right.landmark[i + 3].x > 0 and landmark_Right.landmark[i + 3].x < 1 and landmark_Right.landmark[
            i + 3].y > 0 and landmark_Right.landmark[i + 3].y < 1:
            self.topxy = (int(640 * landmark_Right.landmark[i + 3].x), int(480 * landmark_Right.landmark[i + 3].y))
        if landmark_Right.landmark[i + 2].x > 0 and landmark_Right.landmark[i + 2].x < 1 and landmark_Right.landmark[
            i + 2].y > 0 and \
                landmark_Right.landmark[i + 2].y < 1:
            self.second = (int(640 * landmark_Right.landmark[i + 2].x), int(480 * landmark_Right.landmark[i + 2].y))
        if landmark_Right.landmark[i + 1].x > 0 and landmark_Right.landmark[i + 1].x < 1 and landmark_Right.landmark[
            i + 1].y > 0 and \
                landmark_Right.landmark[i + 1].y < 1:
            self.third = (int(640 * landmark_Right.landmark[i + 1].x), int(480 * landmark_Right.landmark[i + 1].y))
        if landmark_Right.landmark[i].x > 0 and landmark_Right.landmark[i].x < 1 and landmark_Right.landmark[
            i].y > 0 and \
                landmark_Right.landmark[i].y < 1:
            self.forth = (int(640 * landmark_Right.landmark[i].x), int(480 * landmark_Right.landmark[i].y))

        self.topdist = self.checkdist(self.topxy, aligned_depth_frame)
        self.forthdist = self.checkdist(self.forth, aligned_depth_frame)

        self.topbeforxy = (0, 0)

        self.topbefordist = [0, 0, 0, 0]
        self.forthbefordist = [0, 0, 0, 0]

        self.up = 1
        self.keyisdown = False
        self.beforekeysyate = False
        self.click = 0
        self.keyboardmode = 0
        self.pqueue = pqueue
        self.pointpqueue = pointpqueue
        self.a=0

    def checkdist(self, xy, aligned_depth_frame):
        dist = aligned_depth_frame.get_distance(xy[0], xy[1])
        return dist

    def checkvalid(self):
        if (self.topxy[1] - self.forth[1]) > 0:
            self.up = 0
        else:
            self.up = 1

    def Keydown(self):
        if not (self.topbefordist[3] == 0 or self.topbefordist[0] == 0 or self.forthbefordist[3] == 0 or
                self.forthbefordist[0] == 0):
            self.beforekeysyate = self.keyisdown
            if (
                    abs(self.forthbefordist[1] - self.forthbefordist[3]) < 0.005) & (
                    -self.topxy[1] + self.second[1] <= 0) & (self.keyisdown == False):
                self.keyisdown = True




    def Keyup(self):
        if not (self.topbefordist[3] == 0 or self.topbefordist[0] == 0 or self.forthbefordist[3] == 0 or
                self.forthbefordist[0] == 0):

            if (
                    abs(self.forthbefordist[0] - self.forthbefordist[3]) < 0.005) & (
                    -self.topxy[1] + self.second[1] > 0) & (self.keyisdown == True):
                self.keyisdown = False




    def refresh(self, landmark_Right, aligned_depth_frame, i):
        i = (4 * i + 1)

        self.topbeforxy = (self.topxy[0], self.topxy[1])

        if landmark_Right.landmark[i + 3].x > 0 and landmark_Right.landmark[i + 3].x < 1 and landmark_Right.landmark[
            i + 3].y > 0 and landmark_Right.landmark[i + 3].y < 1:
            self.topxy = (int(640 * landmark_Right.landmark[i + 3].x), int(480 * landmark_Right.landmark[i + 3].y))
        if landmark_Right.landmark[i + 2].x > 0 and landmark_Right.landmark[i + 2].x < 1 and landmark_Right.landmark[
            i + 2].y > 0 and \
                landmark_Right.landmark[i + 2].y < 1:
            self.second = (int(640 * landmark_Right.landmark[i + 2].x), int(480 * landmark_Right.landmark[i + 2].y))
        if landmark_Right.landmark[i + 1].x > 0 and landmark_Right.landmark[i + 1].x < 1 and landmark_Right.landmark[
            i + 1].y > 0 and \
                landmark_Right.landmark[i + 1].y < 1:
            self.third = (int(640 * landmark_Right.landmark[i + 1].x), int(480 * landmark_Right.landmark[i + 1].y))
        if landmark_Right.landmark[i].x > 0 and landmark_Right.landmark[i].x < 1 and landmark_Right.landmark[
            i].y > 0 and \
                landmark_Right.landmark[i].y < 1:
            self.forth = (int(640 * landmark_Right.landmark[i].x), int(480 * landmark_Right.landmark[i].y))

        distt = aligned_depth_frame.get_distance(self.topxy[0], self.topxy[1])
        self.topbefordist[0] = self.topbefordist[1]
        self.topbefordist[1] = self.topbefordist[2]
        self.topbefordist[2] = self.topbefordist[3]
        self.topbefordist[3] = distt

        distf = aligned_depth_frame.get_distance(self.forth[0], self.forth[1])
        self.forthbefordist[0] = self.forthbefordist[1]
        self.forthbefordist[1] = self.forthbefordist[2]
        self.forthbefordist[2] = self.forthbefordist[3]
        self.forthbefordist[3] = distf

        self.checkvalid()
        if self.keyboardmode==1 and valid!= [1, 1, 1, 0, 0]:
            self.Keydown()
            self.Keyup()


class umjifinger(finger):

    def checkvalid(self):
        if (self.topxy[0] - self.third[0]) < 0:
            self.up = 0
        else:
            self.up = 1


def movemouse(finger):
    fingerx = finger.topxy[0]
    fingery = finger.topxy[1]

    default = mouse_drag.position
    positionX = default[0]
    positionY = default[1]

    if (first == 0):
        if ((abs(fingerx - finger.topbeforxy[0]) > 1) or (abs(fingery - finger.topbeforxy[1]) > 1)):
            a = - 2 * (1920 / 640) * (fingerx - finger.topbeforxy[0])
            b = 2 * (1080 / 480) * (fingery - finger.topbeforxy[1])

            if a > 0:
                a = a - 9
                if a < 0:
                    a = 0
            elif a < 0:
                a = a + 9
                if a > 0:
                    a = 0
            if a>=3 and a<=9:
                a=a/1.5
            if b > 0:
                b = b - 9
                if b < 0:
                    b = 0
            elif b < 0:
                b = b + 9
                if b > 0:
                    b = 0
            if b>=4.5 and b<=9:
                b=b/2.25

            if (positionX + a <= 1919) & (positionX + a >= 1) & (positionY + b <= 1079) & (positionY + b >= 1):
                mouse_drag.position = (positionX + a, positionY + b)

            else:
                if positionX + a > 1919:
                    positionX = 1919
                    a = 0
                elif positionX + a < 1:
                    positionX = 1
                    a = 0

                elif positionY + b > 1079:
                    positionY = 1079
                    b = 0
                elif positionY + b < 1:
                    positionY = 1
                    b = 0
                mouse_drag.position = (positionX + a, positionY + b)


def clickLmouse(gumji):
    gumji.Keydown()
    gumji.Keyup()
    if ((gumji.keyisdown == True) & (gumji.click == 0)):
        mouse_drag.press(mouse_button.left)
        default = mouse_drag.position
        gumji.click = 1
        return default
    if ((gumji.keyisdown == False) & (gumji.click == 1)):
        mouse_drag.release(mouse_button.left)
        gumji.click = 0

def showvideo(modqueue, pqueue, pointpqueue, valiqueue, gqueue):
    global prex
    global prey
    global m
    global valid
    global depthfinger
    global first

    for i in menustickers1 :
        i.show()
    category1.show()
    category2.show()
    basket.show()
    holdpoint = 0
    hold = 0
    fivefinger = 0
    reverse = 0
    onetime = 0
    keyboardmodpoint = 1
    keyboardmod = 0
    pipeline = rs.pipeline()  # 이미지 가져옴
    config = rs.config()  # 설정 파일 생성
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16,
                         30)  # 1280, 720, rs.format.z16, 30)  # 크기 , 포맷, 프레임 설정
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # 1280, 720, rs.format.bgr8, 30)

    profile = pipeline.start(config)  # 설정을 적용하여 이미지 취득 시작, 프로파일 얻음

    depth_sensor = profile.get_device().first_depth_sensor()  # 깊이 센서를 얻음
    depth_scale = depth_sensor.get_depth_scale()  # 깊이 센서의 깊이 스케일 얻음

    align_to = rs.stream.color  # depth 이미지를 맞추기 위한 이미지, 컬러 이미지
    align = rs.align(align_to)  # depth 이미지와 맞추기 위해 align 생성
    quitt = Quitbutton('', xy=[20, 20], modqueue=modqueue, pointpqueue=pointpqueue, on_top=True,
                       num1='quit', stickers=stickers, pointstickers=pointstickers)
    f = 1
    with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while True:

            frames = pipeline.wait_for_frames()  # color와 depth의 프레임셋을 기다림

            aligned_frames = align.process(frames)  # 모든(depth 포함) 프레임을 컬러 프레임에 맞추어 반환

            aligned_depth_frame = aligned_frames.get_depth_frame()  # aligned depth 프레임은 640x480 의 depth 이미지이다

            color_frame = aligned_frames.get_color_frame()  # 컬러 프레임을 얻음

            if not aligned_depth_frame or not color_frame:  # 프레임이 없으면, 건너 뜀'
                continue

            depth_image = np.asanyarray(aligned_depth_frame.get_data())  # depth이미지를 배열로,
            color_image = np.asanyarray(color_frame.get_data())  # color 이미지를 배열로
            frame = color_image
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            hsvim = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)
            lower = np.array([50, 75, 130], dtype="uint8")
            upper = np.array([120, 255, 255], dtype="uint8")
            skinRegionHSV = cv2.inRange(hsvim, lower, upper)
            #blurred = cv2.blur(skinRegionHSV, (3, 3))
            ret, thresh = cv2.threshold(skinRegionHSV, 0, 255, cv2.THRESH_BINARY)

            thresh = thresh / 255

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #cv2.imshow('sssSSS', skinRegionHSV)
            #cv2.imshow('sssSSsS', hsvim)
            image1 = image
            image[0:480, 0:640, 0] = image[0:480, 0:640, 0] * thresh
            image[0:480, 0:640, 1] = image[0:480, 0:640, 1] * thresh
            image[0:480, 0:640, 2] = image[0:480, 0:640, 2] * thresh

            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                if first == 1:
                    umji = umjifinger(results.multi_hand_landmarks[0], 0, aligned_depth_frame, pqueue, pointpqueue)
                    gumji = finger(results.multi_hand_landmarks[0], 1, aligned_depth_frame, pqueue, pointpqueue)
                    chongji = finger(results.multi_hand_landmarks[0], 2, aligned_depth_frame, pqueue, pointpqueue)
                    yakji = finger(results.multi_hand_landmarks[0], 3, aligned_depth_frame, pqueue, pointpqueue)
                    saekki = finger(results.multi_hand_landmarks[0], 4, aligned_depth_frame, pqueue, pointpqueue)
                    fingerlist = [umji, gumji, chongji, yakji, saekki]
                    first = 0
                if modqueue.qsize() > 0:
                    keyboardmod = modqueue.get()
                    for fin in fingerlist:
                        fin.keyboardmode = keyboardmod
                if first == 0:
                    for r in range(5):
                        if len(results.multi_hand_landmarks) == 1:
                            fingerlist[r].refresh(results.multi_hand_landmarks[0], aligned_depth_frame, r)
                        if len(results.multi_hand_landmarks) == 2:
                            fingerlist[r].refresh(results.multi_hand_landmarks[1], aligned_depth_frame, r)

                if umji.topxy[0] < saekki.topxy[0]:
                    state = 'Left'
                else:
                    state = 'Right'
                if state == 'Left':
                    if umji.up == 1:
                        umji.up = 0
                    elif umji.up == 0:
                        umji.up = 1
                valid = [umji.up, gumji.up, chongji.up, yakji.up, saekki.up]
                quitt.valid=valid

                valiqueue.put(valid)
                category1.valid=valid
                category1.menumod

                if state == 'Right':
                    if umji.topxy[0] < saekki.topxy[0]:
                        reverse = 1
                    else:
                        reverse = 0
                elif state == 'Left':
                    if umji.topxy[0] > saekki.topxy[0]:
                        reverse = 1
                    else:
                        reverse = 0
                if valid == [1, 1, 1, 0, 0] and reverse == 0:
                    movemouse(umji)
                    clickLmouse(gumji)









            frame = cv2.flip(frame, 1)

            f = f + 1
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cv2.destroyAllWindows()
        pipeline.stop()  # 리얼센스 데이터 스트리밍 중지



text2=[['아이스크림', '   '], ['사과', '  '], ['햄버거 ', '   '],['밥 ', '   '], ['콜라 ', '  '], ['사이다 ', '   ']]
menustickers1=[]
menustickers2=[]

menustore=[]
stickers = []
pointstickers = []

count = 0

class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, usecase, size=0.6, on_top=False, num1=0, stickers=[], pointstickers=[],pixmap = None):
        super(Sticker, self).__init__()
        self.timer = QtCore.QTimer(self)
        self.img_path = img_path
        self.xy = xy
        self.to_xy = xy
        self.size = size
        self.direction = [0, 0]  # x: 0(left), 1(right), y: 0(up), 1(down)
        self.setWindowOpacity(1)
        self.on_top = on_top
        self.localPos = None
        self.num1 = num1
        self.menusequence = 0
        self.type = None
        self.firstnum = None
        self.secondnum = None
        self.thirdnum = None
        self.first = 1
        self.pixmap = pixmap
        self.setupUi()
        self.usecase = usecase
        self.count = 0
        # self.show()
        self.type = self.num1[0]
        self.firstnum = self.num1[1]
        self.keyboardpoint = 1
        self.stickers =stickers
        self._menumod=0
        self.valid=[0,0,0,0,0]
        if num1[0] != 'c':
            label1 = QLabel(self.firstnum, self)
        elif num1[0] == 'c':
            label1 = QLabel(self.firstnum.upper(), self)
        label1.move(10, 5)
        font1 = label1.font()
        font1.setPointSize(12)
        font1.setBold(True)
        label1.setFont(font1)

        if len(num1) > 2:
            self.secondnum = self.num1[2]
            label2 = QLabel(self.secondnum, self)
            label2.move(50, 5)
            font2 = label2.font()
            font2.setPointSize(12)
            font2.setBold(True)
            label2.setFont(font2)
        if len(num1) > 3:
            self.thirdnum = self.num1[3]
            label3 = QLabel(self.thirdnum, self)
            label3.move(10, 35)
            font3 = label3.font()
            font3.setPointSize(12)

            font3.setBold(True)
            label3.setFont(font3)



    def setupUi(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)
        flags = QtCore.Qt.WindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint if self.on_top else QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        label = QtWidgets.QLabel(centralWidget)
        movie = QMovie(self.img_path)
        label.setMovie(movie)
        movie.start()
        movie.stop()
        w = int(movie.frameRect().size().width() * self.size)
        self.w = w
        h = int(movie.frameRect().size().height() * self.size)
        self.h = h
        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()
        self.label_damage = QtWidgets.QLabel(label)
        self.a = 0
        if self.pixmap != None:
            print(self.pixmap)
            self.pixmap = QtGui.QPixmap(self.pixmap).scaled(w, h)
            self.label_damage.setPixmap(self.pixmap)
            self.label_damage.hide()

        self.setGeometry(self.xy[0], self.xy[1], w, h)


    def mousePressEvent(self, e):
        if self.usecase == 'category1':
            for i in menustickers2:
                i.hide()
            for j in menustickers1:
                j.show()
        elif self.usecase == 'category2':
            for i in menustickers1:
                i.hide()
            for j in menustickers2:
                j.show()

        if self.usecase == 'menu' :
            self.count = len(menustore)/2
            menustore.append(Sticker('order.png', xy=[123, 785 + 60 * self.count],usecase= 'order',on_top=True, num1=['s',self.num1[0]],stickers=[], pointstickers=[]))
            menustore.append(Sticker('close.png', xy=[775, 785 + 60 * self.count],usecase='close', on_top=True, num1='   ', stickers=[],pointstickers=[]))
            for i in menustore[len(menustore) - 2:len(menustore)]:
                i.show()
            self.label_damage.show()


        if self.usecase == 'close':
            length = len(menustore)
            for p in range(length):
                if menustore[p].xy[1] == self.xy[1]:
                    i=p
                    if length >2:
                        while i+2 < length:
                            xy = menustore[i].xy
                            menustore[i+2].move(*xy)
                            i+=1

                        i += 1

                        while i-2 >= p :
                            xy = menustore[i-2].xy
                            menustore[i].xy=xy
                            i-=1

                    del menustore[p+1]
                    del menustore[p]
                    break
    def mouseReleaseEvent(self, e) :
        self.label_damage.hide()
    @property
    def menumod(self):
        if self.valid == [1,0,0,0,0]:
            for i in menustickers2:
                i.hide()
            for j in menustickers1:
                j.show()
        elif self.valid == [0,0,0,0,1]:
            for i in menustickers1:
                i.hide()
            for j in menustickers2:
                j.show()
    @menumod.setter
    def menumod(self, new_menumod):
            self._menumod = new_menumod



class Quitbutton(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, modqueue, pointpqueue, size=0.6, on_top=False, num1=0, stickers=[],
                 pointstickers=[]):
        super(Quitbutton, self).__init__()
        self.valid=[0,0,0,0,0]
        self.count=0
        self.timer = QtCore.QTimer(self)
        self.img_path = img_path
        self.setWindowOpacity(0.3)
        self.xy = xy
        self.orderx=0
        self.ordery=0
        self.menusequence=0
        self.to_xy = xy
        self.size = size
        self.on_top = on_top
        self.localPos = None
        self.num1 = num1
        self.check=0
        # self.setWindowOpacity(0.3) 반투명
        self.setupUi()
        self.show()
        self.vanish = 1
        self.menuvanish=1
        self.modqueue = modqueue
        self.pointpqueue = pointpqueue
        self._menuorder=0
        self._mod = 0
        self._menumod=0
        self.imshow = 0
        label1 = QLabel(num1, self)
        label1.move(10, 5)
        font1 = label1.font()
        font1.setPointSize(9)
        font1.setBold(True)
        label1.setFont(font1)

    def setupUi(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)
        flags = QtCore.Qt.WindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint if self.on_top else QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        label = QtWidgets.QLabel(centralWidget)
        movie = QMovie(self.img_path)
        label.setMovie(movie)
        movie.start()
        movie.stop()
        w = int(movie.frameRect().size().width() * self.size)
        self.w = w
        h = int(movie.frameRect().size().height() * self.size)
        self.h = h
        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()
        self.setGeometry(self.xy[0], self.xy[1], w, h)


app = QtWidgets.QApplication(sys.argv)



# 4줄

menustickers1.append(Sticker('ice.png', xy=[100,300], usecase = 'menu', on_top=True, num1=text2[0], stickers=[], pointstickers=[],pixmap='ice2.png'))
menustickers1.append(Sticker('abc.png', xy=[500,300], usecase = 'menu', on_top=True, num1=text2[1], stickers=[], pointstickers=[],pixmap='abc2.png'))
menustickers1.append(Sticker('ham.png', xy=[900,300],usecase = 'menu', on_top=True, num1=text2[2], stickers=[], pointstickers=[],pixmap='ham2.png'))
menustickers2.append(Sticker('rice.png', xy=[100,300], usecase = 'menu',on_top=True, num1=text2[3], stickers=[], pointstickers=[],pixmap='rice2.png'))
menustickers2.append(Sticker('coke.png', xy=[500,300], usecase = 'menu', on_top=True, num1=text2[4], stickers=[], pointstickers=[],pixmap='coke2.png'))
menustickers2.append(Sticker('cider.png', xy=[900,300], usecase = 'menu', on_top=True, num1=text2[5], stickers=[], pointstickers=[],pixmap='cider2.png'))
basket =Sticker('basket.png', xy=[100,700], usecase = 'basket',on_top=True, num1='   ', stickers=[], pointstickers=[])
category1 = Sticker('menu.png', xy=[400,120], usecase = 'category1', on_top=True, num1='   ', stickers=menustickers1, pointstickers=[])
category2 = Sticker('beverage.png', xy=[700,120], usecase = 'category2', on_top=True, num1='   ', stickers=menustickers2, pointstickers=[])
background = Sticker('background.png', xy=[80,0], usecase = '    ', on_top=False, num1='   ', stickers=[], pointstickers=[])
programe = Sticker('programe.png', xy=[80,0], usecase = '    ', on_top=True, num1='   ', stickers=[], pointstickers=[])
background.show()
programe.show()
if __name__ == '__main__':
    p1 = Process(target=showvideo, args=(modqueue, pqueue, pointpqueue, valiqueue, gqueue,))
    # p2 = Process(target=main)
    p1.start()
    # p2.start()

    app.exec_()
    p1.join()
    # p2.join()