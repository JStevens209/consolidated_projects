from __future__ import annotations
from abc import ABC, abstractmethod
from state import *


class Context(ABC):

    
    time = 0
    _state = None

    functionQueue = []
    

    def __init__(self, state: State) ->  None:
        self._state = State_Off()
        self._state._context = self

       


    def  stateCycle(self):
        isOn = True
        while isOn:
          isOn = self._state.stateFunc(self._state)
        
        i = 0
        for i in range(len(self.functionQueue)):
            self.functionQueue[i]()
           
    def doSomething(self):
        print("This did something")

    def doSomethingElse(self):
        print("This did something else")

    def transition_to(self, state: State()):

        self._state = state
        self._state.context = self


    



"""
Concrete States implement various behaviors, associated with a state of the
Context.
"""
if __name__ == "__main__":
    # The client code.
    context = Context(State_Off())
    context.stateCycle()
    




