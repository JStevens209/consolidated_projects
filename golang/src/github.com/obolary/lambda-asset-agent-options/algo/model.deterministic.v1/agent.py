from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time
import warnings

from pathlib import Path
from absl import logging
from absl import flags
from absl import app

import matplotlib as mpl
from matplotlib import pylab as plt

import numpy as np
import pandas as pd

import gym

from model import Model
from context import *

flags.DEFINE_enum( 'mode', 'application', ['service', 'application'], 'service or application mode.' )
flags.DEFINE_string( 'CLIENT_ID', CLIENT_ID, "User's TD Developer api-key" )
flags.DEFINE_string( 'REDIRECT_URI', REDIRECT_URI, "User's uri specified on creation of TD Developer application")
flags.DEFINE_string( 'CREDENTIALS_PATH', CREDENTIALS_PATH, "Path to a .json file that holds access/refresh keys")
flags.DEFINE_string( 'ACCOUNT_NUMBER', ACCOUNT_NUMBER, "User's TD Ameritrade Account number")

FLAGS = flags.FLAGS
logging.set_verbosity(logging.INFO)

class Agent():

    def __init__( self, gym_id, symbol ):
        logging.info( '** initializing agent,...' )

        self.env = gym.make( 
            gym_id,
            symbol= symbol,
            CLIENT_ID= FLAGS.CLIENT_ID,
            REDIRECT_URI= FLAGS.REDIRECT_URI,
            CREDENTIALS_PATH= FLAGS.CREDENTIALS_PATH,
            ACCOUNT_NUMBER= FLAGS.ACCOUNT_NUMBER  
        )
        self.model = Model( symbol )

    def train( self ):
        logging.info( '** begin training,...' )

        pass

    def run( self ):
        logging.info( '** begin prediction,...' )
        
        # bootstrap env and determine first action
        observation = self.env.reset()
        action = self.model.action( observation )

        # run loop until done
        done = False
        self.state = self.env.reset()
        
        while not done:
            # get observation, reward (unused) and done from env
            observation, _, done, _ = self.env.step( action )
                
            # determine next action
            if observation != None:
                action = self.model.action( observation )

def main( argv ):

    agent = Agent(
        'td_gym:td-gym-v1',
        'SLV',
    )
    agent.run()


if __name__ == "__main__":
    app.run( main )



