import pandas as pd
import numpy as np
import matplotlib as mlp

import option_pricing

class Gym:
    #Gym methods separated into two types, getters and actions, getters return information, actions act according to the agent

    #variables only used to simulate actual market
    test_dataset = None
    closes = None
    time = None
    hv = None

    call_date = None
    time_to_expire = None
    balance = 0
    
    hold_option = False
    hold_underlying = False

    i = 0
    
    #necessary variables
    strike = 0


    def __init__(self):
        #Parses the gold history csv file into a pd dataset
        file_path = 'lambda-asset-agent-options/algo/models/XAUUSD_1M_ALL.csv'
        delim = ';'
        headers = ["date","O","L","H","C","V"]

        self.test_dataset = pd.read_csv(file_path, delimiter = delim, names = headers, nrows=300000)

        self.test_dataset.date = pd.to_datetime(self.test_dataset.date, format='%Y%m%d %H%M%S')
        self.test_dataset = self.test_dataset.set_index(self.test_dataset.date)
        print("Dataset Parsed")
        
        #Separates two dataset columns out, dataset.C (close prices per min) and the dataset.date (the date of each close)
        self.closes = self.test_dataset.C
        self.time = self.test_dataset.date

        #Historical Volatility Calculations
        daily = self.test_dataset.C.groupby( by=self.test_dataset.date ).apply( lambda x: x[0] )
        daily_days = self.test_dataset.C.groupby( by=self.test_dataset.date ).apply( lambda x: x.index[0] )
        self.hv = daily.pct_change().rolling( 365 ).std() * ( 252 ** 0.5 ) + 0.125
        print("HV Calculated")
        
        pass

    #getters

    #returns what equities are currently held
    def return_held_equity(self):
        return self.hold_option, self.hold_underlying


    def return_option_state(self):
        #print("Option Stated")
        
        #If this strike is less than the current close price, assume the option was excercised
        if self.strike < self.closes[self.i]:

            #print("Excercised")
            self.hold_option = False
            self.hold_underlying = False

            excercised = True
            option = False

        #If the date is after the expiration date, the option expired
        elif self.time[self.i] > self.call_date:

            self.hold_underlying = False

            excercised = False
            option = False
            #print("Expired")

        #Neither happened
        else:
            excercised = False
            option = True
        
        #returns bools on if you still hold the call, if it has expired, or if it has been excercised
        return option, excercised
    
    #returns the current state of the greeks of the placed call
    def return_greeks(self, strike):
        #print("Greeks Returned")
        if self.call_date is not None:
            delta = self.call_date - self.time[self.i]
            self.time_to_expire = delta.days
        else:
            self.time_to_expire = 7

        print("start", self.closes[self.i], strike, self.time_to_expire/365, .01, 0, self.hv[self.i])
        print("")
        call_out = options.american('c',self.closes[self.i], strike, 
                                        self.time_to_expire/365, .01, 0, self.hv[self.i])

        value, delta, gamma, theta, vega, rho = call_out
        

        #return option greeks
        return delta, gamma, theta, vega, rho

    #Returns Historical Volatility
    def return_volatility(self):

        return self.hv[self.i]

    def return_underlying_value(self):
        return self.closes[self.i] 


    #actions

    #Places a call, 
    def place_call(self, strike):
        call_in = None
        #If the date is sometime before friday, or on friday, go for next friday
        if (self.time[self.i].dayofweek + 1) <= 5:

            self.time_to_expire = (self.time[self.i].dayofweek % 4) + 7

            call_in = options.american('c',self.closes[self.i], strike, 
                                        self.time_to_expire/365, .01, 0, self.hv[self.i])
            
            self.balance -= call_in[0]
            self.hold_option = True

            self.call_date = self.closes.index[self.i] + pd.Timedelta(self.time_to_expire, "days")
        else:
            #This function should not be called weekends, due to trading hours
            print("ERROR: Trade occured on weekend")
            

        #print(self.call_date)
        return call_in

    #buys the underlying, returns the cost
    def buy_underlying(self):
        self.balance -= self.closes[self.i]

        self.hold_underlying = True

        pass
    
    #checks if the market is open
    def market_open(self):
        if self.time[self.i].dayofweek not in range(5,7): #{
            if self.time[self.i].hour in range(10,16):
                return True
