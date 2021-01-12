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
   def exec(self):
      pass

class StateClass(object):
   name = "state"
   allowed = []
   physics = Physics()
   forceVolumeDict = dict()

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
   def exec(self):
      #welcome message
      print("Welcome to the Gravity Assistant for Unreal Engine 3. \nThe script assumes that you have already placed the ForceVolumes in your map.")
      print("This includes the attached PathNodes. The configured mass points should be positioned as well.")
      print("Do you want to import your mass points from Triggers in the editor or from a textfile? respond with E(ditor) / T(ext) ")
      while True:
         inp = input()
         if inp == 'E' or inp == 'e':
            return ImportMassPointsEd
         if inp == 'T' or inp == 't':
            return ImportMassPointsText

@StateInterface.register
class ImportMassPointsEd(StateClass):
   name = "importMassPointsEd"
   allowed = ['copyVolAndPathnodes']
   def exec(self):
      #welcome message
      print("Please use the copy feature for all Triggers that should be interpreted as mass points.")
      print("The Tag corresponds to the mass of the simulated object in kg.")
      print("Confirm with enter after copying.")
      _ = input()
      while True:
         massVolumesText = pc.paste()
         with open('dumpTriggerActors.txt', 'w') as f:
            f.write(massVolumesText)
         # perform analysis --> add mass points to physics
         regex = r"Begin Actor Class=Trigger(?:.|\n)*?Location=\(X=(.*?),Y=(.*?),Z=(.*?)\)(?:.|\n)*?Tag=\"(.*)\""
         matches = re.finditer(regex, massVolumesText, re.MULTILINE)
         for matchNum, match in enumerate(matches, start=1):
            pos = Position(float(match.group(1)),float(match.group(2)),float(match.group(3)))
            mass = float(match.group(4))
            self.physics.addMassPoint(MassPoint(pos,mass))

         return CopyVolAndPathnodes
            
@StateInterface.register
class ImportMassPointsText(StateClass):
   name = "importMassPointsText"
   allowed = ['copyVolAndPathnodes']
   def exec(self):
      #welcome message
      print("not supported yet. going back.")
      return Init

@StateInterface.register
class CopyVolAndPathnodes(StateClass):
   name = "copyVolAndPathnodes"
   allowed = ['performCalc']
   def exec(self):
      # checking validity of mass points
      print("Processed input. Review mass points in plot? Y / N")
      while False:
         inp = input()
         if inp == 'Y' or inp == 'y':
            HelperFunctions.plotMassPoints(self.physics)
            break
         if inp == 'N' or inp == 'n':
            break
      print("Now scelect and copy all ForceVolumes and PathNodes that should be manipulated. Then press enter to continue")
      _ = input()
      inputText = pc.paste()
      res = "lol"
      # filling forceVolumeDict entries
      with open('dumpVolAndPath.txt', 'w') as f:
            f.write(inputText)
      regex  = r"Begin Actor Class=ForceVolume_TA Name=(.+?) (?:.|\n)*?CustomForceDirection=PathNode\'(.*?)\'(?:.|\n)*?Location=\(X=(.*?),Y=(.*?),Z=(.*?)\)"
      matches = re.finditer(regex, inputText, re.MULTILINE)
      for matchNum, match in enumerate(matches, start=1):
         pos = Position(float(match.group(3)),float(match.group(4)),float(match.group(5)))
         pathNodeRef = match.group(2)
         name = match.group(1)
         self.forceVolumeDict[name] = (pos, pathNodeRef)
      HelperFunctions.plotVolumes(self.forceVolumeDict)
      return PerformCalc


@StateInterface.register
class PerformCalc(StateClass):
   name = "performCalc"
   allowed = ['init']
   def exec(self):
      print("Calculating...")
      
      res = "lol"
      #pc.copy(res)
      print("Done. You can now remove the scelected ForceVolumes and Path nodes and paste the newly created items.")
      exit()

class StateMachine(object):
   """ represents the State Machine """
   def __init__(self):
      self.state = Init()
   
   def change(self, state):
      """ Change state """
      self.state.switch(state)