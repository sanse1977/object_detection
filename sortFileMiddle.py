import os
import cv2
import numpy as np

def gamma_trans(img, gamma):
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

list = []
path="middle"
for i in os.walk(path):
    list.append(i)

print(len(list[0][2]))

for i, j in enumerate(list[0][2], start = 660):
    img = cv2.imread('middle/' + j)
    frameright = img[310:400, 550:650]
    frameright = cv2.GaussianBlur(frameright, (3, 3), 0)
    frameright = gamma_trans(frameright, 0.75)
    frameright = cv2.resize(frameright, (8, 8))
    cv2.imwrite('E:/detectPerson/roiImg/middleImg/img' + str(i) + '.png', frameright)
    print(i, j)