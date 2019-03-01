import cv2
import os
import numpy as np

def classify_aHash(image1,image2):
    image1 = cv2.GaussianBlur(image1, (3, 3), 0)
    image1 = gamma_trans(image1, 0.75)
    image1 = cv2.resize(image1, (8, 8))
    image2 = cv2.GaussianBlur(image2, (3, 3), 0)
    image2 = gamma_trans(image2, 0.75)
    image2 = cv2.resize(image2, (8, 8))
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    hash1 = getHash(gray1)
    hash2 = getHash(gray2)
    return Hamming_distance(hash1,hash2)

def classify_pHash(image1, image2):
    # l = cv2.resize(image1, (32, 32))
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    dct1 = cv2.dct(np.float32(gray1))
    dct1_roi = dct1[0:8, 0:8]
    # l2 = cv2.resize(image2, (32, 32))
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    dct2 = cv2.dct(np.float32(gray2))
    dct2_roi = dct2[0:8, 0:8]
    hash1 = getHash(dct1_roi)
    hash2 = getHash(dct2_roi)
    return Hamming_distance(hash1,hash2)

# 输入灰度图，返回hash
def getHash(image):
    average = np.mean(image)
    hash = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i,j] > average:
                hash.append(1)
            else:
                hash.append(0)
    return hash

# 计算汉明距离
def Hamming_distance(hash1,hash2):
    num = 0
    for index in range(len(hash1)):
        if hash1[index] != hash2[index]:
            num += 1
    return num

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

if __name__ == '__main__':

    list = []
    a = {}
    path = "middle"
    for i in os.walk(path):
        list.append(i)

    print(len(list[0][2]))

    for i, j in enumerate(list[0][2]):

        a[i] = j
        print(i, j)



    for i in range(0, len(list[0][2])):

        if os.path.exists('middle/' + str(a[i])):
            img1 = cv2.imread('middle/' + str(a[i]))
            img1 = img1[310:400, 550:650]
        else:
            continue
        for j in range(i + 1, len(list[0][2])-1):

            if os.path.exists('middle/' + str(a[j])):
                img2 = cv2.imread('middle/' + str(a[j]))
                img2 = img2[310:400, 550:650]
            else:
                continue
            degree = classify_aHash(img1, img2)
            if degree <= 1:
                 os.remove('middle/' + str(a[j]))
                 print(i, j)