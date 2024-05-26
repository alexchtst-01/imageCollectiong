import cv2 as cv
import random

class collectImage:
    def __init__(self, root, videoDirectory, num=5, manual=False):
        self.root = root
        self.videoDirectory = videoDirectory
        self.manual = manual
        self.num = num

        self.__run__()
    
    def __getImage__(self, idx, img):
        cv.imwrite(f"{self.root}/{idx}.jpg", img)
    
    def __run__(self):
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
                    self.__getImage__(idx=i, img=frame)
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
                self.__getImage__(idx=i, img=frame)

        cap.release()
        cv.destroyAllWindows()


# how to use
# test = collectImage(root="datares", videoDirectory="./video/sample.mp4", manual=True)