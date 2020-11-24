import gym
import pandas as pd
import numpy as np
import math
import collections
import ta
import csv

import matplotlib
import matplotlib.pyplot as plt
import tensorflow as tf

from gym import error, spaces, utils
from gym.utils import seeding

class FxcmEnvV3( gym.Env ):

  metadata = { 'render.modes': [ 'human' ] }

  def __init__(self, **kwargs):
    
    self.bias_action = -1
    self.bias_profit = False
    self.bias_runner = True

    self.csvfile = open( 'log.csv', 'w' )
    self.log = csv.writer( self.csvfile )

    # dataset
    self.dataset_headers = ['date-time','O','H','L','C','V']
    self.dataset_file = ''
    self.dataset_sep = ';'
    self.dataset_tick = 0.01
    self.dataset_window = 2048
    self.dataset_window_fast = 2880
    self.dataset_window_slow = 14400
    self.dataset_zscore_fast = np.array([0.])
    self.dataset_zscore_slow = np.array([0.])
    self.dataset_extra_ind1 = np.array([0.])
    self.dataset_extra_ind2 = np.array([0.])
    self.dataset_extra_ind3 = np.array([0.])
    self.dataset_extra_ind4 = np.array([0.])
    self.dataset_extra_ind5 = np.array([0.])
    self.dataset_extra_ind6 = np.array([0.])
    self.dataset_extra_ind7 = np.array([0.])
    self.dataset_extra_ind8 = np.array([0.])
    self.dataset_extra_ind9 = np.array([0.])
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
    num_features = (self.dataset_window)
    self.min_state = np.full( num_features, -np.finfo(np.float32).max ) 
    self.max_state = np.full( num_features, +np.finfo(np.float32).max )
    self.min_array_state = np.array([
      self.min_state,
      self.min_state,
      self.min_state,
      self.min_state,
      self.min_state,
      self.min_state,
      self.min_state,
      self.min_state
    ])
    self.max_array_state = np.array([
      self.max_state,
      self.max_state,
      self.max_state,
      self.max_state,
      self.max_state,
      self.max_state,
      self.max_state,
      self.max_state
    ])

    # actions
    self.actions = [ 'hold', 'long', 'short', 'close', 'not-applicable' ]

    # action-space and observation-space
    # action, 0 - hold, 1 - long, 2 - short, 3 - close
    self.action_space = spaces.Discrete( 4 )
    self.observation_space = spaces.Box( low=self.min_array_state, high=self.max_array_state, dtype=np.float32 )

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
    self.trades = np.array([])
    
    # clear state
    self.reset()

  def step(self, action):

    current_price = self.dataset['C'][self.dataset_index] 
    profit = ( current_price - self.position_baseline ) * self.position_lots

    s, done = self._state( action )
    r = self._reward( action, profit )

    if not done and self.balance[ self.dataset_index ] < 0.0:
      done = True

    return s, r, done, {}

  def reset(self):

    self.csvfile = open( 'log.csv', 'w' )
    self.log = csv.writer( self.csvfile )

    self.returns = np.array([])
    self.balance = np.full( len( self.dataset ), 10000.0 )
    self.trades = np.array([])

    self.dataset_index = self.dataset_window_slow
    self.dataset_zscore_fast = np.array([0.])
    self.dataset_zscore_slow = np.array([0.])
    self.dataset_extra_ind1 = np.array([0.])
    self.dataset_extra_ind2 = np.array([0.])
    self.dataset_extra_ind3 = np.array([0.])
    self.dataset_extra_ind4 = np.array([0.])
    self.dataset_extra_ind5 = np.array([0.])
    self.dataset_extra_ind6 = np.array([0.])
    self.dataset_extra_ind7 = np.array([0.])
    self.dataset_extra_ind8 = np.array([0.])
    self.dataset_extra_ind9 = np.array([0.])

    self.position_lots = 0.0
    self.position_baseline = 0.0
    self.position_length = 0.0
    self.position_lastopen = self.dataset_index + self.dataset_window_slow

    self.drawdown = 0.0

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
    profit = ( current_price - self.position_baseline ) * self.position_lots 
    target_profit = 0.0 

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

      elif self.bias_runner == False and current_price < self.position_baseline * 0.98 or self.bias_runner == True:

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

      elif self.bias_runner == False and current_price > self.position_baseline * 1.02 or self.bias_runner == True:
      
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
        self.position_lots = 0.0
        self.position_baseline = 0.0
        self.position_length = 0.0
      
    # change min_state and max_state
    all_current_high = self.dataset['H'][ self.dataset_index ]
    all_current_low = self.dataset['L'][ self.dataset_index ]
    done = False
    while not done:

      # get current close, high and low
      current_price = self.dataset['C'][ self.dataset_index ] 
      profit = ( current_price - self.position_baseline ) * self.position_lots

      current_high = self.dataset['H'][ self.dataset_index ]
      if current_high > all_current_high:
        all_current_high = current_high
      if current_price > all_current_high:
        all_current_high = current_price
      current_low = self.dataset['L'][ self.dataset_index ]
      if current_low < all_current_low:
        all_current_low = current_low
      if current_price < all_current_low:
        all_current_low = current_price

      # get zscore for short window
      history_fast = self.dataset['C'][ self.dataset_index - self.dataset_window_fast : self.dataset_index ]
      history_fast_mean = history_fast.mean()
      zscore_fast = int( 0.5 + (( current_price - history_fast_mean ) / history_fast.std()) )
      
      # get zscore for low window
      history_slow = self.dataset['C'][ self.dataset_index - self.dataset_window_slow : self.dataset_index ]
      history_slow_mean = history_slow.mean()
      zscore_slow = int( 0.5 + (( current_price - history_slow_mean ) / history_slow.std()) )

      # any short zscore change triggers a sample
      if zscore_fast != self.dataset_zscore_fast[-1]:

        self.dataset_zscore_fast = np.append( self.dataset_zscore_fast, zscore_fast )
        self.dataset_zscore_slow = np.append( self.dataset_zscore_slow, zscore_slow )

        zscore_fast_high = int( 0.5 + (( all_current_high - history_fast_mean ) / history_fast.std()) )
        zscore_fast_low = int( 0.5 + (( all_current_low - history_fast_mean ) / history_fast.std()) )

        self.dataset_extra_ind1 = np.append( self.dataset_extra_ind1, zscore_fast_high )
        self.dataset_extra_ind2 = np.append( self.dataset_extra_ind2, zscore_fast_low )

        self.dataset_extra_ind3 = np.append( self.dataset_extra_ind3, current_price )
        self.dataset_extra_ind4 = np.append( self.dataset_extra_ind4, all_current_high )
        self.dataset_extra_ind5 = np.append( self.dataset_extra_ind5, all_current_low )

        self.dataset_extra_ind8 = np.append( self.dataset_extra_ind8, profit )
        self.dataset_extra_ind9 = np.append( self.dataset_extra_ind9, self.position_lots )

        all_current_high = self.dataset['H'][ self.dataset_index ]
        all_current_low = self.dataset['L'][ self.dataset_index ]

        # if we sampled enough for slowest index, then sample ta's 
        if len( self.dataset_extra_ind3 ) > self.dataset_window_fast:

          close = pd.Series( self.dataset_extra_ind3[ -self.dataset_window_fast: ] )
          high = pd.Series( self.dataset_extra_ind4[ -self.dataset_window_fast: ] )
          low = pd.Series( self.dataset_extra_ind5[ -self.dataset_window_fast: ] )

          adx = ta.adx( high, low, close, int(self.dataset_window_fast/2), True )
          rsi = ta.rsi( close, int(self.dataset_window_fast/2), True )

          self.dataset_extra_ind6 = np.append( self.dataset_extra_ind6, (adx[-1:].values[0]-20.0) )            
          self.dataset_extra_ind7 = np.append( self.dataset_extra_ind7, (rsi[-1:].values[0]-50.0) )            

          self.log.writerow([
            self.dataset_index,
            action,
            self.dataset_zscore_fast[ -1: ][0],
            self.dataset_zscore_slow[ -1: ][0],
            self.dataset_extra_ind1[ -1: ][0],
            self.dataset_extra_ind2[ -1: ][0],
            self.dataset_zscore_slow[ -1: ][0] - self.dataset_zscore_fast[ -1: ][0],
            self.dataset_extra_ind3[ -1: ][0],
            self.dataset_extra_ind4[ -1: ][0],
            self.dataset_extra_ind5[ -1: ][0],
            self.dataset_extra_ind6[ -1: ][0],
            self.dataset_extra_ind7[ -1: ][0],
            self.dataset_extra_ind8[ -1: ][0],
            self.dataset_extra_ind9[ -1: ][0]
          ])
          self.csvfile.flush()

          if len( self.dataset_extra_ind7 ) > self.dataset_window:
            done = True
            continue

        else:

          self.dataset_extra_ind6 = np.append( self.dataset_extra_ind6, 0.0 )            
          self.dataset_extra_ind7 = np.append( self.dataset_extra_ind7, 0.0 )            

      if self._tick() == True:
        return self.min_state, True
      
    return np.array([
      self.dataset_zscore_fast[ -self.dataset_window: ],
      self.dataset_zscore_slow[ -self.dataset_window: ],
      self.dataset_extra_ind1[ -self.dataset_window: ],
      self.dataset_extra_ind2[ -self.dataset_window: ],
      self.dataset_extra_ind6[ -self.dataset_window: ],
      self.dataset_extra_ind7[ -self.dataset_window: ],
      self.dataset_extra_ind8[ -self.dataset_window: ],
      self.dataset_extra_ind9[ -self.dataset_window: ]
    ]), False

  def _reward( self, action, profit ) :

    # get current return
    reward = 0.0
    if action == 3.0:
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
    profit = ( current_price - self.position_baseline ) * self.position_lots 
    if profit < self.drawdown:
      self.drawdown = profit

    self.balance[ self.dataset_index ] = self.balance[ self.dataset_index - 1 ]

    if self.dataset_index % 10000 == 0:
      
      self.dump_pos( ' ** PROGRESS:' )
      self.dump_score()

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
    profit = ( current_price - self.position_baseline ) * self.position_lots

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
      self.dump_pos( ' **     LONG:' )
      self.dump_score()

    elif action == 2:
      
      self.trades = np.append( self.trades, {
        'step': self.dataset_index,
        'amount': abs( self.position_lots ), 
        'total': 0.0,
        'action': 'open',
        'type': 'sell'
      })
      self.dump_pos( ' **    SHORT:' )
      self.dump_score()

    elif action == 3:

      self.trades = np.append( self.trades, {
        'step': self.dataset_index,
        'amount': abs( self.position_lots ), 
        'total': profit,
        'action': 'close',
        'type': 'sell' if self.position_lots < 0 else 'buy'
      })

      self.balance[ self.dataset_index ] = self.balance[ self.dataset_index - 1 ] + profit - self.position_spread * abs( self.position_lots )
      self.returns = np.append( self.returns, profit * 1.0 )

      self.dump_pos( 'CLOSE:' )
      self.dump_score()

  def dump_pos( self, action ):

      current_price = self.dataset['C'][ self.dataset_index ] 
      profit = ( current_price - self.position_baseline ) * self.position_lots 

      print( 
        action, self.dataset_index,
        '| profit:', '$ {:06,.2f}'.format( profit ), 
        '| lots:', self.position_lots, 
        '| open:', self.position_baseline, 
        '| close:', current_price, 
        '| length:', self.dataset_index - self.position_length,
        '| drawdown:', '$ {:06,.2f}'.format( self.drawdown ),
        '| balance:', '$ {:06,.2f}'.format( self.balance[ self.dataset_index ] ) 
      )

  def dump_score( self ):

      print(
        ' **    SCORE:', self.dataset_index,
        '| fast', self.dataset_zscore_fast[ -1: ][0],
        '| slow', self.dataset_zscore_slow[ -1: ][0],
        '| fast_high', self.dataset_extra_ind1[ -1: ][0],
        '| fast_low', self.dataset_extra_ind2[ -1: ][0],
        '| diff', self.dataset_zscore_slow[ -1: ][0] - self.dataset_zscore_fast[ -1: ][0],
        '| current', self.dataset_extra_ind3[ -1: ][0],
        '| high', self.dataset_extra_ind4[ -1: ][0],
        '| low', self.dataset_extra_ind5[ -1: ][0],
        '| adx', self.dataset_extra_ind6[ -1: ][0],
        '| rsi', self.dataset_extra_ind7[ -1: ][0],
        '| profit', self.dataset_extra_ind8[ -1: ][0],
        '| lots', self.dataset_extra_ind9[ -1: ][0],
      )
