import abc
import pyperclip as pc
import numpy as np
from Physics import Physics, MassPoint, Position
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import HelperFunctions
import re

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
         print('Current:',self,' => switched to new state',state.name)
         self.__class__ = state
         return True
      else:
         print('Current:',self,' => switching to',state.name,'not possible.')
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
      print("Welcome to the Gravity Assistant for Unreal Engine 3. \nThe script assumes that you have already placed the ForceVolumes in your map.")
      print("This includes the attached PathNodes. The configured mass points should be positioned as well.")
      
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
      regex = r"Begin Actor Class=Trigger(?:.|\n)*?Location=\(X=(.*?),Y=(.*?),Z=(.*?)\)(?:.|\n)*?Tag=\"(.*)\""
      matches = re.finditer(regex, massVolumesText, re.MULTILINE)
      for matchNum, match in enumerate(matches, start=1):
         pos = Position(float(match.group(1)),float(match.group(2)),float(match.group(3)))
         mass = float(match.group(4))
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
      for matchNum, match in enumerate(matches, start=1):
         pos = Position(float(match.group(3)),float(match.group(4)),float(match.group(5)))
         pathNodeRef = match.group(2)
         name = match.group(1)
         requiredPathNodes.add(pathNodeRef)
         progState.forceVolumeList.append((name, pos, pathNodeRef))
      
      # checking if all needed PathNodes are available
      regex_pathNode = r"Begin Actor Class=PathNode Name=(.+?) "
      pathNode_matches = re.finditer(regex_pathNode, progState.copiedText, re.MULTILINE)
      # feedback to user
      print(f"Loaded {len(progState.forceVolumeList)} ForceVolumes.")
      for match in pathNode_matches:
         requiredPathNodes.discard(match.group(1))
      if len(requiredPathNodes) != 0:
         print("Your copy of the editor did not include all linked PathNodes! The missing names are:")
         print(requiredPathNodes)
      return PerformCalc


@StateInterface.register
class PerformCalc(StateClass):
   name = "performCalc"
   allowed = ['copyVolAndPathnodes']
   def exec(self, progState):
      print("Calculating...")
      # TODO for each key take Position and calculate forces. Store inside rpyDict[pathNodeName] = (r,p,y) and listForces = [(name, force)]
      #name is for doublechecking.
      #pc.copy(res)
      while True:
         print("You can now remove the scelected ForceVolumes and Path nodes and paste the newly created items.\n V:     Plot a visualization? \n I:     Import additional batch of ForceVolumes\n <any>: End Program")
         inp = input()
         if inp == 'V' or inp == 'v':
            HelperFunctions.plotWithVolumes(progState.physics, progState.forceVolumeList)
         elif inp == 'I' or inp == 'i':
            return CopyVolAndPathnodes
         else:
            exit()

class StateMachine(object):
   """ represents the State Machine """
   def __init__(self):
      self.state = Init()
   
   def change(self, state):
      """ Change state """
      self.state.switch(state)