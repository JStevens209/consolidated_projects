import gym
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pylab as plt

from gym import error, spaces, utils
from gym.utils import seeding

import option_pricing

class TDGymEnvTest( gym.Env ):

    metadata = { 'render.modes': [ 'human' ] }

    close = None
    date  = None
    hv    = None

    num_features = 5

    self.min_state = np.full( num_features, -np.finfo(np.float32).max ) 
    self.max_state = np.full( num_features, +np.finfo(np.float32).max )

    self.observation_space = spaces.Box( low=self.min_state, high=self.max_state, dtype=np.float32 )

    balance = [960]
    profit  = 0
    cost = 0
    lots = 100

    have_underlying = False
    have_option     = False

    strike    = 960
    call_date = None
    time_to_expire = 7
    call_value = 0
    i = 0

    oom = 10

    def __init__(self, dataset_filepath, **kwargs):

        #Default Values Override
        self.__dict__.update(**kwargs)

        #parse dataset
        file_path = dataset_filepath
        delim = ';'
        headers = ["date","O","L","H","C","V"]

        dataset = pd.read_csv(file_path, delimiter = delim, names = headers, nrows=300000)

        dataset.date = pd.to_datetime(dataset.date, format='%Y%m%d %H%M%S')
        dataset = dataset.set_index(dataset.date)
        print("Dataset Parsed")
        
        #Separates two dataset columns out, dataset.C (close prices per min) and the dataset.date (the date of each close)
        self.close = dataset.C
        self.date  = dataset.C.index

        #Historical Volatility Calculations
        daily = self.close.groupby( by=self.date ).apply( lambda x: x[0] )
        daily_days = self.close.groupby( by=self.date ).apply( lambda x: x.index[0] )
        self.hv = daily.pct_change().rolling( 365 ).std() * ( 252 ** 0.5 ) + 0.125
        print("HV Calculated")

        self.queue = None
        pass

    def step(self, action):
        #advance the index
        self.i += 1

        if self.i >= len(self.close.index):
            self.render()
            done = True
            s = None
            r = 0
            return s, r, done

        #perform action
        if action is "hold":
            #do nothing
            pass

        if action is "place_call":
            #calculate strike
            self.strike = self.oom * np.round( np.ceil( self.close[self.i] + self.oom ) / self.oom )
            #calculate how long till the option will expire
            self.time_to_expire = (self.date[self.i].dayofweek % 4) + 7

            #place the call
            call_in = self.options_american()
            self.call_value = call_in[0]

            self.call_date = self.date[self.i]
            self.have_option = True

            self.cost = 0
            pass

        if action is "place_covered_call":
            #calculate strike
            self.strike = self.oom * np.round( np.ceil( self.close[self.i] + self.oom ) / self.oom ) 
            #calculate time till call expires
            self.time_to_expire = (self.date[self.i].dayofweek % 4) + 7
           
            #sell call
            call_in = self.options_american()
            self.call_value = call_in[0]

            self.call_date = self.date[self.i]
            self.have_underlying = True

            #buy underlying
            cost = self.close[self.i] * 100 * self.lots
            self.have_underlying = True

            pass
            

        #get the state
        s, done = self._state( action )
        r = self._reward()

        #return
        return s, r, done

    def reset(self):
        self.close = None
        self.date  = None
        self.hv    = None

        self.balance = [960]
        self.profit  = 0

        self.have_underlying = False
        self.have_option     = False

        self.strike    = 960
        self.call_date = None
        self.time_to_expire = 7
        self.i = 0

        s, _ = self._state( action = 0 )
        return s

    def render(self, mode='human'):
        plt.plot(self.balance)
        plt.show()
        pass

    def close(self):

        pass

    def _state(self,action):
        
        #check the state of the options currently
        if self.call_date is not None:

            delta = self.call_date - self.date[self.i]
            self.time_to_expire = delta.days

            #if option was excercised
            self.profit = 0

            if self.strike < self.close[self.i]:
                
                call_in = self.options_american()

                #realize the loss between the strike price, and the underlying's current value
                self.profit -= self.close[self.i] - self.strike
                #add the difference between the cost of the underlying, and its current value
                self.profit += self.close[self.i] - self.cost 
                #subtract comission
                self.profit -= 2 * .65 * (self.lots/100)
                #add the value of the premium
                self.profit += self.call_value * self.lots
                #subtract spread
                self.profit -= .05 * self.lots
                #subtract the closing value of the call
                self.profit -= call_in[0]
                #if underlying was bought, subtract the cost
                self.profit -= self.cost

                self.have_option = False
                self.have_underlying = False
            
            #if option expired
            elif self.date[self.i] > self.call_date:
                #add option premium
                self.profit += self.call_value * self.lots
                #subtract commission
                self.profit -= 2 * .65 * (self.lots/100)
                #subtract spread (still dont get it)
                self.profit -= .05 * self.lots
                #subtract cost of underlying
                self.profit -= self.cost

                self.have_option = False
                
        self.balance.append(self.profit)

        #dict filled with current state information
        states = {
                     "hold_option":False,  
                     "option_price":0, 
                     "hold_underlying":False, 
                     "underlying_price":0, 
                     "greeks":None,
                     "strike":0,
                     "market_open":False, 
                     "hv":0                    
                }

        #set all dictionary values
        states['underlying_price'], states['option_price'] = self.get_prices()

        states['greeks'] = self.get_greeks()

        states['hold_option'] = self.have_option

        states['hold_underlying'] = self.have_underlying

        states['strike'] = self.strike

        states['market_open'] = self.market_open()
        
        states['hv'] = self.hv[self.i]

        #return dictionary
        return states, False


    def _reward( self) :

        return 0.0 

    def get_prices(self):
        
        call_in = self.options_american()
        option_price = call_in[0]

        underlying_price = self.close[self.i]

        return underlying_price, option_price

    def get_greeks(self):
        value, delta, gamma, theta, vega, rho = self.options_american()
        greeks = { 
                    'delta':delta, 
                    'gamma':gamma, 
                    'theta':theta, 
                    'vega':vega, 
                    'rho':rho 
                }

        return greeks

    def market_open(self):
        if self.date[self.i].dayofweek not in range(5,7): 
            if self.date[self.i].hour in range(10,16):
                return True
        else:
            return False

    #This function was used so much, I simplified it
    def options_american(self):
        if self.time_to_expire <= 0:
            self.time_to_expire = 7
        
        call_in = options.american( 'c', self.close[self.i], self.strike, self.time_to_expire/365, 0.01, 0.0, self.hv[self.i] )
        return call_in


  #Convienience thing so I can start the program from either file  
if __name__ == "__main__":
    test = Agent()
    pass