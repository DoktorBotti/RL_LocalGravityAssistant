import array as arr
import re
from ScreenCoordinates import ClickPoint, ROI


class ForceVolumePositions:
    def __init__(self):
        # Setting ForceVolume coordinates
        self.roi_location = ROI()
        self.pt_constantForce = ClickPoint(0,0)
        self.roi_forceDirectionRef = ROI()
    
    def getPrintMessages(self):
        ret = ["Click the top left corner of the first entry in the location column"]
        ret.append("Click the bottom right corner of the TENTH entry in the location column, this must be the last visible entry!(you can correct this afterwards)")
        ret.append("Click in the center of the Constant force edit field")
        ret.append("Click in the TOP LEFT area of the Custom Force direction field, SO THAT ONLY THE ENDING NUMBERS ARE READABLE")
        ret.append("Click in the BOTTOM RIGHT area of the Custom Force direction field, SO THAT ONLY THE ENDING NUMBERS ARE READABLE")


        return ret
    def assignPositions(self, arr):
        self.roi_location = ROI.createFromCorners(arr[0], arr[1])
        self.pt_constantForce = arr[2]
        self.roi_forceDirectionRef = ROI.createFromCorners(arr[3],arr[4])
