from ScreenCoordinates import ClickPoint, ROI
import numpy as np
import json
class MassPointClickRegions:
    def __init__(self):
        self.pos_topleftMonitor = ClickPoint()
        self.roi_idCollumn = ROI()
        self.roi_massValue = ROI()
        self.roi_location = ROI()

    # accepts array of click positions, which are responses to the getInputClickMessages() method
    @classmethod
    def fromPointArray(cls, arr):
        ret = cls()
        ret.pos_topleftMonitor = arr[0]
        ret.roi_idCollumn = ROI.createFromCorners(arr[1],arr[2])
        #TODO fill out rest after finishing getInputClickMessages()
        return ret

    @staticmethod
    def getInputClickMessages():
        #TODO Replace with correct info
        ret = ["Click in the top left corner of your leftmost monitor"]
        ret.append("Click the top left corner of the first entry in the location column")
        ret.append("Click the bottom right corner of the tenthth entry in the location column")
        ret.append("Click in the center of the Constant force edit field")
        ret.append("Click the top left corner of the Custom Force Direction edit field.\nTHE WHOLE INPUT MUST BE VISIBLE")
        ret.append("Click the bottom right corner of the Custom Force Direction edit field.")
        return ret
    def isValid(self):
        return self.roi_idCollumn.isValid() and self.roi_location.isValid() and self.roi_massValue.isValid()

class ReadMassPointsState:
    def __init__(self):
        self.clickRegions = [] #TODO
        self.massPoints = np.array([]) #TODO
        
    @staticmethod
    def getInputClickMessages():
        return MassPointClickRegions.getInputClickMessages()
        
    def assignClickPositions(self, arr):
        self.clickRegions = MassPointClickRegions(arr)
    
    def getClickPosState(self):
        return self.clickRegions

    def getMassPoints(self):
        return self.massPoints