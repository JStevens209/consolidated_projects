import gym
import pandas as pd
import numpy as np
import math
import collections
import datetime
import copy

import matplotlib
import matplotlib.pyplot as plt

import option_pricing.option_pricing as options

from absl import logging

from gym import error, spaces, utils
from gym.utils import seeding  

class TDGymEnvMock( gym.Env ):

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # OpenAI Gym Mock TD-Ameritrade

    # initialize environment
    def __init__( self, dataset_underlying, dataset_file, dataset_multiplier, **kwargs ):
        logging.info( '** initializing gym, TDGymEnvMock,...' )

        # set constants and allow overrides
        self.equity_spread = 0.01
        self.option_spread = 0.05
        self.option_commission = 0.65
        self.account_balance = 100000.0
        self.hist_vol_offset = 0.125
        self.__dict__.update( **kwargs )

        # set parameters
        self.underlying = dataset_underlying
        self.underlying_multiplier = dataset_multiplier

        num_features = 5

        self.min_state = np.full( num_features, -np.finfo(np.float32).max ) 
        self.max_state = np.full( num_features, +np.finfo(np.float32).max )

        self.observation_space = spaces.Box( low=self.min_state, high=self.max_state, dtype=np.float32 )

        # read simulation dataset
        dataset_headers = [ 'date-time','O','H','L','C','V' ]
        dataset_dtype = 'float32'
        dataset_dtypes = { 
            'O': dataset_dtype, 
            'H': dataset_dtype,
            'L': dataset_dtype,
            'C': dataset_dtype,
            'V': 'int32'
        }
        dataset_sep = ';'

        self.dataset = pd.read_csv( 
            dataset_file, 
            sep = dataset_sep, 
            names = dataset_headers,
            dtype = dataset_dtypes 
        )

        # reset prices, volumes and index 
        self.dataset['O'] = self.dataset['O'] * self.underlying_multiplier
        self.dataset['C'] = self.dataset['C'] * self.underlying_multiplier
        self.dataset['H'] = self.dataset['H'] * self.underlying_multiplier
        self.dataset['L'] = self.dataset['L'] * self.underlying_multiplier
        self.dataset['date-time'] = pd.to_datetime( self.dataset['date-time'], format='%Y%m%d %H%M%S')
        self.dataset = self.dataset.set_index( ['date-time'] )
        
        # calc historical volatility
        close = self.dataset['C']
        daily = close.groupby( by=close.index.date ).apply( lambda x: x[0] )
        self.hv = daily.pct_change().rolling( 365 ).std() * ( 252 ** 0.5 ) + self.hist_vol_offset
        self.hv[0:365] = np.arange( start=0.2, stop=self.hv[365], step=(self.hv[365]-0.2)/365 )

        # Informal workaround so that engine does not have to work around dates
        self.date = self.dataset.index[0]

        # reset state
        _ = self.reset()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # OpenAI Gym Interface Implementation

    # reset environment state
    def reset( self ):
        logging.info( '** gym reset,...' )

        # reset all run-time state attributes
        self.state = {

            # current tick within the dateset
            'index': 0,

            # initial balance of the account
            'balance': self.account_balance,

            # equity position (only one type, but many lots)
            # note, the lots are in multiples of 100, negative means we've shorted, 
            #       and the cost is bid and price is ask. lots positive have the reverse
            'equity': {
                'lots': 0,
                'cost': 0.0,
                'price': 0.0
            },

            # option position (only one type, but many lots)
            # note, the lots are in number of contracts, negative means we've shorted
            #       and the cost is bid and price is ask. lots positive have the reverse
            # for option[ 'kind' ] 1 is a call, 0 is a put
            'option': {
                'kind': 1,
                'lots': 0,
                'cost': 0.0,
                'strike': 0.0,
#                'date': '2020-01-01',
                'days': 0,
                'price': 0.0
            }
        }

        # return reset state
        return self.state.copy()

    # provide the state of the system after the given action is applied
    def step( self, action ):
        # update to current time
        done = self._tick()

        # take snapshot of state after applying action
        s0 = self.state.copy()
        s1 = self._state( action )

        # determine rewards from applied action
        r = self._reward( s0, s1 )

        # return results
        return s1.copy(), r, done, {}

    # render any optional output
    def render( self, mode='human' ):

        pass

    # close any system resources (e.g., files, etc.)
    def close( self ):

        pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Private Gym Behavior

    # _tick determines the state of the index
    def _tick( self ):

        # bump iteration index
        self.state[ 'index' ] += 1
        self.date = self.dataset.index[ self.state[ 'index' ] ]

        # determine if this is the last tick. note, both the
        # _state and _reward function must be allowed to index 
        # into the dataset using this index even when done is true.
        done = False
        if self.state[ 'index' ] + 1 >= self.dataset[ 'C' ].size:
            done = True
        
        #protects from the gym from over indexing 
        elif self.state[ 'index' ] >= self.dataset[ 'C' ].size:
            done = True
            self.state[ 'index' ] = self.dataset[ 'C' ].size


        # return done
        return done

    # _state determines the state of the account
    # action = {
    #   'kind': [ 'hold', 'open', 'close' ]
    #   [ 'extrinsic': [ 'sell', 'buy' ] ]+
    #   [ 'intrinsic': [ 'exercise', 'expire' ] ]+
    #   [
    #     'equity': {
    #       'lots': 0,
    #       # No limit orders
    #     },
    #   ]+
    #   [
    #     'option': {
                    #'c','p'
    #       'kind': [ 1, 0 ],
    #       'lots': 0,
    #       'strike': 0.0,
    #       'date': '2020-01-01',
    #       'days': 0,
    #       # No limit orders
    #     }
    #   ]+ 
    # }
    def _state( self, action ):

        # Checks for an edge case where the agent did not give an action
        if action != None:
            # determine new prices and expire days, etc
            self._state_apply_intrinsic_state()

            # determine any brokerage actions
            action = self._state_determine_intrinsic_action( action )

            # apply action to state
            self._state_apply_action( action )

        else:
            logging.info( '** Error: Agent did not return an action' ) 
            return self.state

        # return updated state
        return self.state

    # _reward is usually needed to train models that use 
    # reinforcement learning (e.g., A2C, Q, etc.)
    def _reward( self, s0, s1 ) :
        # for example; a simple profit based reward
        return s1[ 'balance' ] - s0[ 'balance' ] 

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Private Gym State x Action Behavior

    # _state_apply_intrinsic_state updates the state using information
    # from the brokerage, e.g., prices, expiration days, etc.
    def _state_apply_intrinsic_state( self ):
        
        # apply the new prices and expiration days
        index = self.state[ 'index' ]
        close = self.dataset[ 'C' ][ index ]
        now = self.dataset[ 'C' ].index[ index ]


        # update current equity price
        equity = self.state[ 'equity' ]
        equity[ 'price' ] = close

        # update current option price and days-to-expire
        option = self.state[ 'option' ]

        # apply days-to-expire and price
        if option[ 'lots' ] != 0:
            option[ 'days' ] = ( pd.to_datetime( self.date ) - now ).days
            option[ 'price' ] = self.get_option_price()

        # update account balance
        self.state[ 'balance' ] = self.account_balance

        self.state[ 'option' ] = option

    # _state_determine_intrinsic_action determines actions normally 
    # performed by the brokerage
    def _state_determine_intrinsic_action( self, action ):
        keys = action.keys()
        
        # determine expirations or exercises
        option = self.state[ 'option' ]
        equity = self.state[ 'equity' ]
        strike = option[ 'strike' ]
        kind = option[ 'kind' ]

        ITM = False
        percent_ITM = 0

        # Check if any option has been placed
        if option[ 'lots' ] != 0:

            if kind == 0 and strike > equity[ 'price' ]:
                ITM = True
                percent_ITM = (( option[ 'strike' ] - equity[ 'price' ] ) / option[ 'strike' ] ) * 100

            if kind == 1 and strike < equity[ 'price' ]:
                ITM = True
                percent_ITM = (( equity[ 'price' ] - option[ 'strike' ] ) / option[ 'strike' ] ) * 100

            # If the agent tries to do the broker's job by expiring the option, log an error
            if 'intrinsic' in keys and action[ 'intrinsic' ] == 'expire':
                logging.info( '** Logic Error: Agent tried to expire option.' )
                action[ 'intrinsic' ] = ' '

            # If the option is about to expire, but it is ITM, excercise it
            elif ITM and option[ 'days' ] <= 0:
                action[ 'intrinsic' ] = 'excercise'

            # If the option is expiring, expire it
            # Days is calculated beforehand in the previous function call
            elif option[ 'days' ] <= 0:
                action[ 'intrinsic' ] = 'expire'

        return action

    # _state_apply_action are performed by the agent, but may also
    # conflict with actions to be performed by the brokerage, this function
    # avoids performing those action twice, and updates the state accordingly
    def _state_apply_action( self, action ):

        option = self.state[ 'option' ]
        equity = self.state[ 'equity' ]
        kind = option[ 'kind' ]

        valid_option_order = False

        keys = action.keys()
        
        if ( 'intrinsic' in keys ):

            qualified_actions = [
            # { c/p, expire/excercise, action }
                [ 1, 'expire', self.expire ],  
                [ 1, 'excercise', self.call_excercise ],           
                [ 0, 'expire', self.expire ],          
                [ 0, 'excercise', self.put_excercise ],    
            ]      

            current_state = [ kind, action['intrinsic'] ]
                    
            # Iterates through the table and tests if the state_array is equal to any of table arrays
            # If the state_array is equal, call that array's function
            for actions in qualified_actions:
                if current_state == actions[0:2]:
                    actions[ 2 ]()

        if 'extrinsic' in keys:
            # if there was a buy or sell
            # check if the action was already performed,
            # then update the state appropriately
            if 'option' in keys and action[ 'kind' ] == 'open':
            # Check if the order that the action is giving is valid, given the current state
                option_shorted     = False
                action_shorting    = False

                # If lots is negative, the option was shorted, if it is positive the option was longed
                if option[ 'lots' ] < 0:
                    option_shorted = True

                # selling_to_open is the same thing as a short, 
                if action[ 'extrinsic' ] == 'sell' and action[ 'kind' ] == 'open':
                    action_shorting = True
  
                #               [ days, strike, kind, true/false (Shorting or not) ]
                action_option = [ action[ 'option' ][ 'date' ], action[ 'option' ][ 'strike' ], action[ 'option' ][ 'kind' ], action_shorting ]
                state_option  = [ self.date, option[ 'strike' ], option[ 'kind' ], option_shorted ]
        
                # The action is giving a valid option order, when either there is no active option, 
                # or the strike price, type, expiration time, and  of the option are all the same
                 # or if the order is only closing, and not opening
                if option[ 'lots' ] == 0 or action[ 'option' ][ 'lots' ] == 0 or action_option == state_option or action[ 'kind' ] == 'close':
                    valid_option_order = True
            else:
                valid_option_order = True

            qualified_actions = [
            # { open/close/hold, buy/sell, valid_option, action }
                [ 'hold', '', '', None ],
                ['open', 'buy', True, self.buy_to_open ],
                [ 'open', 'buy', False, 'log_error' ],
                [ 'open', 'sell', True, self.sell_to_open ],
                [ 'open', 'sell', False, 'log_error' ],
                [ 'close', 'buy', True, self.buy_to_close ],
                [ 'close', 'sell', True, self.sell_to_close ],
            ]

            current_state = [ action[ 'kind' ], action[ 'extrinsic' ], valid_option_order ]

            # Checks current_state against each qualified action, if it matches any, do that action
            for actions in qualified_actions:
                if current_state == actions[0:3]:
                    if actions[3] == 'log_error':
                        logging.info( '** Logic Error: Agent passed Invalid option order. ' )
                    else:
                        actions[3]( action )

        # return the option and equity states back to state
        self.state[ 'option' ] = option
        self.state[ 'equity' ] = equity

        pass

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Private Functions for the purpose of simplifying calculations in _state_apply_action
#
    def expire( self ):
        option = self.state[ 'option' ]

        if option[ 'lots' ] > 0:
            # Realize loss from commission, spread, and original cost
            self.account_balance -= option[ 'cost' ] * option[ 'lots' ] * 100 - (self.option_commission * 2 + self.option_spread) * option[ 'lots' ]

        if option[ 'lots' ] < 0:
            self.account_balance += option[ 'cost' ] * abs( option[ 'lots' ] ) * 100 - (self.option_commission * 2 + self.option_spread) * abs( option[ 'lots' ] )

        # An option that expires is now worthless
        option[ 'cost' ] = 0
        option[ 'lots' ] = 0

        self.state[ 'option' ] = option
        return
        
    def call_excercise( self ):
        option = self.state[ 'option' ]
        equity = self.state[ 'equity' ]

        # If a call that was long was excercised, calculate temporary loss, and gain in equity
        if option[ 'lots' ] > 0:
            equity[ 'lots' ] += option[ 'lots' ]
            equity[ 'cost' ] = option[ 'strike' ]
            self.account_balance -= option[ 'cost' ] * option[ 'lots' ] * 100 - (self.option_commission * 2 + self.option_spread) * option[ 'lots' ]


        # If a short call was excercised before expire date, lost equity for less than market value, also need to close out the trade    
        if option[ 'lots' ] < 0:
            self.account_balance += (( option[ 'strike' ] - equity[ 'cost' ] ) * 100 * abs( option[ 'lots' ] )) - ( self.equity_spread * 100 * abs( option[ 'lots' ] ))
            equity[ 'lots' ] -= abs ( option[ 'lots' ] )

            self.account_balance += ( option[ 'cost' ] - option[ 'price' ] ) * abs( option[ 'lots' ] ) * 100 - (self.option_commission * 2 + self.option_spread) * abs( option[ 'lots' ] )

        option[ 'lots' ] = 0

        self.state[ 'option' ] = option
        self.state[ 'equity' ] = equity

        return

    def put_excercise( self ):
        #print( 'excercisec' )
        option = self.state[ 'option' ]
        equity = self.state[ 'equity' ]

        # If a put that was long was excercised, lose equity, gain strike price amount of money
        if option[ 'lots' ] > 0:
            equity[ 'lots' ] -= option[ 'lots' ]
            self.account_balance += option[ 'strike' ] * option[ 'lots' ] * 100
            self.account_balance -= option[ 'cost' ]  * option[ 'lots' ] * 100 - (self.option_commission * 2 + self.option_spread) * option[ 'lots' ]

        # If a put that was short was excercised, gain equity, lose strike price amount of money
        if option[ 'lots' ] < 0:
            equity[ 'lots' ] += abs( option[ 'lots' ] )
            self.account_balance += ( option[ 'cost' ] - option[ 'price' ] ) * abs( option[ 'lots' ] ) * 100 - (self.option_commission * 2 + self.option_spread) * option[ 'lots' ]

            # Add Comments
            if equity[ 'lots' ] > 0:
                equity[ 'cost' ] = ( equity[ 'cost' ] + option[ 'strike' ] ) / 2

            elif equity[ 'lots' ] == 0:
                equity[ 'cost' ] = option[ 'strike' ]

            elif equity[ 'lots' ] < 0:
                self.account_balance += (( equity[ 'cost' ] - equity[ 'price' ] ) * 100 * abs( option[ 'lots' ] )) - ( self.equity_spread * 100 * abs( option[ 'lots' ] ))

        option[ 'lots' ] = 0

        self.state[ 'option' ] = option
        self.state[ 'equity' ] = equity

        return

    def buy_to_open( self, action ):
        equity = self.state[ 'equity' ]
        option = self.state[ 'option' ]

        keys = action.keys()

        #Handly equity buying
        if 'equity' in keys:
            
            action_equity = action[ 'equity' ]

            # Checks for pre-existing equity contracts, takes the average cost if so, takes the cost if not
            if equity[ 'lots' ] > action_equity[ 'lots' ]:
                equity[ 'cost' ] = ( equity[ 'price' ] + equity[ 'cost' ] ) / 2
            else:
                equity[ 'cost' ] = equity[ 'price' ]  
            equity[ 'lots' ] += action_equity[ 'lots' ]
                
        #Handle option buying
        if 'option' in keys:
            
            action_option = action[ 'option' ]
            curr_time = self.dataset.C.index[ self.state[ 'index' ] ]

            # Copies the action option's terms over to the current option to handle default states
            option[ 'lots' ]  += action_option[ 'lots' ]
            option[ 'kind' ]   = action_option[ 'kind' ]
            option[ 'strike' ] = action_option[ 'strike' ]
            self.date   = action_option[ 'date' ]
            option[ 'days' ]   = ( pd.to_datetime( action_option[ 'date' ], format= '%Y-%m-%d' ) - curr_time ).days

            self.state[ 'option' ] = option

            # Checks for pre-existing option contracts, takes the average cost if so, takes the cost if not
            if option[ 'lots' ] > action_option[ 'lots' ]:
                option[ 'cost' ]   = ( option[ 'cost' ] + self.get_option_price() ) / 2
            else:
                option[ 'cost' ] = self.get_option_price()
            
        self.state[ 'equity' ] = equity
        self.state[ 'option' ] = option

        return

    def sell_to_open( self, action ):
        equity = self.state[ 'equity' ]
        option = self.state[ 'option' ]

        keys = action.keys()

        #Handle Shorting Equity
        if 'equity' in keys:
            
            action_equity = action[ 'equity' ]

            # Checks for pre-existing equity contracts, takes the average cost if so, takes the cost if not
            if equity[ 'lots' ] != 0:
                equity[ 'cost' ] = ( equity[ 'price' ] + equity[ 'cost' ] ) / 2
            else:
                equity[ 'cost' ] = equity[ 'price' ]
            equity[ 'lots' ] -= action_equity[ 'lots' ]
        
        #Handle Shorting Options
        if 'option' in keys:

            action_option = action[ 'option' ]
            curr_time = self.dataset.C.index[ self.state[ 'index' ] ]

            # Only allows the selling of calls to be covered by equity
            if option[ 'lots' ] <= equity[ 'lots' ]:
                # Copies the action option's terms over to the current option to handle default states
                option[ 'lots' ] -= action_option[ 'lots' ]
                option[ 'kind' ]   = action_option[ 'kind' ]
                option[ 'strike' ] = action_option[ 'strike' ]
                self.date   = action_option[ 'date' ]
                option[ 'days' ]   = ( pd.to_datetime( action_option[ 'date' ], format= '%Y-%m-%d' ) - curr_time ).days
            
            elif action_option[ 'lots' ] != 0:
                logging.info( '** Broker Error: Agent tried to short sell an uncovered call.' )

            self.state[ 'option' ] = option

            # Checks for pre-existing option contracts, takes the average cost if so, takes the cost if not
            if option[ 'lots' ] < action_option[ 'lots' ]:
                option[ 'cost' ]   = ( option[ 'cost' ] + self.get_option_price() ) / 2
            else:
                option[ 'cost' ] = self.get_option_price()
        
        self.state[ 'equity' ] = equity
        self.state[ 'option' ] = option
        return

    def buy_to_close( self, action ):
        equity = self.state[ 'equity' ]
        option = self.state[ 'option' ]

        keys = action.keys()
        # Handle closing equity
        if 'equity' in keys:
            action_equity = action[ 'equity' ]

            # If agent is trying to buy_to_close a long position, log error, return
            if action_equity[ 'lots' ] > 0 and ( equity[ 'lots' ] > 0 or equity[ 'lots' ] - action_equity[ 'lots' ] > 0 ):
                lots = option[ 'lots' ]
                logging.info( f'** Logic Error: Agent tried to buy_to_close a long equity position. Equity Lots: {lots}' )

            else:
                # Adds initial value of equity, minus the current price of the equity, minus the spread and commission
                self.account_balance += (( equity[ 'cost' ]  - equity[ 'price' ] ) * 100 * action_equity[ 'lots' ] ) - ( self.equity_spread * 100 * action_equity[ 'lots' ] )
                equity[ 'lots' ] += action_equity[ 'lots' ]

        # Handle closing options
        if 'option' in keys:
            action_option = action[ 'option' ]

            # If agent is trying to buy_to_close a long position, log the error, return
            if action_option[ 'lots' ] > 0 and ( option[ 'lots' ] > 0 or option[ 'lots' ] + action_option[ 'lots'] > 0 ):
                lots = option[ 'lots' ]
                logging.info( f'** Logic Error: Agent tried to buy_to_close a long option position. Option Lots: {lots}' )

            else:
                # Adds the initial const minus the current price, minus the spread and commission
                self.account_balance += (( option[ 'cost' ] - option[ 'price' ]) * 100 * abs( action_option[ 'lots' ] ) ) - (( self.option_spread * 100 + self.option_commission * 2) * action_option[ 'lots' ] )
                option[ 'lots' ] += action_option[ 'lots' ]

        self.state[ 'equity' ] = equity
        self.state[ 'option' ] = option
        return

    def sell_to_close( self, action ):
        equity = self.state[ 'equity' ]
        option = self.state[ 'option' ]

        keys = action.keys()
        # Handle closing equity
        if 'equity' in keys:
            
            action_equity = action[ 'equity' ]

            # Checks for a short position when selling, logs an error and does not run calculations
            if action_equity[ 'lots' ] > 0 and ( equity[ 'lots' ] < 0 or abs( equity[ 'lots' ] ) - action_equity[ 'lots' ] < 0 ):
                lots = equity[ 'lots' ]
                logging.info( f'** Logic Error: Agent tried to sell_to_close a short equity position. Equity Lots: {lots}')

            else:
                # Adds thec current value of the equity, minus the opening cost, minus the spread and commission
                self.account_balance += (( equity[ 'price' ] - equity[ 'cost' ] ) * 100 * action_equity[ 'lots' ] ) - ( self.equity_spread * 100 * action_equity[ 'lots' ] )
                equity[ 'lots' ] -= action_equity[ 'lots' ]
        
        # Handle closing options
        if 'option' in keys:
            action_option = action[ 'option' ]
            
            # Checks for a short position when closing, logs an error if so and returns early
            if action_option[ 'lots' ] > 0 and ( option[ 'lots' ] < 0 or abs( option[ 'lots' ] ) - action_option[ 'lots' ] < 0 ):
                lots = option[ 'lots' ]
                logging.info( f'** Logic Error: Agent tried to sell_to_close a short option position.  Option Lots: {lots}' )

            else:
                # Adds the current value of the option contract minus the initial cost of the contract minus spread and commission
                self.account_balance +=  ( option[ 'price' ] - option[ 'cost' ] ) * 100 * action_option[ 'lots' ] - (( self.option_spread * 100 + self.option_commission * 2) * action_option[ 'lots' ] )
                option[ 'lots' ] -= action_option[ 'lots' ]

        self.state[ 'option' ] = option
        self.state[ 'equity' ] = equity

        return

    # Gets the historicaal volatility at the current time
    def get_historical_vol( self ):
        i = self.state[ 'index' ]
        close = self.dataset.C

        vol = self.hv[ datetime.date( close.index[ i ].year, close.index[ i ].month, close.index[ i ].day ) ]         
        return vol

    
    def get_option_price( self ):

        # Gets the price according to the current state
        option = self.state[ 'option' ]
        close  = self.state[ 'equity' ][ 'price' ]
        kind   = option[ 'kind' ]
        strike = option[ 'strike' ]
        days   = option[ 'days' ]
        vol    = self.get_historical_vol()
        price  = 0

        if days <= 0.4:
            days = 0.5

        if strike > 0:
            price = options.american( kind, close, strike, days/365, 0.01, 0.0, vol )[0]

        return price
