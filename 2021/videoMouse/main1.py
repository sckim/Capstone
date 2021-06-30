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
from pynput import keyboard
import time
keyboardmod = 0

Lbeforedepth = []
Lbeforecdepth = []
Rbeforedepth = []
Rbeforecdepth = []

cantclick = False

global valid
global gaesoo
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
                print("click")



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
            a = - 3 * (1920 / 640) * (fingerx - finger.topbeforxy[0])
            b = 3 * (1080 / 480) * (fingery - finger.topbeforxy[1])
            a=int(a)
            b=int(b)
            if a > 0:
                a = a - 13
                if a < 0:
                    a = 0
            elif a < 0:
                a = a + 13
                if a > 0:
                    a = 0
            if abs(a)>=3 and abs(a)<=32:
                a=int(a/3)
            if b > 0:
                b = b - 13
                if b < 0:
                    b = 0
            elif b < 0:
                b = b + 13
                if b > 0:
                    b = 0
            if abs(b)>=7.25 and abs(b)<=20.75:
                b=int(b/3)
            if (positionX + a <= 1919) & (positionX + a >= 1) & (positionY + b <= 1079) & (positionY + b >= 1):
                mouse_drag.position = (positionX + a, positionY + b)

            else:
                if positionX + a > 1920:
                    positionX = 1920
                    a = 0
                elif positionX + a < 0:
                    positionX = 0
                    a = 0

                elif positionY + b > 1080:
                    positionY = 1080
                    b = 0
                elif positionY + b < 0:
                    positionY = 0
                    b = 0
                mouse_drag.position = (positionX + a, positionY + b)

def clickLmouse(gumji):
    gumji.Keydown()
    gumji.Keyup()
    if ((gumji.keyisdown == True) & (gumji.click == 0)):
        mouse_drag.press(mouse_button.left)
        gumji.click = 1
    if ((gumji.keyisdown == False) & (gumji.click == 1)):
        mouse_drag.release(mouse_button.left)
        gumji.click = 0


def clickRmouse(chongji):
    chongji.Keydown()
    chongji.Keyup()
global chonghab
global gaesoo

def showvideo(modqueue, pqueue, pointpqueue, valiqueue, gqueue):
    global prex
    global prey
    global m
    global valid
    global depthfinger
    global first
    global gaesoo
    holdpoint = 0
    hold = 0
    chonghab = 0
    gaesoo = 0
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
    quitt = Quitbutton('U', xy=[20, 20], modqueue=modqueue, pointpqueue=pointpqueue, on_top=True,
                       num1='quit', stickers=stickers, pointstickers=pointstickers)
    z1 = Sticker('point.jpg', xy=[500, 30], on_top=True, num1=text[1], stickers=[], pointstickers=[])
    pointstickers.append(z1)
    with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while True:
            cur=time.time()
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
            lower = np.array([20, 75, 130], dtype="uint8")
            upper = np.array([130, 255, 255], dtype="uint8")
            skinRegionHSV = cv2.inRange(hsvim, lower, upper)
            ret, thresh = cv2.threshold(skinRegionHSV, 0, 255, cv2.THRESH_BINARY)
            thresh = thresh / 255
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image1 = image
            image[0:480, 0:640, 0] = image[0:480, 0:640, 0] * thresh
            image[0:480, 0:640, 1] = image[0:480, 0:640, 1] * thresh
            image[0:480, 0:640, 2] = image[0:480, 0:640, 2] * thresh
            image.flags.writeable = False
            results = hands.process(image)
            # Draw the hand annotations on the image.
            image.flags.writeable = True
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
                    dd = time.time()
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
                if valid == [1, 1, 1, 1, 1]:
                    fivefinger = 1

                '''if valid == [0, 0, 0, 0, 0] and holdpoint == 0 and fivefinger == 1:
                    holdpoint += 1
                    fivefinger = 0

                if valid == [0, 0, 0, 0, 0] and holdpoint == 1 and fivefinger == 1:
                    holdpoint = 0
                    fivefinger = 0
                    if hold == 0:
                        hold = 1
                    elif hold == 1:
                        hold = 0

                if hold == 1:
                    frame = cv2.flip(frame, 1)
                    cv2.imshow('sss', frame)
                    continue'''

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

                if (chongji.topxy[0] - yakji.topxy[0] > 10):
                    if valid == [1, 1, 0, 0, 1] and onetime == 0 and reverse == 0:
                        quitt.mod
                        onetime = 1

                    elif valid != [1, 1, 0, 0, 1] and onetime == 1 and reverse == 0:

                        onetime = 0

                if umji.keyboardmode == 1:
                    if valid == [1, 1, 1, 0, 0]:
                        keyboardmodpoint = 0
                    else:
                        keyboardmodpoint = 1
                    pointstickers[0].walk(umji, keyboardmodpoint)
                if gumji.beforekeysyate == False and gumji.keyisdown == True:
                 if keyboardmod == 1 and valid != [1, 1, 1, 0, 0]:
                        umji.pqueue.put([640 - (pointstickers[0].xy[0] / 3), pointstickers[0].xy[1] * (480 / 1080)])


            frame = cv2.flip(frame, 1)
            cv2.imshow('sss', frame)

            if cv2.waitKey(5) & 0xFF == 27:
                break
        cv2.destroyAllWindows()
        pipeline.stop()  # 리얼센스 데이터 스트리밍 중지


