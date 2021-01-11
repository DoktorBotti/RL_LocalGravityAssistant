from pynput import mouse
from pynput.keyboard import Key, Controller
import StateMachine 
from SelectorState import ForceVolumePositions, ClickPoint
from ScreenGrabber import ScreenGrabber
from ScreenCoordinates import ROI, ClickPoint
import jsonpickle as jsonIo
import ctypes
import cv2 as cv
import time



def performClickRequests(stateClass):
    msgs = stateClass.getPrintMessages()
    clickPositions = []
    for el in msgs:
        print(el)
        # mouse click callback
        def onClick(x,y,button,pressed):
            if(pressed):
                print(ClickPoint(x,y))
                clickPositions.append(ClickPoint(x,y))
            else:
                # Stop listener
                return False
        # record click
        with mouse.Listener(on_click=onClick) as listener:
            listener.join()
    stateClass.assignPositions(clickPositions)

def getAllPositions():
    print("I will now scan and edit the ForceVolumes.\nCHECK THAT THE VISIBLE LIST IS 10 ELEMENTS LONG!\nType the number of expected enties:")
    # ask how many elements to expect
    numForceVolumes = int(input())
    mouseCtrl = mouse.Controller()
    keyCtrl = Controller()
    numBatches = int(numForceVolumes / 10)
    rest = numForceVolumes % 10
    for batchNum in range(numBatches):
        bbox = forceVolPos.roi_location.toScreenshotTuple()
        ret = ScreenGrabber.getLocationBatch(bbox)
        # click on each location and extract screenshot of force direction ID
        for batchElem in range(10):
            # moving away curser (readable screenshot)
            mouseCtrl.position = (0,0)

            # selecting element
            posX = int((forceVolPos.locationCoordBottomRight.getX() + forceVolPos.locationCoordTopLeft.getX())/2.0)
            yDiff = forceVolPos.locationCoordBottomRight.getY() - forceVolPos.locationCoordTopLeft.getY()
            posY = int(forceVolPos.locationCoordTopLeft.getY() + yDiff*batchElem / 10 + yDiff / 20)
            locationImage = ScreenGrabber.getCvScreenshot(bbox)
            alternativePos = forceVolPos.roi_location.getPositionBySclale(0.5,float(batchElem)/10.0)
            #locationImage = cv.line(locationImage, (0,posY-forceVolPos.locationCoordTopLeft.getY()),(locationImage.shape[1],posY-forceVolPos.locationCoordTopLeft.getY()),(0,0,255),thickness=1)
            mouseCtrl.position = (posX,posY)
            mouseCtrl.press(mouse.Button.left)
            mouseCtrl.release(mouse.Button.left)
            time.sleep(0.2)

            # setting constant force
            forcePt = forceVolPos.constantForceMiddle #Point.difference(forceVolPos.constantForceMiddle, forceVolPos.zeroPosition)
            mouseCtrl.position= forcePt.toTuple()
            mouseCtrl.press(mouse.Button.left)
            mouseCtrl.release(mouse.Button.left)
            time.sleep(0.2)
            keyCtrl.type('1337.000')
            keyCtrl.press(Key.enter)
            keyCtrl.release(Key.enter)
            mouseCtrl.position = (posX,posY)

            # screenshot Node reference number

        mouseCtrl.scroll(0,-4)
        time.sleep(0.2)

forceVolPos = ForceVolumePositions()
def main():
    # avoiding inconsistences between recording and controlling mouse
    #PROCESS_PER_MONITOR_DPI_AWARE = 2
    #ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

    
    stateMachine = StateMachine.StateMachine()
    while(True):
        nextState = stateMachine.state.exec()
        if nextState != None:
            stateMachine.change(nextState)
        else:
            stateInput = input()
            nextState = stateMachine.change(eval(stateInput))
    # Getting relevant mouse positions
    performClickRequests(forceVolPos)
    print(jsonIo.encode(forceVolPos))
    forceVolPos.importFromFile()
    # grabbing images of clicked boundingboxes
    if False:
        bbox = ClickPoint.getBbox(forceVolPos.locationCoordTopLeft,forceVolPos.locationCoordBottomRight,forceVolPos.zeroPosition.toTuple())
        ret = ScreenGrabber.getLocationBatch(bbox)
        print(ret)
    getAllPositions()

main()