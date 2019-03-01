import cv2
import pickle
import numpy as np
import os

class DictSave(object):
    def __init__(self,filenames):
        self.filenames = filenames
        self.arr = []
        self.all_arr = []

    def image_input(self, filenames):
        for filename in filenames:
            self.arr = self.read_file(filename)
            if self.all_arr == []:
                self.all_arr = self.arr
            else:
                self.all_arr = np.append(self.all_arr, self.arr, axis=0)
                print(self.all_arr.shape)

    def read_file(self, filename):
        im = cv2.imread(filename) # 打开一个图像
         # 将图像的RGB分离

        # 将32*32二位数组转成1024的一维数组

        olivettifaces = np.empty((8, 8, 3))  # 开辟一个空数组
        olivettifaces = np.array([im])
        return olivettifaces

    def pickle_save(self, arr):
        print("正在存储")
        # 构造字典,所有的图像数据都在arr数组里,我这里是个一维数组,目前并没有存label
        f = open('img/rightImg.pkl', 'wb+')###还有此处用wb+ ，原作者用的 w ，一直报错
        pickle.dump(arr, f) # 把字典存到文本中去
        f.close()
        print("存储完毕")

if __name__ == "__main__":
    filenames = []
    for i in range(0, 1109):
        filename = [os.path.join("E:/detectPerson/roiImg/rightImg/", "img%d" % i)+".png"]
        print(filename)
        filenames = filenames + filename

    print(filenames)
    ds = DictSave(filenames)
    ds.image_input(ds.filenames)
    ds.pickle_save(ds.all_arr)
    print("最终数组的大小:" + str(ds.all_arr.shape))

