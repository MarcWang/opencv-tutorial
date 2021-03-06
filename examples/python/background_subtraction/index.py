import numpy as np
import cv2


class BackgroundSubtractor:

    def __init__(self):
        history = 1500
        varThreshold = 60
        detectShadows = False
        self.detector = cv2.createBackgroundSubtractorMOG2(
            history, varThreshold, detectShadows)

    def process(self, frame):
        fgmask = self.detector.apply(frame)

        kernel = np.ones((5, 5), np.uint8)
        erodeImg = cv2.erode(fgmask, kernel)
        dilateImg = cv2.dilate(erodeImg, kernel)

        return dilateImg


class MediaProcessor:

    def __init__(self, detector):
        self.detector = detector

    def run(self):
        video = cv2.VideoCapture(0)

        while(True):
            ret, frame = video.read()

            fgmask = self.detector.process(frame)

            im2, contours, hierarchy = cv2.findContours(
                fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            areaArray = []
            for i, c in enumerate(contours):
                area = cv2.contourArea(c)
                areaArray.append(area)

            sorteddata = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

            if len(sorteddata) > 1:
            	largestcontour = sorteddata[0]
            	cv2.drawContours(frame, largestcontour, -1, (0, 255, 0), 3)

            cv2.imshow('fgmask', fgmask)
            cv2.imshow('frame', frame)
            cv2.waitKey(33)

        video.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':

    detector = BackgroundSubtractor()
    mediaRes = MediaProcessor(detector)
    mediaRes.run()
