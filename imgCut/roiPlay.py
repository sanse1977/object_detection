import cv2
import numpy as np

cap = cv2.VideoCapture('../yjc/1.mp4')
mask = cv2.imread('../imgCut/2.jpg')
ret, frame = cap.read()


while ret is True:
    frame = cv2.bitwise_and(frame, mask)
    frame=cv2.resize(frame,(1280,720))
    cv2.imshow("111", frame)
    ret, frame = cap.read()
    cv2.waitKey(25)

