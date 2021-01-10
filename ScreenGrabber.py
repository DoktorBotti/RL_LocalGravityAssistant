from PIL import ImageGrab
import pytesseract as ocr
import re
import cv2 as cv
import numpy as np


class ScreenGrabber:
    def __init__(self):
        super().__init__()

    # grabs a screenshot of insterest with the boundingbox (lowX,lowY,highX,highY), debug also exexutes imshow
    @staticmethod
    def getCvScreenshot(bbox, debug=False):
        pil_image = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True)
        open_cv_img = np.array(pil_image)[bbox[1]:bbox[3],bbox[0]:bbox[2]]
        if debug:
            tmp = cv.cvtColor(open_cv_img,cv.COLOR_BGR2RGB)
            cv.imshow('foo',tmp)
            cv.waitKey(0)
        return open_cv_img
    @staticmethod
    def getDigitsInImage(image):
        return ocr.image_to_string(image,config='digits')

    @staticmethod
    def getLocationBatch(bbox, debug = False):
        # screenshotting region
        img = ScreenGrabber.getCvScreenshot(bbox)
        #img = []
        if False:
            imgPath = "E:/WIN/Development/RL_GUIautomation/sampleImg/temp.png"
            img = cv.imread(imgPath)
            img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        imageText = ScreenGrabber.getDigitsInImage(img)
        # extracting coordinates
        ret = []
        xyz_regex = r"(-?\d+)[\.\,](\d{3}).*?(-?\d+)[\.\,](\d{3}).*?(-?\d+)\.(\d{3}).*"
        matches = re.finditer(xyz_regex, imageText, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            if debug:
                print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
                for groupNum in range(0, len(match.groups())): 
                    groupNum = groupNum + 1
                    print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
            # TODO: fix recognize misread ~ character instead of -
            ret.append((float(match.group(1)+ '.'+match.group(2)),float(match.group(3)+ '.'+match.group(4)), float(match.group(5)+ '.'+match.group(6))))
        if debug:
            print(ret)
        if len(ret) != 10: 
            print("problem! -Not all numbers detected, raw text:")
            print(imageText)
            cv.imshow('error state',img)
            cv.waitKey(0)
        return ret

    