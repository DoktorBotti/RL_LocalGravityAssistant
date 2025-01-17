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
    def add(a,b):
        return Position.from_array(np.add(a.arr,b.arr))
    @staticmethod
    def from_array(a):
        pos = Position(0,0,0)
        pos.arr = a
        return pos
    def subtract(self, toSubtr):
        return Position.from_array(np.add(self.arr , -1.0 * toSubtr.arr))
    def norm(self):
        return np.sqrt(np.dot(self.arr,self.arr) )
    def normalized(self):
        return np.multiply(self.arr,1/Position.norm(self))
class MassPoint(object):
    def __init__(self, pos, mass, minDst, maxDst):
        self.position = pos
        self.mass = mass
        self.minDst = minDst
        self.maxDst = maxDst
    def __str__(self):
        return f"MassPoint({self.position}, {self.mass} kg)"
    def __repr__(self):
        return f"MassPoint({self.position}, {self.mass} kg)"

class Physics:
    def __init__(self):
        self.massPoints = []
    
    def getMassPoints(self):
        return self.massPoints
    def addMassPoint(self, mass, position):
        self.massPoints.append(MassPoint(position,mass))

    def addMassPoint(self, massPt):
        self.massPoints.append(massPt)
    def getForceVecOnPosition(self, pos):
        def getForceVec(p1,m1,p2,m2):
            r = p1.subtract(p2).norm()
            F = 6.6743e-11 * m1 * m2 / r / r
            direction = p1.subtract(p2).normalized()
            return F * direction
        totalForce = np.array([0,0,0])
        for mp in self.massPoints:
            distance = pos.subtract(mp.position).norm()
            if distance < mp.minDst or distance > mp.maxDst:
                continue
            vec = getForceVec(mp.position, mp.mass,pos, 1000.0)
            totalForce = np.add(totalForce, vec)
        return totalForce
    def getForceRPYtuple(self, position):
        forceVec = self.getForceVecOnPosition(position)
        norm = np.sqrt(np.dot(forceVec,forceVec))
        if norm == 0.0:
            return (norm, (0.0,0.0,0.0))
        normalized = forceVec * 1 / norm
        yaw = np.arctan2(normalized[0],normalized[1]) * 180 / np.pi
        pitch = np.arcsin(normalized[2])* 180 / np.pi
        return (norm, (0.0,pitch,yaw))
    def getNormAndRirectionVecFromPosition(self, pos):
        forceVec = self.getForceVecOnPosition(pos)
        norm = np.sqrt(np.dot(forceVec,forceVec))
        normalized = forceVec * 1 / norm
        return (norm, normalized)

    def __str__(self):
        return f"Physics instance. MassPoints: {self.massPoints}"
    def __repr__(self):
        return f"Physics instance. MassPoints: {self.massPoints}"