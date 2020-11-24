import pandas as pd
import gym
import numpy as np
import math
import collections
import csv
import time

import matplotlib
import matplotlib.pyplot as plt
import tensorflow as tf
import cbpro

from gym import error, spaces, utils
from gym.utils import seeding
from termcolor import colored

class WebsocketClient( cbpro.WebsocketClient ):

  def __init__( self, env, socketurl, key, passphrase, b64secret, pair='BTC-USD' ):
      
    self.env = env
    self.url = socketurl
    self.auth = True
    self.api_key = key
    self.api_passphrase = passphrase
    self.api_secret = b64secret
    self.products = [ pair ]
    
    super().__init__( channels = [ 'ticker' ] )
      
  def on_open(self):

    pass
  
  def on_message( self, msg ):
      
    self.env.tick( msg )
          
  def on_close( self ):
      
    pass
        
class CoinEnvV0( gym.Env ):

  metadata = { 'render.modes': [ 'human' ] }

  def __init__(self, **kwargs):

    # parameters    
    self.cbpro_weburl = 'https://public.sandbox.pro.coinbase.com'
    self.cbpro_resturl = 'https://api-public.sandbox.pro.coinbase.com'
    self.cbpro_socketurl = 'wss://ws-feed-public.sandbox.pro.coinbase.com'
    self.cbpro_fixurl = 'tcp+ssl://fix-public.sandbox.pro.coinbase.com:4198'

    self.cbpro_passphrase = 'je5zm0rm4i'
    self.cbpro_key = '5fc3717334a8718cd60f3ee74b819cec'
    self.cbpro_b64secret = '/fnWX+p82wuYbdjKZ3rlIceuUB1hxut2/6/EVchzuBntYHnZ4PxpcG2epTuvUnV8IAlzGu584mWBPch7wo6Ohw=='

    self.cbpro_usd_account = '3c4528aa-7065-42c8-999b-37f322af98f5'
    self.cbpro_btc_account = '44078656-cfca-4355-9ddd-d7f7c927ca9e'
    self.cbpro_best_bid = 0.0
    self.cbpro_best_ask = 0.0

    self.bias_profit = False
    self.bias_runner = True
    
    self.dataset_window = 1440
    
    # optional overwrite parameters
    for key in dir( self ):
      if key in kwargs.keys():
        setattr( self, key, kwargs.pop(key) )

    # observation-space config
    self.min_state = np.full( self.dataset_window, -np.finfo(np.float32).max ) 
    self.max_state = np.full( self.dataset_window, +np.finfo(np.float32).max )
    self.min_array_state = np.array([
      self.min_state,
      self.min_state,
      self.min_state,
    ])
    self.max_array_state = np.array([
      self.max_state,
      self.max_state,
      self.max_state,
    ])

    # action-space and observation-space
    # action, 0 - hold, 1 - long, 2 - close (there is no short)
    self.action_space = spaces.Discrete( 3 )
    self.observation_space = spaces.Box( low=self.min_array_state, high=self.max_array_state, dtype=np.float32 )
    
    # cbpro connections
    self.cbpro_client = cbpro.AuthenticatedClient( self.cbpro_key, self.cbpro_b64secret, self.cbpro_passphrase, api_url=self.cbpro_resturl )
    self.cbpro_socket = WebsocketClient( self, self.cbpro_socketurl, self.cbpro_key, self.cbpro_passphrase, self.cbpro_b64secret, pair='BTC-USD' )
    self.cbpro_socket.start()

    # parameters normally in reset section
    self.cbpro_dirty = False
    self.cbpro_last_order_id = ''
    self.cbpro_last_order_done = False

    self.balance = np.array( [0.] )
    
    self.dataset_price = np.array( [0.] )
    self.dataset_volume = np.array( [0.] )
    self.dataset_side = np.array( [0.] )

    self.dataset_dirty = False

    # reset session
    self.reset()
    return

  def reset( self ):

    self.csvfile = open( 'log.csv', 'w' )
    self.log = csv.writer( self.csvfile )

    s, _, _, _ = self.step( action=0 )    
    return s

  def tick( self, data ):
    
    if 'type' in data:
        
      if data[ 'type' ] == 'ticker' \
        and 'price' in data \
          and 'last_size' in data:
          
        self.dataset_price = np.append( self.dataset_price, float( data[ 'price' ] ) )
        self.dataset_volume = np.append( self.dataset_volume, float( data[ 'last_size' ] ) )
        self.cbpro_best_bid = float( data[ 'best_bid' ] )
        self.cbpro_best_ask = float( data[ 'best_ask' ] )
        if data[ 'side' ] == 'buy':
          self.dataset_side = np.append( self.dataset_side, 1. )
        else:
          self.dataset_side = np.append( self.dataset_side, 2. )

        self.dataset_price = self.dataset_price[ -self.dataset_window: ]
        self.dataset_volume = self.dataset_volume[ -self.dataset_window: ]

        self.dataset_dirty = True
        print( ' ** TICK   :', data[ 'price' ], '-', data[ 'last_size' ], '-', data[ 'side' ], len( self.dataset_price ) )

        if self.cbpro_dirty:

          r = self.cbpro_client.get_order( self.cbpro_last_order_id )
          if 'status' in r and r[ 'status' ] == 'done':

            self.cbpro_dirty = False

            if 'side' in r and r[ 'side' ] == 'sell':
              self.cbpro_last_order_done = True

            print( ' ** DONE   :', r[ 'side' ],  r[ 'id' ] )

    return

  def step( self, action ):

    self.dataset_dirty = False

    # perform action
    # action, 0 - hold, 1 - long, 2 - close (there is no short)
    if action == 0:
        
      pass
    
    elif action == 1:
        
      if self.cbpro_dirty == False:
        r = self.cbpro_client.place_market_order( product_id='BTC-USD', side='buy', size='0.1' )
        if 'id' in r:
          self.cbpro_last_order_id = r[ 'id' ]
          self.cbpro_dirty = True
          print( ' ** BUY    :', r[ 'id' ] )
    
    elif action == 2:
        
      if self.cbpro_dirty == False:
        r = self.cbpro_client.place_market_order( product_id='BTC-USD', side='sell', size='0.1' )
        if 'id' in r:
          self.cbpro_last_order_id = r[ 'id' ]
          self.cbpro_dirty = True
          print( ' ** SELL   :', r[ 'id' ] )
        
    else:
        
      print( ' ** ERROR  : unknown action,', action )

    while len( self.dataset_price ) < self.dataset_window or self.dataset_dirty == False:
        
      # yield to other threads
      time.sleep( 0 )
        
    reward = self._reward()
    return np.array([
      self.dataset_price[ -self.dataset_window: ],
      self.dataset_volume[ -self.dataset_window: ],
      self.dataset_side[ -self.dataset_window: ],
    ]), reward, False, {}

  def render( self, mode='human' ):

    return

  def close( self ):
    
    return

  def _reward( self ):
        
    reward = 0.
    current = 0.
    valid = False

    if self.cbpro_last_order_done == True:

      self.cbpro_last_order_done = False
      account = self.cbpro_client.get_account( self.cbpro_usd_account ) 
      if 'balance' in account:

        current = float(account[ 'balance' ])

        account = self.cbpro_client.get_account( self.cbpro_btc_account )
        if 'balance' in account and self.cbpro_best_bid > 0.0:

          current = current + float(account[ 'balance' ]) * self.cbpro_best_bid
          valid = True

      if valid:

        if self.balance[ -1 ] > 0.0:
          reward = current - self.balance[ -1 ]

        self.balance = np.append( self.balance, current )
        self.balance = self.balance[ -2: ]

    print( ' ** REWARD :', reward, self.balance )
    return reward  