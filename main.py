import pyperclip as pc
import re
import StateMachine 



def main():
    print("Welcome to the enhanced gravity modding tool!")
    stateMachine = StateMachine.StateMachine()
    while(True):
        nextState = stateMachine.state.exec()
        if nextState != None:
            stateMachine.change(nextState)
        else:
            print('Internal error :(')
            exit()

main()