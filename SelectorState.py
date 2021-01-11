import array as arr
import re
from ClickingStuff import ClickPoint, ROI


class ForceVolumePositions:
    def __init__(self):
        # Setting ForceVolume coordinates
        self.zeroPosition = ClickPoint(0,0)
        self.locationCoordTopLeft = ClickPoint(0,0)
        self.locationCoordBottomRight = ClickPoint(0,0)
        self.constantForceCoord=ClickPoint(0,0)
        self.forceDirectionCoordTopLeft = ClickPoint(0,0)
        self.forceDirectionCoordBottomRight = ClickPoint(0,0)
        self.eleventhEntryBottom = ClickPoint(0,0)
    
    def getPrintMessages(self):
        ret = ["Click in the top left corner of your leftmost monitor"]
        ret.append("Click the top left corner of the first entry in the location column")
        ret.append("Click the bottom right corner of the tenthth entry in the location column")
        ret.append("Click in the center of the Constant force edit field")
        ret.append("Click the top left corner of the Custom Force Direction edit field.\nTHE WHOLE INPUT MUST BE VISIBLE")
        ret.append("Click the bottom right corner of the Custom Force Direction edit field.")


        return ret
    def assignPositions(self, arr):
        self.zeroPosition = arr[0]
        self.locationCoordTopLeft = arr[1]
        self.locationCoordBottomRight = arr[2]
        self.constantForceMiddle = arr[3]
        self.forceDirectionCoordTopLeft = arr[4]
        self.forceDirectionCoordBottomRight= arr[5]
    def exportPositions(self):
        with open("ForceVolumesClickPts.tmp","w") as file:
            file.write(self.zeroPosition.__repr__()+"\n")
            file.write(self.locationCoordTopLeft.__repr__()+"\n")
            file.write(self.locationCoordBottomRight.__repr__()+"\n")
            file.write(self.constantForceMiddle.__repr__()+"\n")
            file.write(self.forceDirectionCoordTopLeft.__repr__()+"\n")
            file.write(self.forceDirectionCoordBottomRight.__repr__()+"\n")
    def importFromFile(self):
        with open("ForceVolumesClickPts.tmp", "r") as file:
            arr = []
            regex = r"Point\((.*), (.*)\)"
            lines = '\n'.join(file.readlines())
            matches = re.finditer(regex, lines)
            for matchnum,match in enumerate(matches, start=1):
                arr.append(ClickPoint(int(match.group(1)),int(match.group(2))))
            self.assignPositions(arr)




class PathNodePositions:
    def __init__(self):
        # Setting Path node coordinates
        self.actorNameCoordTopLeft = ClickPoint(0,0)
        self.actorNameCoordBottomRight = ClickPoint(0,0)
        self.rpyCoordTopLeft = ClickPoint(0,0)
        self.rpyBottomRight = ClickPoint(0,0)

