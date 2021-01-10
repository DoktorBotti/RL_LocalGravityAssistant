from pynput import mouse
from SelectorState import ForceVolumePositions, Point
import ctypes
import cv2 as cv
import numpy as np
from PIL import ImageGrab
import pytesseract as ocr

# grabs a screenshot of insterest with the boundingbox (lowX,lowY,highX,highY), debug also exexutes imshow
def getCvScreenshot(bbox, debug=False):
    print(bbox)
    pil_image = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True)
    open_cv_img = np.array(pil_image)[bbox[1]:bbox[3],bbox[0]:bbox[2]]
    if debug:
        tmp = cv.cvtColor(open_cv_img,cv.COLOR_BGR2RGB)
        cv.imshow('foo',tmp)
        cv.waitKey(0)
    return open_cv_img

def getForceVolumeClicks():
    msgs = forceVolPos.getPrintMessages()
    clickPositions = []
    for el in msgs:
        print(el)
        # mouse click callback
        def onClick(x,y,button,pressed):
            if(pressed):
                print(Point(x,y))
                clickPositions.append(Point(x,y))
            else:
                # Stop listener
                return False
        # record click
        with mouse.Listener(on_click=onClick) as listener:
            listener.join()
    forceVolPos.assignPositions(clickPositions)

def getTextInImage(image):
    return ocr.image_to_string(image)

forceVolPos = ForceVolumePositions()
def main():
    # avoiding inconsistences between recording and controlling mouse
    #PROCESS_PER_MONITOR_DPI_AWARE = 2
    #ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    
    #welcome message
    print("Welcome to the Gravity Assistant for Unreal Engine 3. \nThe script assumes that you have already placed the ForceVolumes in your map.")
    print("This includes the attached PathNodes. Also the configured mass points should be positioned as well.\n\nDuring the runtime, please do not interfere, except wen you are told to.")
    
    # Getting relevant mouse positions
    getForceVolumeClicks()

    # grabbing images of clicked boundingboxes
    
    bbox = Point.getBbox(forceVolPos.forceDirectionCoordTopLeft,forceVolPos.forceDirectionCoordBottomRight,forceVolPos.zeroPosition.toTuple())
    img = getCvScreenshot(bbox, True)
    imageText = getTextInImage(img)




main()