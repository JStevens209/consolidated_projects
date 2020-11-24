from __future__ import annotations
from abc import ABC, abstractmethod
import time as tm

class State(ABC):

    _context = None
    sleepTime = .1
    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def stateFunc(self, time = 0):
        pass


class State_Off(State):

    def stateFunc(self, time = 0):
        answer = input("Turn On? y/N \n")

        if answer == "y":
            self._context.transition_to(State_Idle())
            return True
        else:
            self._context.transition_to(State_Off())
            return False

        

class State_Idle(State):
    
    def stateFunc(self, time=0):
        answer = input("Waiting For Input \n")

        if answer == "start":
            print("Button Pushed, cycle started.")
            self._context.transition_to(State_Rinse())

        elif answer == "off":
            self._context.transition_to(State_Off())

        else:
            self._context.transition_to(State_Idle())
        
        return True
    
    
   

class State_Rinse(State):

    def stateFunc(self, time=0):
        print("Rinsing", end = '', flush = True)

        i = 0
        while i < 3:
            tm.sleep(self.sleepTime)
            print(".", end = '', flush = True)
            i += 1
        print("")

        if self._context.time == 0:
            self._context.transition_to(State_Wash())

        elif self._context.time == 1:
            self._context.transition_to(State_Dry())
        
        return True




class State_Wash(State):

    def stateFunc(self, time=0):  
        print("Washing", end = '', flush = True)

        i = 0
        while i < 3:
            tm.sleep(self.sleepTime)
            print(".", end = '', flush = True)
            i += 1
        print("")

        self._context.time = 1
        self._context.transition_to(State_Rinse())

        self._context.functionQueue.append(self._context.doSomething)
        self._context.functionQueue.append(self._context.doSomethingElse)

        return True

    
class State_Dry(State):

    def stateFunc(self, time=0):
        print("Drying", end = '', flush = True)
        
        i = 0
        while i < 3:
            tm.sleep(self.sleepTime)
            print(".", end = '', flush = True)
            i += 1
        print("")
        print("Done!")

        self._context.transition_to(State_Idle())
        return True

