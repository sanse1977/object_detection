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

def roi_cut(image, i, loc=(900, 1080, 0, 1550)): # 0, 900), (1550, 1080
    '''
    截取一个矩形兴趣区域
    :param filepath:
    :param loc:
    :return:
    '''
    l = image[loc[0]:loc[1], loc[2]:loc[3]]
    l = cv2.GaussianBlur(l, (3, 3), 0)
    l1 = gamma_trans(l, 0.75)
    l = cv2.resize(l1, (8, 8))
    # cv2.imwrite('imgX/imgX' + str(i) + '.png', l)
    # gray = cv2.cvtColor(l, cv2.COLOR_BGR2GRAY)
    # dct = cv2.dct(np.float32(gray))
    # dct_roi = dct[0:8, 0:8]
    # print('type:', type(dct_roi))
    cv2.imwrite('roiImg/bottom/imgX' + str(i) + '.png', l)
    cv2.imshow('a', frame)
    cv2.waitKey(1)

# def roi_cut1(image, i, loc=(260, 340, 1010, 1110)):
#     '''
#     截取一个矩形兴趣区域
#     :param filepath:
#     :param loc:
#     :return:
#     '''
#     l = image[loc[0]:loc[1], loc[2]:loc[3]]
#     l = cv2.GaussianBlur(l, (3, 3), 0)
#     l1 = gamma_trans(l, 0.75)
#     l = cv2.resize(l1, (8, 8))
#     # cv2.imwrite('imgX/imgX' + str(i) + '.png', l)
#     # gray = cv2.cvtColor(l, cv2.COLOR_BGR2GRAY)
#     # dct = cv2.dct(np.float32(gray))
#     # dct_roi = dct[0:8, 0:8]
#     # print('type:', type(dct_roi))
#     cv2.imwrite('roiImg/rightImg/imgX' + str(i) + '.png', l)
#     # cv2.imshow('a', l1)
#     cv2.waitKey(1)

if __name__ == '__main__':

    i = 2
    cap = cv2.VideoCapture('testvideo/mixVideo.avi')
    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False

    while ret:
        #cv2.rectangle(frame, (550, 310), (650, 400), (255, 0, 255), 3)
        if i == 2:
            roi_cut(frame, i)
        # roi_cut1(frame, i)
        # cv2.imshow('frame', frame)
        # img1 = gamma_trans(frame, 1)
        # cv2.imshow('img1', img1)
        # cv2.waitKey(1)
        i += 1
        ret, frame = cap.read()