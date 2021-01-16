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
    if len(massPts) > 0: 
        ptMatrix = np.stack(massPtArray,axis=0)
        mx,my,mz = np.hsplit(ptMatrix, 3)
        ax.scatter(mx,my,mz, label='Mass Points')

    if len(pointArray) != 0:
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

def changeForceMode(programState):
    userChoice = ""
    while True:
        listedOptions = """ - 'ForceMode_Force'             <F>   : Applies the specified constant force on all contained objects (default).
- 'ForceMode_Acceleration'      <A>   : Accelerates all objects inside with a constant rate to the target vector. (good alternative)
- 'ForceMode_Impulse'           <I>   : Applies an impuls continuously (? makes no sense...).
- 'ForceMode_Velocity'          <V>   : Propells all entered dynamic objects with a constant speed.
- 'ForceMode_SmoothImpulse'     <sI>  : Like impulse mode, but applied along a longer time interval (?)
- 'ForceMode_SmoothVelocity'    <sV>  : Like velocity mode, but no direct acceleration to target velocity.
Type the desired mode then enter.
    """
        print("\nThis setting will remain unchanged for the duration of this program or until changed again.\nUDK allows the following force application in the constant mode: \n" + listedOptions)
        userInput = input().lower()
        if userInput == 'f':
            userChoice = "ForceMode_Force"
            break
        if userInput == 'a':
            userChoice = "ForceMode_Acceleration"
            break
        if userInput == 'i':
            userChoice = "ForceMode_Impulse"
            break
        if userInput == 'v':
            userChoice = "ForceMode_Velocity"
            break
        if userInput == 'si':
            userChoice = "ForceMode_SmoothImpulse"
            break
        if userInput == 'sv':
            userChoice = "ForceMode_SmoothVelocity"
            break
    print(f"Scelected option \'{userChoice}\'\n")
    programState.forceMode = userChoice