text = [
    ['c', 'q', 'ㅃ', 'ㅂ'], ['c', 'w', 'ㅉ', 'ㅈ'], ['c', 'e', 'ㄸ', 'ㄷ'], ['c', 'r', 'ㄲ', 'ㄱ'], ['c', 't', 'ㅆ', 'ㅅ'],
    ['c', 'y', 'ㅛ'], ['c', 'u', 'ㅕ'], ['c', 'i', 'ㅑ'], ['c', 'o', 'ㅒ', 'ㅐ'], ['c', 'p', 'ㅖ', 'ㅔ'],
    ['n', '7'], ['n', '8'], ['n', '9'],

    ['c', 'a', 'ㅁ'], ['c', 's', 'ㄴ'], ['c', 'd', 'ㅇ'], ['c', 'f', 'ㄹ'], ['c', 'g', 'ㅎ'], ['c', 'h', 'ㅗ'],
    ['c', 'j', 'ㅓ'], ['c', 'k', 'ㅏ'], ['c', 'l', 'ㅣ'], ['n', '4'], ['n', '5'], ['n', '6'],

    ['c', 'z', 'ㅋ'], ['c', 'x', 'ㅌ'], ['c', 'c', 'ㅊ'], ['c', 'v', 'ㅍ'], ['c', 'b', 'ㅠ'], ['c', 'n', 'ㅜ'],
    ['c', 'm', 'ㅡ'], ['n', '1'], ['n', '2'], ['n', '3'],
    ['s', 'capslock'], ['s', 'hangul'], ['s', 'space'], ['s', 'enter'], ['n', 'backspace'], ['n', '0'], ['n', '']
]
text2=[['s', '아이스크림'], ['s', '사과'], ['s', '햄버거'],['s', '밥'], ['s', '콜라'], ['s', '사이다']]
menustickers=[]
menustore=[]
stickers = []
pointstickers = []
image=['ice2.png','apple2.png','ham2.png','rice2.png','coke2.png','cider2.png']

