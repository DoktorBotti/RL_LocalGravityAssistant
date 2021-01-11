import abc
from StateDependentCode import CalibrateScreenHelper
class StateInterface(abc.ABC):
   @abc.abstractmethod
   def exec(self):
      pass

class ComputerState(object):
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
class Init(ComputerState):
   name = "init"
   allowed = ['calibrateScreen', 'preMassPoints']
   def exec(self):
      #welcome message
      print("Welcome to the Gravity Assistant for Unreal Engine 3. \nThe script assumes that you have already placed the ForceVolumes in your map.")
      print("This includes the attached PathNodes. Also the configured mass points should be positioned as well.\n\nDuring the runtime, please do not interfere, except wen you are told to.")
      print("Do you whish to calibrate your screen? (reccomended)  Y / N")
      while True:
         inp = input()
         if inp == 'Y' or inp == 'y':
            return CalibrateScreen
         if inp == 'N' or inp == 'n':
            return PreMassPoints

@StateInterface.register
class CalibrateScreen(ComputerState):
   """ screen calibration imminent """
   name = "calibrateScreen"
   allowed = ['preMassPoints']

   def exec(self):
      print(f"In state: {self.name}")
      print("Calibration: Click in the top left corner of your leftmost monitor")
      CalibrateScreenHelper.doCalibrationClick()
      return PreMassPoints

@StateInterface.register
class PreMassPoints(ComputerState):
   """ before decision about the mass points is made """
   name = "preMassPoints"
   allowed = ['importMasspoints', 'calibrateMassPoints']
   def exec(self):
      print(f"In state: {self.name}")
      return None

@StateInterface.register
class ImportMasspoints(ComputerState):
   """ User drags file or specifies path, where to find the mass points """
   name = "importMasspoints"
   allowed = ['preMassPoints', 'preForceVolumes']
   def exec(self):
      print(f"In state: {self.name}")
      return None

@StateInterface.register
class CalibrateMassPoints(ComputerState):
   """ calibration process for reading masspoints of the editor """
   name = "calibrateMassPoints"
   allowed = ['preMassPoints', 'grabMasspoints']
   def exec(self):
      print(f"In state: {self.name}")
      return None

@StateInterface.register
class GrabMasspoints(ComputerState):
   """ process for reading masspoints of the editor """
   name = "grabMasspoints"
   allowed = ['preMassPoints', 'grabMasspoints', 'preForceVolumes']
   def exec(self):
      print(f"In state: {self.name}")
      return None

@StateInterface.register
class PreForceVolumes(ComputerState):
   """ before forceVolumes are either read or imported"""
   name = 'preForceVolumes'
   allowed = ['importForceVolumes', 'calibrateForceVolumes']
   def exec(self):
      print(f"In state: {self.name}")
      return None

@StateInterface.register
class ImportForceVolumes(ComputerState):
   """ User drags file or specifies path, where to find the force volume data """
   name = 'importForceVolumes'
   allowed = ['preForceVolumes', 'preRotation']
   def exec(self):
      print(f"In state: {self.name}")
      return None

@StateInterface.register
class CalibrateForceVolumes(ComputerState):
   """ calibration process for reading force volumes of the editor """
   name = 'calibrateForceVolumes'
   allowed = ['preForceVolumes', 'preOverwrRotation']
   def exec(self):
      print(f"In state: {self.name}")
      return None

@StateInterface.register
class PreOverwrRotation(ComputerState):
   """ before rpy values are overwritten """
   name = 'preOverwrRotation'
   allowed = ['calibrateRotation', 'overwriteRoation']
   def exec(self):
      print(f"In state: {self.name}")
      return None

@StateInterface.register
class CalibrateRotation(ComputerState):
   """ calibration process, allowing overwriting Rotational components in the editor """
   name = 'calibrateRotation'
   allowed = ['preOverwrRotation', 'overwriteRoation']
   def exec(self):
      print(f"In state: {self.name}")
      return None

@StateInterface.register
class OverwriteRoation(ComputerState):
   """ overwriting Rotational components in the editor """
   name = 'overwriteRoation'
   allowed = ['end', 'preOverwrRotation']
   def exec(self):
      print(f"In state: {self.name}")
      return None

@StateInterface.register
class End(ComputerState):
    """ Giving final report, maybe storing results and configurations """
    name = 'end'
    allowed = []

    def exec(self):
      print(f"In state: {self.name}, terminating")
      exit()

class StateMachine(object):
   """ represents the State Machine """
   
   def __init__(self):

      self.state = Init()
   
   def change(self, state):
      """ Change state """
      self.state.switch(state)