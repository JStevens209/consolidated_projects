import gym
import pandas as pd
import numpy as np
import math
import collections

import matplotlib
import matplotlib.pyplot as plt
import tensorflow as tf

from gym import error, spaces, utils
from gym.utils import seeding

class FxcmEnv( gym.Env ):

  metadata = { 'render.modes': [ 'human' ] }

  def __init__(self, **kwargs):
    
    self.last_render = 0

    self.bias_action = -1
    self.bias_profit = False
    self.bias_runner = True

    # dataset
    self.dataset_headers = ['date-time','O','H','L','C','V']
    self.dataset_file = ''
    self.dataset_sep = ';'
    self.dataset_tick = 0.01
    self.dataset_window_fast = 256
    self.dataset_zscore_fast = 0
    self.dataset_window_slow = 14400
    self.dataset_zscore_slow = 0
    self.dataset_index = self.dataset_window_slow

    # lots
    self.min_lots = -np.finfo(np.float32).max
    self.max_lots = np.finfo(np.float32).max

    self.position_lots = 0.0
    self.position_baseline = 0.0
    self.position_length = 0.0
    self.position_spread = 0.35 # FXCM XAU/USD SPREAD
    self.position_lastopen = self.dataset_index + self.dataset_window_slow
    self.lot_stepsize = 1

    # states
    num_features = (self.dataset_window_fast)
    self.min_state = np.full( num_features, -np.finfo(np.float32).max ) 
    self.max_state = np.full( num_features, +np.finfo(np.float32).max )

    # actions
    self.actions = [ 'hold', 'long', 'short', 'close', 'not-applicable' ]

    # action-space and observation-space
    # action, 0 - hold, 1 - long, 2 - short, 3 - close
    self.action_space = spaces.Discrete( 4 )
    self.observation_space = spaces.Box( low=self.min_state, high=self.max_state, dtype=np.float32 )

    # reward and returns
    self.reward_func = 'sortino'
    self.reward_return_window = 1

    # any callback for balance updates
    self.balance_callback = None

    # overwrite attributes with any given parameters
    for key in dir(self):
      if key in kwargs.keys():
        setattr( self, key, kwargs.pop(key) )

    # read selected dataset file
    self.dataset = pd.read_csv( self.dataset_file, sep=self.dataset_sep, names=self.dataset_headers )

    # initialize simulation
    self.drawdown = 0.0
    self.returns = np.array([])
    self.balance = np.full( len( self.dataset ), 10000 )
    if self.balance_callback != None:
      self.balance_callback( self.balance[ self.dataset_index ] )

    self.benchmarks = np.array([
      {
        'label': 'zscore fast',
        'values': np.full( len( self.dataset ), 0.0 )
      },
      {
        'label': 'zscore slow',
        'values': np.full( len( self.dataset ), 0.0 )
      },
    ])
    self.trades = np.array([])
    
    # clear state
    self.reset()

  def step(self, action):

    current_price = self.dataset['C'][self.dataset_index] 
    profit = ( current_price - self.position_baseline ) * self.position_lots - self.position_spread * abs( self.position_lots )

    s, done = self._state( action )
    r = self._reward( action, profit )

    if not done and self.balance[ self.dataset_index ] < 0.0:
      done = True

    return s, r, done, {}

  def reset(self):

    self.returns = np.array([])
    self.balance = np.full( len( self.dataset ), 10000.0 )

    self.benchmarks = np.array([
      {
        'label': 'zscore fast',
        'values': np.full( len( self.dataset ), 0.0 )
      },
      {
        'label': 'zscore slow',
        'values': np.full( len( self.dataset ), 0.0 )
      },
    ])
    self.trades = np.array([])

    self.dataset_index = self.dataset_window_slow
    self.dataset_zscore_fast = 0
    self.dataset_zscore_slow = 0

    self.position_lots = 0.0
    self.position_baseline = 0.0
    self.position_length = 0.0
    self.position_lastopen = self.dataset_index + self.dataset_window_slow

    self.drawdown = 0.0

    if self.balance_callback != None:
      self.balance_callback( self.balance[ self.dataset_index ] )

    s, _ = self._state( action=0 )
    return s

  def render(self, mode='human'):

    return

  def close(self):
    
    pass

  def _state(self,action):

    if self._tick() == True:
      return self.min_state, True

    current_price = self.dataset['C'][self.dataset_index] 
    profit = ( current_price - self.position_baseline ) * self.position_lots - self.position_spread * abs( self.position_lots )
    target_profit = 0.0 # self.position_baseline * 1.1 - current_price if self.position_lots > 0 else current_price - self.position_baseline * 0.9

    if action == 0:

      # hold / do nothing
      pass

    elif action == 1:

      # long
      if self.position_lots < 0.0:

        pass

      elif self.bias_action == 2:

        pass

      elif self.balance[ self.dataset_index ] - self.position_baseline * abs( self.position_lots ) - current_price < 0:

        pass

      elif self.position_lots == 0.0:

        self.position_baseline = current_price
        self.position_lots = self.lot_stepsize
        self.position_length = self.dataset_index
        self.position_lastopen = self.dataset_index
        self._trade( action )

      elif self.bias_runner == False and current_price > self.position_baseline:

        pass

      elif self.bias_runner == False and current_price < self.position_baseline * 0.90 or self.bias_runner == True:

        current_lots = abs( self.position_lots )
        self.position_baseline = (self.position_baseline * current_lots + current_price) / (current_lots + self.lot_stepsize)
        self.position_lots = self.position_lots + self.lot_stepsize
        self.position_lastopen = self.dataset_index
        self._trade( action )

      else:

        pass

    elif action == 2:

      # short
      if self.position_lots > 0.0:

        pass

      elif self.bias_action == 1:

        pass

      elif self.balance[ self.dataset_index ] - self.position_baseline * abs( self.position_lots ) - current_price < 0:

        pass

      elif self.position_lots == 0.0:
      
        self.position_baseline = current_price
        self.position_lots = -self.lot_stepsize
        self.position_length = self.dataset_index
        self.position_lastopen = self.dataset_index
        self._trade( action )
      
      elif self.bias_runner == False and current_price < self.position_baseline:

        pass

      elif self.bias_runner == False and current_price > self.position_baseline * 1.10 or self.bias_runner == True:
      
        current_lots = abs( self.position_lots )
        self.position_baseline = (self.position_baseline * current_lots + current_price) / (current_lots + self.lot_stepsize)
        self.position_lots = self.position_lots - self.lot_stepsize
        self.position_lastopen = self.dataset_index
        self._trade( action )

      else:

        pass

    elif action == 3:

      # close
      if self.position_lots == 0.0:

        pass
      
      elif self.bias_profit == True and profit < target_profit:

        pass 

      else:

        self._trade( action )
        self.balance[ self.dataset_index ] = self.balance[ self.dataset_index - 1 ] + profit
        self.returns = np.append( self.returns, profit * 1.0 )

        if self.balance_callback != None:
          self.balance_callback( self.balance[ self.dataset_index ] )

        print( 
          'step:', self.dataset_index,
          '| profit:', '$ {:06,.2f}'.format( profit ), 
          '| lots:', self.position_lots, 
          '| open:', self.position_baseline, 
          '| close:', current_price, 
          '| length:', self.dataset_index - self.position_length,
          '| drawdown:', '$ {:06,.2f}'.format( self.drawdown ),
          '| balance:', '$ {:06,.2f}'.format( self.balance[ self.dataset_index ] ) 
        )

        self.position_lots = 0.0
        self.position_baseline = 0.0
        self.position_length = 0.0
      
    # change min_state and max_state
    s = self.dataset['C'][ self.dataset_index - self.dataset_window_fast : self.dataset_index ].to_numpy()

    return s, False

  def _reward( self, action, profit ) :

    # get last returns
    #length = min( len( self.returns ), self.reward_return_window )
    #returns = self.returns[ -length: ]

    # get current return
    reward = 0.0
    if action == 3:
      reward = profit

    # avoid non-numbers
    if np.isnan( reward ) or np.isinf( reward ):
      reward = 0.0

    return reward 

  def _tick( self ):

    self.dataset_index = self.dataset_index + 1
    if self.dataset_index >= len(self.dataset):
      return True

    current_price = self.dataset['C'][ self.dataset_index ] 
    profit = ( current_price - self.position_baseline ) * self.position_lots - self.position_spread * abs( self.position_lots )
    if profit < self.drawdown:
      self.drawdown = profit

    self.balance[ self.dataset_index ] = self.balance[ self.dataset_index - 1 ]
    if self.balance_callback != None:
      self.balance_callback( self.balance[ self.dataset_index ] )

    if self.dataset_index % 10000 == 0:
      print( 
        '     ** progress **',
        'step:', self.dataset_index,
        '| profit:', '$ {:06,.2f}'.format( profit ), 
        '| lots:', self.position_lots, 
        '| open:', self.position_baseline, 
        '| close:', current_price, 
        '| length:', self.dataset_index - self.position_length,
        '| drawdown:', '$ {:06,.2f}'.format( self.drawdown ),
        '| balance:', '$ {:06,.2f}'.format( self.balance[ self.dataset_index ] ) 
      )

    if self.position_lots < 0:
      current_extent = self.dataset['H'][ self.dataset_index ]
      margin_balance = self.balance[ self.dataset_index ] - self.position_baseline * abs( self.position_lots )
      current_profit_extent = ( current_extent - self.position_baseline ) * self.position_lots
      if margin_balance + current_profit_extent < 0:
        print( '*** MARGIN CALL ***' )
        return True

    return False

  def _trade( self, action ):

    current_price = self.dataset['C'][self.dataset_index] 
    profit = ( current_price - self.position_baseline ) * self.position_lots - self.position_spread * abs( self.position_lots )

    if action == 0:

      pass 

    elif action == 1:

      self.trades = np.append( self.trades, {
        'step': self.dataset_index,
        'amount': abs( self.position_lots ), 
        'total': 0.0,
        'action': 'open',
        'type': 'buy'
      })

    elif action == 2:
      
      self.trades = np.append( self.trades, {
        'step': self.dataset_index,
        'amount': abs( self.position_lots ), 
        'total': 0.0,
        'action': 'open',
        'type': 'sell'
      })

    elif action == 3:

      self.trades = np.append( self.trades, {
        'step': self.dataset_index,
        'amount': abs( self.position_lots ), 
        'total': profit,
        'action': 'close',
        'type': 'sell' if self.position_lots < 0 else 'buy'
      })

