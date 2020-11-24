import gym
import collections
import math
import csv
import ta

import matplotlib
import matplotlib.pyplot as plt

import tensorflow as tf

import pandas as pd
import numpy as np

from gym import error, spaces, utils
from gym.utils import seeding
from termcolor import colored

def zigzag( s, pct=0.04 ):
    
    ut = 1 + pct
    dt = 1 - pct

    ld = s.index[0]
    lp = s.C[ld]
    tr = None

    zzd, zzp, zzt = [ld], [lp], [0]

    for ix, ch, cl in zip(s.index, s.H, s.L):
        # No initial trend
        if tr is None:
            if ch / lp > ut:
                tr = 1
            elif cl / lp < dt:
                tr = -1
        # Trend is up
        elif tr == 1:
            # New H
            if ch > lp:
                ld, lp = ix, ch
            # Reversal
            elif cl / lp < dt:
                zzd.append(ld)
                zzp.append(lp)
                zzt.append(tr)

                tr, ld, lp = -1, ix, cl
        # Trend is down
        else:
            # New L
            if cl < lp:
                ld, lp = ix, cl
            # Reversal
            elif ch / lp > ut:
                zzd.append(ld)
                zzp.append(lp)
                zzt.append(tr)

                tr, ld, lp = 1, ix, ch

    # Extrapolate the current trend
    if zzd[-1] != s.index[-1]:
        zzd.append(s.index[-1])

        if tr is None:
            zzp.append(s.C[zzd[-1]])
            zzt.append(0)
        elif tr == 1:
            zzp.append(s.H[zzd[-1]])
            zzt.append(1)
        else:
            zzp.append(s.L[zzd[-1]])
            zzt.append(-1)
            
    df = pd.DataFrame( index=zzd, columns=['ZZ','ZT'] )
    df['ZZ'] = zzp
    df['ZT'] = zzt
    return df

class FxcmEnvV5( gym.Env ):

  metadata = { 'render.modes': [ 'human' ] }

  def __init__(self, **kwargs):

    # behavioral parameters    
    self.bias_action = 0
    self.bias_profit = False
    self.bias_runner = False
    self.lot_stepsize = 1
    self.reward_multiplier = 1.0

    # structural parameters
    self.initial_balance = 10000.0
    self.margin_ratio = 1.0
    self.dataset_tick_ratio = 1 # e.g., 1to1lot (XAUUSD), 10000to1lot (EURUSD)

    self.dataset_window = 16
    self.position_spread = 0.35 # FXCM XAU/USD SPREAD

    # dataset
    self.dataset_headers = [ 'date-time','O','H','L','C','V' ]
    self.dataset_file = ''
    self.dataset_sep = ';'

    # override parameters
    self.__dict__.update( **kwargs )

    # states
    num_features = (self.dataset_window)
    self.min_state = np.full( num_features, -np.finfo(np.float32).max ) 
    self.max_state = np.full( num_features, +np.finfo(np.float32).max )
    self.min_array_state = np.array([
      self.min_state,
      #self.min_state,
      #self.min_state,
      #self.min_state,
    ])
    self.max_array_state = np.array([
      self.max_state,
      #self.max_state,
      #self.max_state,
      #self.max_state,
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
    self.dataset['date-time'] =  pd.to_datetime( self.dataset['date-time'], format='%Y-%m-%d')
    self.dataset = self.dataset.set_index( ['date-time'] )

    self.zigzag = zigzag( self.dataset, pct=0.04 )
    print( self.zigzag.head() )

    self.dataset = pd.concat( [self.dataset, self.zigzag], axis=1, sort=False )
    
    # initialize state
    self.reset()

  def reset(self):

    self.balance = np.full( len( self.dataset ), self.initial_balance )

    self.dataset_index = self.dataset_window

    self.position_lots = 0.0
    self.position_baseline = 0.0
    self.position_length = 0.0
    self.position_lastopen = self.dataset_index + self.dataset_window

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

  # can be called prior to step in order to determine what
  # the model should really do for an action, i.e., train
  # the model to do what it should do.
  def expected_action( self ):
        
    action = 0
    if self.dataset_index + 1 >= len(self.dataset):
        return action
    
    curr = self.dataset[ 'ZT' ][ self.dataset_index ]
    next = self.dataset[ 'ZT' ][ self.dataset_index + 1 ]
    
    if np.isnan( curr ) and not np.isnan( next ):
        action = 3
        
    else:
        if curr == -1:
            action = 1
        if curr == 1:
            action = 2
        
    return action
        
  def _state( self ,action ):

    if self._tick() == True:
      return self.min_state, self._profit(), True

    target_profit = 0.0 
    reward = 0.0
    current_price = self.dataset['C'][ self.dataset_index ] 

    if action == 0:
      reward = 1
      self.dump_pos( 'WAITING      :', color='yellow' )

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
    
    return np.array([
        #self.dataset['O'][ self.dataset_index - self.dataset_window : self.dataset_index ],
        self.dataset['C'][ self.dataset_index - self.dataset_window : self.dataset_index ],
        #self.dataset['H'][ self.dataset_index - self.dataset_window : self.dataset_index ],
        #self.dataset['L'][ self.dataset_index - self.dataset_window : self.dataset_index ],
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
