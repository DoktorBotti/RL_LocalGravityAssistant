import array as arr

class Point(object):
    def __init__(self,x,y):
        self.X = x
        self.Y = y
    def __str__(self):
        return f"Point({self.X}, {self.Y})"
    def __repr__(self):
        return f"Point({self.X}, {self.Y})"
    def getX(self):
        return self.X
    def getY(self):
        return self.Y
    def difference(self, other):
        return Point(self.X - other.getY(), self.Y - other.getY())
    def toTuple(self):
        return (self.X,self.Y)
    @staticmethod
    def getBbox(start, end, offset=(0,0)):
        return (start.getX()-offset[0],start.getY()-offset[1],end.getX()-offset[0],end.getY()-offset[1])

class ForceVolumePositions:
    def __init__(self):
        # Setting ForceVolume coordinates
        self.zeroPosition = Point(0,0)
        self.locationCoordTopLeft = Point(0,0)
        self.locationCoordBottomRight = Point(0,0)
        self.constantForceCoord=Point(0,0)
        self.forceDirectionCoordTopLeft = Point(0,0)
        self.forceDirectionCoordBottomRight = Point(0,0)
        self.ninthEntryBottom = Point(0,0)
    
    def getPrintMessages(self):
        ret = ["Click in the top left corner of your leftmost monitor"]
        ret.append("Click the top left corner of the first entry in the location column")
        ret.append("Click the bottom right corner of the first entry in the location column")
        ret.append("Click in the center of the Constant force edit field")
        ret.append("Click the top left corner of the Custom Force Direction edit field.\nTHE WHOLE INPUT MUST BE VISIBLE")
        ret.append("Click the bottom right corner of the Custom Force Direction edit field.")
        ret.append("Click the bottom of the ninth list entry. (This scales the click positions)")


        return ret
    def assignPositions(self, arr):
        self.zeroPosition = arr[0]
        self.locationCoordTopLeft = arr[1]
        self.locationCoordBottomRight = arr[2]
        self.constantForceCoordTopLeft = arr[3]
        self.forceDirectionCoordTopLeft = arr[4]
        self.forceDirectionCoordBottomRight= arr[5]
        self.ninthEntryBottom = arr[6]


class PathNodePositions:
    def __init__(self):
        # Setting Path node coordinates
        self.actorNameCoordTopLeft = Point(0,0)
        self.actorNameCoordBottomRight = Point(0,0)
        self.rpyCoordTopLeft = Point(0,0)
        self.rpyBottomRight = Point(0,0)

