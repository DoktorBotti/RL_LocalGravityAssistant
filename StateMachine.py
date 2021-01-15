import abc
import pyperclip as pc
import numpy as np
from Physics import Physics, MassPoint, Position
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import HelperFunctions
import re

def getTriggers(str):
   return re.search(r"Begin Actor Class=Trigger",str)

class StateInterface(abc.ABC):
   @abc.abstractmethod
   def exec(self, progState):
      pass

class StateClass(object):
   name = "state"
   allowed = []

   def switch(self, state):
      """ Switch to new state """
      if state.name in self.allowed:
         #print('Current:',self,' => switched to new state',state.name)
         self.__class__ = state
         return True
      else:
         #print('Current:',self,' => switching to',state.name,'not possible.')
         return False

   def __str__(self):
      return self.name
      
# ---------------------- Individual States  ----------------------

@StateInterface.register
class Init(StateClass):
   name = "init"
   allowed = ['importMassPointsEd', 'importMassPointsText']
   def exec(self, progState):
      #welcome message
      print("Welcome to the Gravity Assistant for Unreal Engine 3. \n")
      
      return ImportMassPointsEd

@StateInterface.register
class ImportMassPointsEd(StateClass):
   name = "importMassPointsEd"
   allowed = ['copyVolAndPathnodes']
   def exec(self, progState):
      #welcome message
      print("Please use the copy feature for all Triggers that should be interpreted as mass points.")
      print("You can already scelect PathNodes and ForceVolumes too. This temporal memory will only be read and seached for Trigger values.")
      print("The Tag corresponds to the mass of the simulated object in kg.")
      print("Confirm with enter")
      _ = input()
      massVolumesText = pc.paste()
      #with open('dumpTriggerActors.txt', 'w') as f:
       #  f.write(massVolumesText)
      # perform analysis --> add mass points to physics
      regex = r"Begin Actor Class=Trigger(?:.|\n)*?Location=\(X=(.*?),Y=(.*?),Z=(.*?)\)(?:.|\n)*?Tag=\"(.*?)\""
      matches = re.finditer(regex, massVolumesText, re.MULTILINE)
      for matchNum, match in enumerate(matches, start=1):
         pos = Position(float(match.group(1)),float(match.group(2)),float(match.group(3)))
         mass = 0
         try:
            mass = float(match.group(4))
         except ValueError:
            print(f"Mass point at {pos} had no Tag assigned. -Skipping")
            continue
         progState.physics.addMassPoint(MassPoint(pos,mass))

      print(f"Loaded {len(progState.physics.getMassPoints())} mass points.")
      # checking validity of mass points
      # TODO stuff?
      return CopyVolAndPathnodes

@StateInterface.register
class CopyVolAndPathnodes(StateClass):
   name = "copyVolAndPathnodes"
   allowed = ['performCalc']
   def exec(self, progState):
      print("Copy all ForceVolumes and PathNodes that should be manipulated. Then press enter to continue")
      _ = input()
      progState.copiedText = pc.paste()
      requiredPathNodes = set([])
   
      # dumping to File for debugging
      #with open('dumpVolAndPath.txt', 'w') as f:
      #      f.write(progState.copiedText)
      # reading all ForceVolumes
      regex_forceVol  = r"Begin Actor Class=ForceVolume_TA Name=(.+?) (?:.|\n)*?CustomForceDirection=PathNode\'(.*?)\'(?:.|\n)*?Location=\(X=(.*?),Y=(.*?),Z=(.*?)\)"
      matches = re.finditer(regex_forceVol, progState.copiedText, re.MULTILINE)
      forceVolMatches = re.finditer(r"Begin Actor Class=ForceVolume_TA Name=(.+?) (?:.|\n)*?End Actor", progState.copiedText, re.MULTILINE)
      for match in forceVolMatches:
         name = match.group(1)
         posMatch = re.search(r"Location=\(X=(.*?),Y=(.*?),Z=(.*?)\)",match.group(0))
         pos = ()
         if posMatch == None:
            pos = Position(0,0,0) # UE does not generate a field, when the object stays on (0,0,0)
         else:
            pos = Position(float(posMatch.group(1)),float(posMatch.group(2)),float(posMatch.group(3)))
         pathNodeMatch = re.search(r"CustomForceDirection=PathNode\'(.*?)\'",match.group(0))
         if pathNodeMatch == None:
            print(f"Error! No PathNode reference found in {name}. Discarding this volume.")
            continue

         requiredPathNodes.add(pathNodeMatch.group(1))
         progState.forceVolumeList.append((name, pos, pathNodeMatch.group(1)))
      
      # checking if all needed PathNodes are available
      regex_pathNode = r"Begin Actor Class=PathNode Name=(.+?) "
      pathNode_matches = re.finditer(regex_pathNode, progState.copiedText, re.MULTILINE)
      # feedback to user
      print(f"Loaded {len(progState.forceVolumeList)} ForceVolumes.")
      for match in pathNode_matches:
         requiredPathNodes.discard(match.group(1))
      if len(requiredPathNodes) != 0:
         print("Your copy from the editor did not include all linked PathNodes! The missing names are:")
         print(requiredPathNodes)
      return PerformCalc


