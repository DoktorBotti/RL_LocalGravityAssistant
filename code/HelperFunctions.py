from Physics import Physics, MassPoint, Position
import matplotlib.pyplot as plt
import numpy as np
import re
# Import 3D Axes 
from mpl_toolkits.mplot3d import axes3d

def plotMassPoints(phyInstance):
    massPts = phyInstance.getMassPoints()
    pointArray = list(mp.position.arr for mp in massPts)
    ptMatrix = np.stack(pointArray,axis=0)
    x,y,z = np.hsplit(ptMatrix, 3)

    plottingWindow = plt.figure()

    ax = plottingWindow.add_subplot(111, projection='3d')
    ax.scatter(x,y,z, label='Mass points')
    ax.axis('equal')
    ax.legend()
    # Labeling
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    plt.show()

def plotWithVolumes(phyInstance, dictVol):
    if len(dictVol) == 0:
        print("<Nothing to plot>")
        return
    # plotting setup
    plottingWindow = plt.figure('ForceVolume')
    ax = plottingWindow.add_subplot(111, projection='3d')
    
    # prep plotting volumes

    pointArray = list(tup[1].arr for tup in dictVol)
    ptMatrix = np.stack(pointArray,axis=0)
    x,y,z = np.hsplit(ptMatrix, 3)

    # prep mass points 
    massPts = phyInstance.getMassPoints()
    massPtArray = list(mp.position.arr for mp in massPts)
    if len(pointArray) != 0:
        ptMatrix = np.stack(massPtArray,axis=0)
        mx,my,mz = np.hsplit(ptMatrix, 3)
        ax.scatter(mx,my,mz, label='Mass Points')

        # add vectors
        endPositions = list()
        for pt in pointArray:
            norm, direction = phyInstance.getNormAndRirectionVecFromPosition(Position.from_array(pt))
            endPositions.append(norm * direction)
        ptMatrix_end = np.stack(endPositions, axis=0)
        endX,endY,endZ = np.hsplit(ptMatrix_end,3)
        ax.quiver(x,y,z,endX,endY,endZ,length=100, normalize=True)

    
    ax.scatter(x,y,z, label='ForceVolume')
    ax.legend()
    # Labeling
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    plt.show()

def deleteRotationInPathElements(inputStr):
    actorSplitBegin = re.split(r"Begin Actor", inputStr)
    nextLst = [actorSplitBegin.pop(0)]
    for el in actorSplitBegin:
        nextLst.append("Begin Actor" + el)
    resList = []
    for el in nextLst:
        actorSplitEnd = re.split(r"End Actor", el) 
        nextLst2 = [actorSplitEnd.pop(0)]
        for el in actorSplitEnd:
            nextLst2.append("End Actor" + el)
        for splittedEl in nextLst2:
            pathNodesWithoutRotation = re.sub(r"(Begin Actor Class=PathNode (?:.|\n)*?)         Rotation.*\n","\g<1>", splittedEl, flags=re.MULTILINE) 
            resList.append(pathNodesWithoutRotation)
    res = ''.join(resList)
    return res