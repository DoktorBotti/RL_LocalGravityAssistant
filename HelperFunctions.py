from Physics import Physics, MassPoint, Position
import matplotlib.pyplot as plt
import numpy as np
# Import 3D Axes 
from mpl_toolkits.mplot3d import axes3d

def plotMassPoints(phyInstance):
    massPts = phyInstance.getMassPoints()
    pointArray = list(mp.position.arr for mp in massPts)
    ptMatrix = np.stack(pointArray,axis=0)
    x,y,z = np.hsplit(ptMatrix, 3)

    plottingWindow = plt.figure()

    ax = plottingWindow.add_subplot(111, projection='3d')
    ax.scatter(x,y,z)
    # Labeling
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    plt.show()

def plotVolumes(dictVol):
    positions = dictVol.values()
    pointArray = list(p.arr for p,_ in positions)
    ptMatrix = np.stack(pointArray,axis=0)
    x,y,z = np.hsplit(ptMatrix, 3)

    plottingWindow = plt.figure('ForceVolume')

    ax = plottingWindow.add_subplot(111, projection='3d')
    ax.scatter(x,y,z)
    # Labeling
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    plt.show()