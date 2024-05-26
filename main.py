import os
import cv2 as cv
import random
import numpy as np 
from matplotlib import pyplot as plt

class collectImage:
    def __init__(self, root, videoDirectory, num=5, manual=False):
        self.root = root
        self.videoDirectory = videoDirectory
        self.manual = manual
        self.num = num

        self.__run()
    
    def __getImage(self, idx, img):
        cv.imwrite(f"{self.root}/{idx}.jpg", img)
    
    def __run(self):
        cap = cv.VideoCapture(self.videoDirectory)
        if not cap.isOpened():
            print("not started .....")
            return 
        
        if self.manual:
            i = 0
            while i < self.num:
                title = "press space to take 1 image"
                ret, frame = cap.read()

                if not ret:
                    print("canceling collecting image ....")
                    break

                cv.imshow(title, frame)
                if cv.waitKey(1) == 32:
                    self.__getImage(idx=i, img=frame)
                    i += 1
                    newTitle = f"{i} image has been captured >press space to take 1 image"
                    cv.setWindowTitle(title, newTitle)
                    title = newTitle

        else:
            total_frame = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
            for i in range(self.num):
                frame = random.randint(0, total_frame)
                cap.set(cv.CAP_PROP_POS_FRAMES, frame)
                ret, frame = cap.read()
                if not ret:
                    break
                self.__getImage(idx=i, img=frame)

        cap.release()
        cv.destroyAllWindows()


# how to use
# test = collectImage(root="datares", videoDirectory="./video/sample.mp4", manual=True)

class GenerateSampleImageAnot():
    def __init__(self, root, size=5):
        self.root = root
        
        self.imagePath = f"{self.root}/images"
        self.maskPath = f"{self.root}/masks"
        self.__makedir()
        self.__generatedataset(num_images=size)
    
    def __triangle(self, arr, xpos, ypos, size):
        s = int(size / 2)
        triangle = np.tril(np.ones((size, size), dtype=bool))
        arr[xpos-s:xpos-s+triangle.shape[0],ypos-s:ypos-s+triangle.shape[1]] = triangle
        return arr
    
    def __fillrectangle(self, arr, xpos, ypos, size):
        s = int(size / 2)
        arr[ypos-s:ypos+s, xpos-s:xpos+s] = 1
        return arr
    
    def __rectangle(self, arr, xpos, ypos, size):
        s = int(size / 2)
        arr[xpos-s, ypos-s:ypos+s] = 1
        arr[xpos+s, ypos-s:ypos+s+1] = 1
        arr[xpos-s:xpos+s, ypos-s] = 1
        arr[xpos-s:xpos+s, ypos+s] = 1
        return arr
    
    def __plus(self, arr, xpos, ypos, size):
        s = int(size / 2)
        arr[xpos-1:xpos+1,ypos-s:ypos+s] = 1
        arr[xpos-s:xpos+s,ypos-1:ypos+1] = 1
        return arr

    def __circle(self, arr, xpos, ypos, size, fill=False):
        xx, yy = np.mgrid[:arr.shape[0], :arr.shape[1]]
        circle = np.sqrt((xx - xpos) ** 2 + (yy - ypos) ** 2)
        new_arr = np.logical_or(arr, np.logical_and(circle < size, circle >= size * 0.7 if not fill else True))
        return new_arr

    def generateImage(self, triangleNum, circleNum, rectNum, fillrectNum):
        pass

    def makeMask(self):
        pass

    def __generatedataset(self, num_images, shapes=(256, 256)):
        for i in range(num_images):
            canvas = np.zeros(shape=shapes)
            image = self.generateImage(canvas)
            mask = self.makeMask(image)
            plt.imsave(f"{self.imagePath}/image{i}.jpg", image)
            plt.imsave(f"{self.imagePath}/mask{i}.jpg", mask)
        pass

    def __makedir(self):
        os.mkdir(self.imagePath)
        os.mkdir(self.maskPath)