@StateInterface.register
class PerformCalc(StateClass):
   name = "performCalc"
   allowed = ['copyVolAndPathnodes', 'init']
   def exec(self, progState):
      print("Calculating...")
      # TODO for each key take Position and calculate forces. Store inside rpyDict[pathNodeName] = (r,p,y) and listForces = [(name, force)]
      
      # split text into pieces per ForceVolume
      splForceVol_re = r"Begin Actor Class=ForceVolume_TA"
      forceVolElementList = re.split(splForceVol_re, progState.copiedText)
      header_beforeForceList = forceVolElementList.pop(0) # first segment contains no ForceVolume
      forceVolElementList = list(splForceVol_re + el for el in forceVolElementList)
      # throw out any presettings regarding constant and enter forces
      strippedForceVolList = []
      for forceVolText in forceVolElementList:
         strippedEl = re.sub(r" *(?:ConstantForceMo| ForceDirec|ConstantForce|EnterForce).*\n","",forceVolText)
         strippedForceVolList.append(strippedEl)
      forceVolElementList = strippedForceVolList
      # preparing new variables for next step
      PathElToRPYDict = dict()
      postForceVolSubs = header_beforeForceList
      test = header_beforeForceList
      #for each element in the list: find replacement values by calculating force and orientation
      for (textEl, data) in zip(forceVolElementList, progState.forceVolumeList):
         constForceMode = 'ForceMode_Force' 'ForceMode_Acceleration'
         constForceVal, PathElToRPYDict[data[2]] = progState.physics.getForceRPYtuple(data[1])
         subs_regex = r"(Begin Actor Class=ForceVolume_TA (?:.|\n)*?)CustomForc"
         subst = f"\g<1>ForceDirection=EFD_Custom\n         ConstantForceMode={constForceMode}\n         ConstantForce={constForceVal}\n         EnterForce=0.000000\n         CustomForc"
         res = re.sub(subs_regex,subst, textEl,0, re.MULTILINE) 
         postForceVolSubs += res
         test += textEl
      if len(forceVolElementList) != len(progState.forceVolumeList):
         missingIndices = len(forceVolElementList) - len(progState.forceVolumeList)
         for el in forceVolElementList[-missingIndices:]:
            postForceVolSubs += el
      # rearranging original string - but with substituted values

      # apply rpy changes to all path nodes (first remove any existing rpy entry)
      removePrevRotation_regex = r"(Begin Actor Class=PathNode (?:.|\n)*)         Rotation.*\n"
      subs_string = "\g<1>"
      resText = re.sub(removePrevRotation_regex, subs_string, postForceVolSubs, re.MULTILINE)

      # split by PathElemens
      splPathEl_re = r"Begin Actor Class=PathNode"
      pathElemStrList = re.split(splPathEl_re,resText)
      header_beforePathElList = pathElemStrList.pop(0)
      pathElemStrList = list(splPathEl_re + el for el in pathElemStrList)
      pathElemResList =[""]
      test= ""
      for pathElStr in pathElemStrList:
         pName = re.search(r"Begin Actor Class=PathNode Name=(.*) ", pathElStr).group(1)
         if not pName in PathElToRPYDict.keys():
            pathElemResList.append(pathElStr)
            continue
         r, p, y = PathElToRPYDict[pName]
         #insert rotation information below location
         splittedByLocation = re.split(r"Location", pathElStr,1)
         pathElemResList.append(splittedByLocation[0])
         firstLineSplit = re.split(r"\n",splittedByLocation[1],1)
         pathElemResList.append("Location" + firstLineSplit[0])
         factor = 182.05 # WTF
         pathElemResList.append(f"         Rotation=(Pitch={p*factor},Yaw={y*factor},Roll={r*factor}\n")
         pathElemResList.append(firstLineSplit[1])
         test +=pathElStr
      
      resText = header_beforePathElList + ''.join(pathElemResList)
      pc.copy(resText)
      while True:
         print("You can now remove the scelected ForceVolumes and Path nodes and paste the newly created items.\n V:     Plot a visualization? \n I:     Import additional batch of ForceVolumes\n R:     Restart entire program\n <any>: End Program")
         inp = input()
         if inp == 'V' or inp == 'v':
            HelperFunctions.plotWithVolumes(progState.physics, progState.forceVolumeList)
         elif inp == 'I' or inp == 'i':
            progState.forceVolumeList = list()
            progState.copiedText = ""
            return CopyVolAndPathnodes
         elif inp == 'R' or inp == 'r':
            progState.forceVolumeList = list()
            progState.copiedText = ""
            progState.physics = Physics()
            return Init
         else:
            exit()

class StateMachine(object):
   """ represents the State Machine """
   def __init__(self):
      self.state = Init()
   
   def change(self, state):
      """ Change state """
      self.state.switch(state)