class ClickPoint(object):
    def __init__(self,x,y):
        self.X = x
        self.Y = y
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
    @staticmethod
    def getBbox(start, end, offset=(0,0)):
        return (start.getX()-offset[0],start.getY()-offset[1],end.getX()-offset[0],end.getY()-offset[1])

class ROI:
    def __init__(self, topLeft, bottomRight):
        self.topLeft = topLeft
        self.bottRight = bottomRight
    def __init__(self):
        self.topLeft = ClickPoint(0,0)
        self.bottRight = ClickPoint(0,0)
    def tl(self):
        return self.topLeft
    def br(self):
        return self.bottRight
    def isValid(self):
        diff = self.bottRight.difference(self.topLeft)
        return diff.getX() > 0 and diff.getY() > 0
