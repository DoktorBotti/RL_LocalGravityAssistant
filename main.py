import pyperclip as pc
import re
import StateMachine 
from Physics import Physics

class ProgramState(object):
    def __init__(self): 
        self.physics = Physics()
        self.forceVolumeList = list()
        self.copiedText = ""

def main():
    print("Welcome to the enhanced gravity modding tool!")
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