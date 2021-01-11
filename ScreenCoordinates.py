import pynput

class ClickPoint(object):
    def __init__(self,x,y):
        self.X = int(x)
        self.Y = int(y)
    def __str__(self):
        return f"ClickPoint({self.X}, {self.Y})"
    def __repr__(self):
        return f"ClickPoint({self.X}, {self.Y})"
    def getX(self):
        return self.X
    def getY(self):
        return self.Y
    def difference(self, other):
        return ClickPoint(self.X - other.getX(), self.Y - other.getY())
    def toTuple(self):
        return (self.X,self.Y)
    #@staticmethod
    #def getBbox(start, end, offset=(0,0)):
    #    return (start.getX()-offset[0],start.getY()-offset[1],end.getX()-offset[0],end.getY()-offset[1])

class ROI:
    def __init__(self):
        self.topLeft = ClickPoint(0,0)
        self.bottRight = ClickPoint(0,0)
    
    #static variable allows calibration for Screenshot compatibility
    calibrationPoint = ClickPoint(0,0)
    @classmethod
    def createFromCorners(cls, topLeft, bottRight):
        ret = cls()
        ret.topLeft =topLeft
        ret.bottRight = bottRight
        return ret
    def tl(self):
        return self.topLeft
    def br(self):
        return self.bottRight
    def isValid(self):
        diff = self.bottRight.difference(self.topLeft)
        return diff.getX() > 0 and diff.getY() > 0
    def width(self):
        return self.bottRight.getX()-self.topLeft.getX()
    def height(self):
        return self.bottRight.getY() -self.topLeft.getY()
    # returns the clicking point (can be negative) for scaleX and scaleY from 0 to 1 for inside the box
    def getPositionBySclale(self, scaleX, scaleY):
        diffX = self.bottRight.getX() - self.topLeft.getX()
        diffY = self.bottRight.getY() - self.topLeft.getY()
        return ClickPoint(self.topLeft.getX() + scaleX * diffX, self.topLeft.getY() + scaleY * diffY)
    def toScreenshotTuple(self):
        return (self.topLeft.getX()-self.calibrationPoint.getX(), self.topLeft.getY()-self.calibrationPoint.getY(), self.bottRight.getX()-self.calibrationPoint.getX(), self.bottRight.getY()-self.calibrationPoint.getY())

