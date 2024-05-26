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
    
    def __triangle(self):
        pass
    
    def __rectangle(self):
        pass

    def __circle(self):
        pass

    def generateImage(self, triangleNum, circleNum, rectNum):
        pass

    def makeMask(self):
        pass

    def __generatedataset(self):
        pass

    def __makedir(self):
        os.mkdir(self.imagePath)
        os.mkdir(self.maskPath)