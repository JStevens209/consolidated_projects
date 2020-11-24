import numpy as np
import pandas as pd
import datetime

import matplotlib as mlp
from matplotlib import pylab as plt

from absl import logging
import random

from td_gym_env_mock import *

opening_price = 0
closing_price = 0


# This function just brute forces every single possible state the action could concievably be in to test for missed bugs
def brute_force_actions( ):
    action = { 'kind':  'hold' }

    random.seed()

    kind = [ 'hold', 'open', 'close', '' ]
    extrinsic = [ 'sell', 'buy', '' ]
    intrinsic = [ 'excercise', 'expire', '' ]

    option_kind = [ 'c', 'p', '' ]
    
    equity = action[ 'equity' ]
    option = action[ 'option' ]

    # Random date gen code I stole from somewhere
    start_date = datetime.date(2009, 3, 15)
    end_date = datetime.date(2018, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange( days_between_dates )

    action[ 'kind' ] = kind[ random.getrandbits( 5 ) % 3 ]
    action[ 'extrinsic' ] = extrinsic[ random.getrandbits( 5 ) % 2 ]
    action[ 'intrinsic' ] = intrinsic[ random.getrandbits( 5 ) % 2 ]

    equity[ 'lots' ] = ( random.getrandbits( 5 ) % 200 ) - 100

    option[ 'kind' ] =  option_kind[ random.getrandbits( 5 ) % 2 ]
    option[ 'lots' ] = ( random.getrandbits( 5 ) % 200 ) - 100
    option[ 'strike' ] = ( random.getrandbits( 5 ) % 1000 )

    option[ 'date' ] = start_date + datetime.timedelta( days=random_number_of_days )
    option[ 'days' ] = ( random_number_of_days )

    action[ 'option' ] = option
    action[ 'equity' ] = equity

    return action

#U
def simulate_basic_equity_trades( state ):
    action = { 'kind':  'hold' }

    curr_equity = state[ 'equity' ]
    new_equity  = {}

    scenario_make_money = True
    scenario_lose_money = False
    scenario_short_equity = False

    if curr_equity[ 'cost' ] > 0:
        percent_itm = ((curr_equity[ 'price' ] - curr_equity[ 'cost' ]) / curr_equity[ 'price' ] ) * 100
    else:
        percent_itm = 100

    if ( curr_equity[ 'lots' ] == 0 ) and ( scenario_lose_money or scenario_make_money ):
        action[ 'kind' ] = 'open'
        action[ 'extrinsic' ] = 'buy'
        new_equity[ 'lots' ] = 1

    elif curr_equity[ 'lots' ] == 0 and scenario_short_equity:
        action[ 'kind' ] = 'open'
        action[ 'extrinsic' ] = 'sell'
        new_equity[ 'lots' ] = 1
        
    elif percent_itm > 0 and scenario_make_money:
        action[ 'kind' ] = 'close'
        action[ 'extrinsic' ] = 'sell'
        new_equity[ 'lots' ] = 1
    
    elif percent_itm < 0 and scenario_lose_money:
        action[ 'kind' ] = 'close'
        action[ 'extrinsic' ] = 'sell'
        new_equity[ 'lots' ] = 1

    elif percent_itm < 0 and scenario_short_equity:
        action[ 'kind' ] = 'close'
        action[ 'extrinsic' ] = 'buy'
        new_equity[ 'lots' ] = 1
        
    else:
        action[ 'kind' ] = 'hold'

    if new_equity:
        action[ 'equity' ] = new_equity

    return action


def simulate_basic_option_trades( state, expire_date ):
    action = { 'kind':  'hold' }

    option = state[ 'option' ]
    equity = state[ 'equity' ]
    new_option = {}
    new_equity = {}

    long_call = True
    short_put = False

    if equity[ 'lots' ] > 0 and long_call:
        action[ 'kind' ] = 'close'
        action[ 'extrinsic' ] = 'sell'
        new_equity[ 'lots' ] = equity[ 'lots' ]
    
    elif option[ 'lots' ] == 0 and long_call:
        action[ 'kind' ] = 'open'
        action[ 'extrinsic' ] = 'buy'
        
        new_option[ 'kind' ] = 'c'
        new_option[ 'lots' ] = 1
        new_option[ 'strike' ] = equity[ 'price' ] + 2
        new_option[ 'date' ] = expire_date

    elif equity[ 'lots' ] > 0 and option[ 'price' ] - option[ 'cost' ] > 0 and short_put:
        action[ 'kind' ] = 'close'
        action[ 'extrinsic' ] = 'sell'
        new_equity[ 'lots' ] = equity[ 'lots' ]

    elif option[ 'lots' ] == 0 and short_put:
        action[ 'kind' ] = 'open'
        action[ 'extrinsic' ] = 'sell'
        
        new_option[ 'kind' ] = 'p'
        new_option[ 'lots' ] = 1
        new_option[ 'strike' ] = equity[ 'price' ] - 2
        new_option[ 'date' ] = expire_date

    else:
        action[ 'kind' ] = 'hold'
    
    if new_equity:
        action[ 'equity' ] = new_equity
    if new_option:
        action[ 'option' ] = new_option
    return action

def simulate_covered_call( state, expire_date ):
    action = { 'kind':  'hold' }

    option = state[ 'option' ]
    equity = state[ 'equity' ]
    action_option = {}
    action_equity = {}

    if equity[ 'lots' ] < 10:
        action[ 'kind' ] = 'open'
        action[ 'extrinsic' ] = 'buy'

        action_equity[ 'lots' ] = 10 - equity[ 'lots' ]

    elif option[ 'lots' ] == 0:
        action[ 'kind' ] = 'open'
        action[ 'extrinsic' ] = 'sell'

        action_option[ 'lots' ] = 10
        action_option[ 'kind' ] = 'c'
        action_option[ 'strike' ] = equity[ 'price' ] + 5
        action_option[ 'date' ] = expire_date

    else:
        action[ 'kind' ] = 'hold'

    if action_option:
        action[ 'option' ] = action_option
    if action_equity:
        action[ 'equity' ] = action_equity

    return action

# Expiration date needs to be relative to the Gym's current date
def get_expiration_date( GymTest, state ):
    date = GymTest.dataset.C.index[ state[ 'index' ] ]
    delta = pd.Timedelta( '7 days' )
    expire_date = date + delta

    return expire_date

if __name__ == "__main__":

    #logging.set_verbosity( logging.INFO )
    
    GymTest = TDGymEnvMock('GLD', '/Users/joshua/source/golang/src/github.com/obolary/lambda-asset-corpus/ALL/XAUUSD_1M_ALL.csv', 1)
    balances = []
    costs = []
    prices = []
    strikes = []
    done = False
    action = { 'kind': 'hold' }

    for i in range( 100000 ): #while not done:
        observation, r, done, _ = GymTest.step( action )
        expire_date = get_expiration_date( GymTest, observation )
        action = simulate_basic_equity_trades( observation )
        #action = brute_force_actions( action )
        #action = simulate_basic_option_trades( observation, expire_date )
        #action = simulate_covered_call( observation, expire_date )
        
        balances.append( observation[ 'balance' ] )
        #strikes.append( observation[ 'option' ][ 'strike' ])
        #costs.append( observation[ 'equity' ][ 'cost' ])
        #prices.append( observation[ 'equity' ][ 'price' ])
    
    #plt.plot( costs ) 
    #plt.plot( prices)
    #plt.plot( strikes )
    plt.plot( balances )
    plt.show()
    

