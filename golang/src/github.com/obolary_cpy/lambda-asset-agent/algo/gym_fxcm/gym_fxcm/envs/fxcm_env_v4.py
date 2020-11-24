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
from termcolor import colored

class FxcmEnvV4( gym.Env ):

  metadata = { 'render.modes': [ 'human' ] }

  def __init__(self, **kwargs):

    # behavioral parameters    
    self.bias_action = -1
    self.bias_profit = False
    self.bias_runner = True
    self.lot_stepsize = 1
    self.reward_multiplier = 1.0

    # structural parameters
    self.initial_balance = 10000.0
    self.margin_ratio = 50.0
    self.dataset_tick_ratio = 1 # e.g., 1to1lot (XAUUSD), 10000to1lot (EURUSD)

    self.dataset_window = 1440
    # 1440 fast/14400 slow = 13% yoy, drawdown 10k+, follows
    # 120 fast/14400 slow  = 3.2% yoy, drawdown 6k+, follows
    # 60 fast/1440 slow    = 9.9% yoy, drawdown 4k+, follows
    self.dataset_window_fast = 1440
    self.dataset_window_slow = 14400
    self.position_spread = 0.35 # FXCM XAU/USD SPREAD

    # dataset
    self.dataset_headers = ['date-time','O','H','L','C','V']
    self.dataset_file = ''
    self.dataset_sep = ';'

    # overwrite attributes with any given parameters
    for key in dir(self):
      if key in kwargs.keys():
        setattr( self, key, kwargs.pop(key) )

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

    # action-space and observation-space
    # action, 0 - hold, 1 - long, 2 - short, 3 - close
    self.action_space = spaces.Discrete( 4 )
    self.observation_space = spaces.Box( low=self.min_array_state, high=self.max_array_state, dtype=np.float32 )

    # read selected dataset file
    self.dataset = pd.read_csv( self.dataset_file, sep=self.dataset_sep, names=self.dataset_headers )
    self.dataset['H'] = self.dataset['H'] * self.dataset_tick_ratio
    self.dataset['L'] = self.dataset['L'] * self.dataset_tick_ratio
    self.dataset['O'] = self.dataset['O'] * self.dataset_tick_ratio
    self.dataset['C'] = self.dataset['C'] * self.dataset_tick_ratio

    # initialize state
    self.reset()

  def reset(self):

    self.csvfile = open( 'log.csv', 'w' )
    self.log = csv.writer( self.csvfile )

    self.balance = np.full( len( self.dataset ), self.initial_balance )

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

    s, _, _ = self._state( action=0 )
    return s

  def step(self, action):

    s, r, done = self._state( action )
    if not done and self.balance[ self.dataset_index ] < 0.0:
      done = True

    return s, r, done, {}

  def render(self, mode='human'):

    return

  def close(self):
    
    pass

  def _state(self,action):

    if self._tick() == True:
      return self.min_state, self._profit(), True

    target_profit = 0.0 
    reward = 0.0
    current_price = self.dataset['C'][ self.dataset_index ] 

    if action == 0:

      # hold / do nothing
      pass

    elif action == 1:

      # long
      if self.bias_action == 2:

        pass

      elif self.balance[ self.dataset_index ] - self.position_baseline * abs( self.position_lots ) - current_price < 0:

        pass

      elif self.position_lots < 0.0:

        lot_profit = ( current_price - self.position_baseline ) * self.margin_ratio * -1.0
        if self.bias_profit == True and lot_profit < 0.0:

          pass 

        else:

          reward = lot_profit
          self.balance[ self.dataset_index ] = self.balance[ self.dataset_index - 1 ] + lot_profit - self.position_spread * self.margin_ratio

          self.position_lots = self.position_lots + 1
          if self.position_lots == 0.0:
            self.dump_pos( 'CLOSER      :', color='red' )
            self.position_baseline = 0.0
            self.position_length = 0.0
          else:
            self.dump_pos( ' **   LONGER:' )

      elif self.position_lots == 0.0:

        self.position_baseline = current_price
        self.position_lots = self.lot_stepsize
        self.position_length = self.dataset_index
        self.position_lastopen = self.dataset_index
        self.dump_pos( ' **     LONG:' )

      elif self.bias_runner == False and current_price > self.position_baseline:

        pass

      elif self.bias_runner == False and current_price < self.position_baseline or self.bias_runner == True:

        current_lots = abs( self.position_lots )
        self.position_baseline = (self.position_baseline * current_lots + current_price) / (current_lots + self.lot_stepsize)
        self.position_lots = self.position_lots + self.lot_stepsize
        self.dump_pos( ' **     LONG:' )

      else:

        pass

    elif action == 2:

      # short
      if self.bias_action == 1:

        pass

      elif self.balance[ self.dataset_index ] - self.position_baseline * abs( self.position_lots ) - current_price < 0:

        pass

      elif self.position_lots > 0.0:

        lot_profit = ( current_price - self.position_baseline ) * self.margin_ratio * 1.0
        if self.bias_profit == True and lot_profit < 0.0:

          pass 

        else:

          reward = lot_profit
          self.balance[ self.dataset_index ] = self.balance[ self.dataset_index - 1 ] + lot_profit - self.position_spread * self.margin_ratio

          self.position_lots = self.position_lots - 1
          if self.position_lots == 0.0:
            self.dump_pos( 'CLOSER      :', color='red' )
            self.position_baseline = 0.0
            self.position_length = 0.0
          else:
            self.dump_pos( ' **  SHORTER:' )

      elif self.position_lots == 0.0:
      
        self.position_baseline = current_price
        self.position_lots = -self.lot_stepsize
        self.position_length = self.dataset_index
        self.position_lastopen = self.dataset_index
        self.dump_pos( ' **    SHORT:' )
      
      elif self.bias_runner == False and current_price < self.position_baseline:

        pass

      elif self.bias_runner == False and current_price > self.position_baseline or self.bias_runner == True:
      
        current_lots = abs( self.position_lots )
        self.position_baseline = (self.position_baseline * current_lots + current_price) / (current_lots + self.lot_stepsize)
        self.position_lots = self.position_lots - self.lot_stepsize
        self.dump_pos( ' **    SHORT:' )

      else:

        pass

    elif action == 3:

      # close
      if self.position_lots == 0.0:

        pass
      
      elif self.bias_profit == True and self._profit() < target_profit:

        pass 

      else:

        profit = self._profit() 
        reward = profit
        self.balance[ self.dataset_index ] = self.balance[ self.dataset_index - 1 ] + profit - self.position_spread * self.margin_ratio * abs( self.position_lots )
        self.dump_pos( 'CLOSE       :', color='red' )
        self.position_lots = 0.0
        self.position_baseline = 0.0
        self.position_length = 0.0

    if reward != 0.0:
      reward = reward * self.reward_multiplier
      print( ' **   REWARD:', reward )

    # change min_state and max_state
    done = False
    while not done:

      # get current close, high and low
      current_price = self.dataset['C'][ self.dataset_index ] 
      profit = self._profit()

      # get zscore for short window
      history_fast = self.dataset['C'][ self.dataset_index - self.dataset_window_fast : self.dataset_index ]
      history_fast_mean = history_fast.mean()
      zscore_fast = int( 0.5 + (( current_price - history_fast_mean ) / history_fast.std()) )
      
      # get zscore for low window
      history_slow = self.dataset['C'][ self.dataset_index - self.dataset_window_slow : self.dataset_index ]
      history_slow_mean = history_slow.mean()
      zscore_slow = int( 0.5 + (( current_price - history_slow_mean ) / history_slow.std()) )

      # any short zscore change triggers a sample
      if zscore_fast != self.dataset_zscore_fast[-1] or zscore_slow != self.dataset_zscore_slow[-1]:

        self.dataset_zscore_fast = np.append( self.dataset_zscore_fast, zscore_fast )
        self.dataset_zscore_slow = np.append( self.dataset_zscore_slow, zscore_slow )

        self.dataset_extra_ind1 = np.append( self.dataset_extra_ind1, current_price - history_fast_mean )
        self.dataset_extra_ind2 = np.append( self.dataset_extra_ind2, current_price - history_slow_mean )

        self.dataset_extra_ind8 = np.append( self.dataset_extra_ind8, profit )
        self.dataset_extra_ind9 = np.append( self.dataset_extra_ind9, self.position_lots )

        position_length = 0
        if self.position_length != 0:
          position_length = self.dataset_index - self.position_length

        self.log.writerow([
          self.dataset_index,
          self.balance[ self.dataset_index ],
          action,
          position_length,
          current_price,
          self.dataset_zscore_fast[ -1: ][0],
          self.dataset_zscore_slow[ -1: ][0],
          self.dataset_zscore_slow[ -1: ][0] - self.dataset_zscore_fast[ -1: ][0],
          self.dataset_zscore_slow[ -1: ][0] + self.dataset_zscore_fast[ -1: ][0],
          self.dataset_extra_ind1[ -1: ][0],
          self.dataset_extra_ind2[ -1: ][0],
          self.dataset_extra_ind8[ -1: ][0],
          self.dataset_extra_ind9[ -1: ][0]
        ])
        self.csvfile.flush()

        if len( self.dataset_zscore_fast ) > self.dataset_window:
          done = True
          continue

      # otherwise, wait until all significant events are found
      if self._tick() == True:
        return self.min_state, self._profit(), True
      
    return np.array([
      self.dataset_zscore_fast[ -self.dataset_window: ],
      self.dataset_zscore_slow[ -self.dataset_window: ],
      self.dataset_zscore_slow[ -self.dataset_window: ] - self.dataset_zscore_fast[ -self.dataset_window: ],
      self.dataset_zscore_slow[ -self.dataset_window: ] + self.dataset_zscore_fast[ -self.dataset_window: ],
      self.dataset_extra_ind1[ -self.dataset_window: ],
      self.dataset_extra_ind2[ -self.dataset_window: ],
      self.dataset_extra_ind8[ -self.dataset_window: ],
      self.dataset_extra_ind9[ -self.dataset_window: ]
    ]), reward, False

  def _profit( self ):

    current_price = self.dataset['C'][ self.dataset_index ] 
    profit = ( current_price - self.position_baseline ) * self.position_lots
    return profit * self.margin_ratio

  def _tick( self ):

    self.dataset_index = self.dataset_index + 1
    if self.dataset_index >= len(self.dataset):
      return True

    profit = self._profit() 
    if profit < self.drawdown:
      self.drawdown = profit

    self.balance[ self.dataset_index ] = self.balance[ self.dataset_index - 1 ]

    if self.dataset_index % 10000 == 0:
      self.dump_pos( ' ** PROGRESS:' )

    # TODO - should handle ratio (long and short) and according to forex rules
    if self.position_lots < 0:
      current_extent = self.dataset['H'][ self.dataset_index ]
      margin_balance = self.balance[ self.dataset_index ] - self.position_baseline * abs( self.position_lots )
      current_profit_extent = ( current_extent - self.position_baseline ) * self.position_lots
      if margin_balance + current_profit_extent < 0:
        self.dump_pos( ' ** MARGIN CALL:' )
        return True

    return False

  def dump_pos( self, action, color='green' ):

      current_price = self.dataset['C'][ self.dataset_index ] 
      profit = self._profit() 

      print( 
        colored( action, color ), self.dataset_index,
        '| profit:', '$ {:06,.2f}'.format( profit ), 
        '| lots:', self.position_lots, 
        '| open:', self.position_baseline, 
        '| close:', current_price, 
        '| length:', self.dataset_index - self.position_length,
        '| drawdown:', '$ {:06,.2f}'.format( self.drawdown ),
        '| balance:', '$ {:06,.2f}'.format( self.balance[ self.dataset_index ] ) 
      )
      self.dump_score()

  def dump_score( self ):

      print(
        ' **    SCORE:', self.dataset_index,
        '| fast', self.dataset_zscore_fast[ -1: ][0],
        '| slow', self.dataset_zscore_slow[ -1: ][0],
        '| diff', self.dataset_zscore_slow[ -1: ][0] - self.dataset_zscore_fast[ -1: ][0],
        '| sum', self.dataset_zscore_slow[ -1: ][0] + self.dataset_zscore_fast[ -1: ][0],
        '| profit', self.dataset_extra_ind8[ -1: ][0],
        '| lots', self.dataset_extra_ind9[ -1: ][0],
      )

