import numpy as np
import math

class Position(object):
    def __init__(self, x,y,z):
        self.arr = np.array([x,y,z])
    def __str__(self):
        return f"({self.arr[0]}, {self.arr[1]}, {self.arr[2]})"
    def __str__(self):
        return f"({self.arr[0]}, {self.arr[1]}, {self.arr[2]})"
    @staticmethod
    def cross(a,b):
        return np.cross(a.arr,b.arr)
    @staticmethod
    def dist(a, b):
        return math.sqrt(np.dot(a,a) + np.dot(b,b))
    def norm(self):
        return Position.dist(self,self)
    def normalized(self):
        return np.multiply(self.arr,1/norm(self))
class MassPoint(object):
    def __init__(self, pos, mass):
        self.position = pos
        self.mass = mass
    def __str__(self):
        return f"MassPoint({self.position}, {self.mass} kg)"
    def __repr__(self):
        return f"MassPoint({self.position}, {self.mass} kg)"

class Rotation(object):
    def __init__(self,r,p,y):
        self.roll = r
        self.pitch = p
        self.yaw = y
    def getDirectionVec(self):
        #TODO
        print("TODO")
        return Position(0,0,0)
        
    def fromDirectionalVec(self, vec):
        #TODO
        print("TODO")

    def __str__(self):
        return f"(r:{self.roll}, p:{self.pitch}, y:{self.yaw})"
    def __repr__(self):
        return f"(r:{self.roll}, p:{self.pitch}, y:{self.yaw})"

class Physics:
    def __init__(self):
        self.massPoints = []
    
    def getMassPoints(self):
        return self.massPoints
    def addMassPoint(self, mass, position):
        self.massPoints.append(MassPoint(position,mass))

    def addMassPoint(self, massPt):
        self.massPoints.append(massPt)
    def getForceOnPosition(self, pos):
        # TODO make force calcuation
        return (Rotation(1,37,7),12.34)

    def __str__(self):
        return f"Physics instance. MassPoints: {self.massPoints}"
    def __repr__(self):
        return f"Physics instance. MassPoints: {self.massPoints}"