class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, size=0.6, on_top=False, num1=0, stickers=[], pointstickers=[]):
        super(Sticker, self).__init__()
        self.timer = QtCore.QTimer(self)
        self.img_path = img_path
        self.xy = xy
        self.xy = xy
        self.to_xy = xy
        self.size = size
        self.direction = [0, 0]  # x: 0(left), 1(right), y: 0(up), 1(down)
        self.setWindowOpacity(0.7)
        self.on_top = on_top
        self.localPos = None
        self.num1 = num1
        self.type = None
        self.firstnum = None
        self.secondnum = None
        self.thirdnum = None
        self.first = 1
        self.setupUi()
        self.a=0
        self.type = self.num1[0]
        self.firstnum = self.num1[1]
        self.keyboardpoint = 1
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

    def walk(self, finger, keyboardpoint):
        fingerx = finger.topxy[0]
        fingery = finger.topxy[1]
        self.keyboardpoint = keyboardpoint
        if (self.xy[0] <= 1920 and self.xy[0] >= 0 and self.xy[1] >= 0 and self.xy[1] <= 1080 and (
                3 * fingerx) <= 1920 and (
                3 * fingerx) >= 0 and fingery >= 0 and fingery <= 1080 and self.keyboardpoint == 1):

            if (self.first == 1):
                if (1920 - (3 * fingerx) <= 1920 and 1920 - (3 * fingerx) >= 0 and fingery >= 0 and
                        fingery <= 1080):
                    self.xy[0] = 1920 - (3 * fingerx)
                    self.xy[1] = (1080 / 480) * fingery
                    if (self.xy[0] < 1):
                        self.xy[0] = 1
                    elif self.xy[0] > 1919:
                        self.xy[0] = 1919
                    if self.xy[1] < 1:
                        self.xy[1] = 1
                    elif self.xy[1] > 1079:
                        self.xy[1] = 1079
                    self.move(*self.xy)
                    self.first = 0

        if (self.first == 0 and self.keyboardpoint == 1):

            if ((abs(fingerx - finger.topbeforxy[0]) > 1) or (abs(fingery - finger.topbeforxy[1]) > 1)):
                a = - 2* (1920 / 640) * (fingerx - finger.topbeforxy[0])
                b = 2 * (1080 / 480) * (fingery - finger.topbeforxy[1])

                if a > 0:
                    a = a - 9
                    if a < 0:
                        a = 0
                elif a < 0:
                    a = a + 9
                    if a > 0:
                        a = 0
                if b > 0:
                    b = b - 9
                    if b < 0:
                        b = 0
                elif b < 0:
                    b = b + 9
                    if b > 0:
                        b = 0
                if (self.xy[0] + a <= 1919) & (self.xy[0] + a >= 1) & (self.xy[1] + b <= 1079) & (self.xy[1] + b >= 1):
                    self.xy[0] = self.xy[0] + a
                    self.xy[1] = self.xy[1] + b
                    self.move(*self.xy)
                else:
                    if self.xy[0] + a > 1919:
                        self.xy[0] = 1919
                        a = 0
                    elif self.xy[0] + a < 1:
                        self.xy[0] = 1
                        a = 0
                    if self.xy[1] + b > 1079:
                        self.xy[1] = 1079
                        b = 0
                    elif self.xy[1] + b < 1:
                        self.xy[1] = 1
                        b = 0
                    self.xy[0] = self.xy[0] + a
                    self.xy[1] = self.xy[1] + b
                    self.move(*self.xy)



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


    @property
    def mod(self):
        if self.vanish == 0:

            h.hide()
            self.vanish = 1
            keyboardmod = 0
            self.modqueue.put(keyboardmod)
            for i in pointstickers:
                i.hide()

        elif self.vanish == 1:

            h.show()
            self.vanish = 0
            keyboardmod = 1
            self.modqueue.put(keyboardmod)
            for i in pointstickers:
                i.show()


    @mod.setter
    def mod(self, new_mod):
        self._mod = new_mod



    def mousePressEvent(self, e):
        if self.vanish == 0:
            # print('b')
            h.hide()
            self.vanish = 1
            keyboardmod = 0
            self.modqueue.put(keyboardmod)
            for i in pointstickers:
                i.hide()

        elif self.vanish == 1:
            h.show()
            self.vanish = 0
            keyboardmod = 1
            self.modqueue.put(keyboardmod)
            for i in pointstickers:
                i.show()



app = QtWidgets.QApplication(sys.argv)

# 1줄
for i in range(10):
    s = Sticker('keyboard.png', xy=[i * 85 + 450, 490], on_top=True, num1=text[i], stickers=[], pointstickers=[])
    stickers.append(s)
