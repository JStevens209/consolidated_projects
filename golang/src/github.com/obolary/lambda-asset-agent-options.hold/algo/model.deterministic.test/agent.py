import pandas as pd
import numpy as np

import test_gym


#Agent Class
class Agent:
    #holds the current State
    state = None
    #Holds a Gym class Object
    gymPtr = None
    #Holds the current strike price
    strike = 0

    def __init__(self):
        self.gymPtr = Gym()
        
        hold_option, hold_underlying = self.gymPtr.return_held_equity()

        #If you hold neither underlying or option
        if hold_option is False and hold_underlying is False:
            self.state = self.State_Cash

        #if you hold underlying but not option
        if hold_option is False and hold_underlying is True:
            self.state = self.State_Expire

        #if you hold both underlying and option
        if hold_option is True and hold_underlying is True:
            self.state = self.State_Wait
        
        self.Run()


        pass

    
    def Run(self):
       #usually would be a While True statement, but something had to iterate through the index to simulate time passing
        closes = self.gymPtr.test_dataset.C
        for i,c in enumerate(closes):
            self.gymPtr.i = i
            if(self.gymPtr.market_open()):
               self.state()   

        pass

    #Default starting state, 
    def State_Cash(self):
        oom = 5

        self.strike = oom * np.round( ( np.ceil( self.gymPtr.return_underlying_value() + ( oom / 2 ) ) ) / oom )

        delta, gamma, theta, vega, rho = self.gymPtr.return_greeks(self.strike)

        print(theta, vega, rho)
        

        pass

    #Waits for either option expiration, or option excercising
    def State_Wait(self):
        #print("Waiting")
        #if option is excercised
        option, excercised = self.gymPtr.return_option_state()
        if(option is False and excercised is True):
            self.state = self.State_Excercised
        
        #else if it expired
        elif(option is False and excercised is False):
            self.state = self.State_Expire
        
        #if option is excercised
        
        pass
    
    #Determines when the right time to place a call is, using greeks, then goes back to waiting state
    def State_Expire(self):
        pass
    
    #Determines when the right time to place a call is, using greeks, after buying underlying, then goes back to waiting
    def State_Excercised(self):
        pass


if __name__ == "__main__":
    #initializes an object of class Agent, which calls init, starting the program.
    run = Agent()
    