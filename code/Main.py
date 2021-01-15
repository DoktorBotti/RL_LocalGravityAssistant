import re
import sys
import StateMachine
from Physics import Physics

class ProgramState(object):
    def __init__(self): 
        self.physics = Physics()
        self.forceVolumeList = list()
        self.copiedText = ""

def main():
    if len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == '-h'):
        helpStr = """ Gravity Assistant for Unreal Engine 3:
        This tool allows you to enhance your custom Rocket League maps with complex gravity situations.
        The following components in UDK will be used:
         - Trigger:     Represents a mass point. 
                - TAG:                  Defines the mass in kilograms
                - Collision Height:     Min distance (no effect within this range) 
                - Collision Radius:     Max distance (no effect afterwards)

         - PathNode:    Is used to store the force direction for every ForceVolume. 
                        They must be placed and linked manually!

         - ForceVolume: Used to apply Force on game objects. Place them, where 
                        the the custom gravity should take effect. 
                - ForceMode:            Will be overwritten.
                                        (Set a different mode by supplying the mode name as argument)
                - Custom Force Dir.:    REQUIRES MANUAL ATTACHMENT. Each ForceVolume must have its own attached PathNode
        
        Useful Links:
         YT showcase and tutorial

        How to use this tool:
        1. Create the rough shape of your map with mass points in mind
        2. Place a single ForceVolume and PathNode
        3. Reference the PathNode from the ForceVolume; Group both components. (grouping is useful, not required)
        4. Copy the group to wherever you need custom gravity
                CAUTION: UDK will only handle about ~750 items at once during some steps.
                Make sure, that your groupings are not bigger.
        5. Place and configure your Trigger objects (your mass points)
        6. Scelect all Triggers (i.e. Ctrl+A in the Scenes tab) and copy them to your clipboard
        7. The script will tell you instructions, when to provide the ForceVolumes and PathNodes
        8. PROFIT. Go back to UDK and DELETE the previously selected items, then paste your clipboard. 
           Your ForceVolumes are now completely configured.
        """
        print(helpStr)
        exit()

    stateMachine = StateMachine.StateMachine()
    pState = ProgramState()
    while(True):
        nextState = stateMachine.state.exec(pState)
        if nextState != None:
            stateMachine.change(nextState)
        else:
            print('Internal error :(')
            exit()

main()