for i in range(3):
    s1 = Sticker('keyboard.png', xy=[i * 85 + 1400, 490], on_top=True, num1=text[i + 10], stickers=[], pointstickers=[])
    stickers.append(s1)

# 2줄
for i in range(9):
    a = Sticker('keyboard.png', xy=[i * 85 + 500, 570], on_top=True, num1=text[i + 13], stickers=[], pointstickers=[])
    stickers.append(a)
for i in range(3):
    a1 = Sticker('keyboard.png', xy=[i * 85 + 1400, 570], on_top=True, num1=text[i + 22], stickers=[], pointstickers=[])
    stickers.append(a1)

# 3줄
for i in range(7):
    b = Sticker('keyboard.png', xy=[i * 85 + 560, 650], on_top=True, num1=text[i + 25], stickers=[], pointstickers=[])
    stickers.append(b)
for i in range(3):
    b1 = Sticker('keyboard.png', xy=[i * 85 + 1400, 650], on_top=True, num1=text[i + 32], stickers=[], pointstickers=[])
    stickers.append(b1)

# 4줄
stickers.append(Sticker('keyboard.png', xy=[450, 730], on_top=True, num1=text[35], stickers=[], pointstickers=[]))
stickers.append(Sticker('keyboard.png', xy=[535, 730], on_top=True, num1=text[36], stickers=[], pointstickers=[]))
stickers.append(Sticker('rlsrj.png', xy=[620, 730], on_top=True, num1=text[37], stickers=[], pointstickers=[]))
stickers.append(Sticker('key2.png', xy=[1050, 730], on_top=True, num1=text[38], stickers=[], pointstickers=[]))
stickers.append(Sticker('keyboard.png', xy=[1225, 730], on_top=True, num1=text[39], stickers=[], pointstickers=[]))
stickers.append(Sticker('keyboard.png', xy=[1485, 730], on_top=True, num1=text[40], stickers=[], pointstickers=[]))

h = Sticker('zlqhem.png', size=1, xy=[450, 490], on_top=True, num1=text[41], stickers=[], pointstickers=[])





def imagecollision(pqueue,pointpqueue,valiqueue):

    shiftstate = 0
    while True:
        if valiqueue.qsize() > 0:
            valid = valiqueue.get()

        if pqueue.qsize() > 0:
          if valid == [1, 1, 1, 0, 0]:
              x,y=pqueue.get()
          elif valid!=[1,1,1,0,0]:
            x, y = pqueue.get()
            x = 1920 - int((1920 / 640 * x))
            y = int((1080 / 480 * y))
            if valid == [1, 1, 1, 1, 0]:
                shiftstate = 1
                print(valid)
            elif valid != [1, 1, 1, 1, 0] and shiftstate == 1:
                shiftstate =0
            for i in stickers[0:35]:

                if (x > i.xy[0]) and (x < i.xy[0] + i.w) and (y > i.xy[1]) and (y < i.xy[1] + i.h):
                    if shiftstate ==1 :
                        Controller.press(keyboard.Key.shift)
                    Controller.press(i.firstnum)
                    if shiftstate ==1 :
                        Controller.release(keyboard.Key.shift)



            for i in stickers[35:41]:

                if (x > i.xy[0]) and (x < i.xy[0] + i.w) and (y > i.xy[1]) and (y < i.xy[1] + i.h):

                    pyautogui.press(i.firstnum)
                    if i.firstnum == 'hangul':
                        print('han')




def gesture(gqueue):
    while True:
        if gqueue.qsize() > 0:
            ges = gqueue.get()
            if ges == 'on':
                quitt.mod


if __name__ == '__main__':
    p1 = Process(target=showvideo, args=(modqueue, pqueue, pointpqueue, valiqueue, gqueue,))
    p3 = Process(target=imagecollision, args=(pqueue, pointpqueue, valiqueue,))
    p4 = Process(target=gesture, args=(gqueue,))
    p1.start()
    p3.start()
    p4.start()

    app.exec_()
    p1.join()
    p3.join()
    p4.join