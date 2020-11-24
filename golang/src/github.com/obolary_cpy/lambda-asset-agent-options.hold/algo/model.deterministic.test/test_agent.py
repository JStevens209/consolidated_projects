# ICSIII - moved from old gym_tdameritrade
import pandas as pd
import numpy as np

import gym


#Agent Class
class Agent:
    #holds the current State
    state = None
    #Holds a Gym class Object
    gym = None
    #Holds the current strike price
    strike = 0

    action = 'hold'

    done = False

    def __init__(self):

        self.gym = gym.make( 
            'td_gym:td-gym-test-v0', 
            dataset_filepath='../../../lambda-asset-corpus/ALL/XAUUSD_1M_ALL.csv' 
        )

        self.gym = TDAmeritradeEnv()
        
        holdings, r, done = self.gym.step('hold')

        if holdings['hold_option'] and holdings['hold_underlying']:
            self.state = self.State_Wait
        
        if not holdings['hold_option'] and holdings['hold_underlying']:
            self.state = self.State_Expire
        
        if not holdings['hold_option'] and not holdings['hold_underlying']:
            self.state = self.State_Cash
        
        else:
            print("Error: Bad State Information")
    
        self.Run()

        pass

    
    def Run(self):
       #usually would be a While True statement, but something had to iterate through the index to simulate time passing
        while not self.done:
            state, r, self.done = self.gym.step(self.action)
            if self.done:
                break
            if state['market_open'] is True:
                self.state(state)
        
        pass

    #Default starting state, 
    def State_Cash(self, state):
        self.action = 'place_covered_call'

        self.state = self.State_Wait
        pass

    #Waits for either option expiration, or option excercising
    def State_Wait(self, state):
        #dont do anything
        self.action = 'hold'
        #if option is excercised
        if not state['hold_option'] and not state['hold_underlying']:
            self.state = self.State_Excercised
        #if option is excercised
        if not state['hold_option'] and state['hold_underlying']:
            self.state = self.State_Expire
        pass
    
    #Determines when the right time to place a call is, using greeks, then goes back to waiting state
    def State_Expire(self, state):
        if state['hv'] < .3:
            self.action = 'place_call'
            self.state = self.State_Wait
        pass
    
    #Determines when the right time to place a call is, using greeks, after buying underlying, then goes back to waiting
    def State_Excercised(self, state):
        if state['hv'] < .3:
            self.action = 'place_covered_call'
            self.state = self.State_Wait
        pass


if __name__ == "__main__":
    #initializes an object of class Agent, which calls init, starting the program.
    run = Agent()