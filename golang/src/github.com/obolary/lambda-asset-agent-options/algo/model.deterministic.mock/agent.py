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

flags.DEFINE_enum( 'mode', 'application', ['service', 'application'], 'service or application mode.' )
flags.DEFINE_string( 'dataset_file', '/Users/joshua/source/golang/src/github.com/obolary/lambda-asset-corpus/ALL/XAUUSD_1M_ALL.csv', 'simulation data-set.' )
flags.DEFINE_string( 'dataset_underlying', 'GLD', 'underlying equity' )
flags.DEFINE_float( 'dataset_multiplier', 1, 'underlying dataset multiplier' )

FLAGS = flags.FLAGS
logging.set_verbosity(logging.INFO)


date = None

class Model():

    def __init__( self ):
        logging.info( '** initializing model,...' )

        self.next_action = {}
        self.prev_lots = 0

        pass

    def action( self, observation ):
        action = { 'kind': 'hold' }

        option = observation[ 'option' ]
        equity = observation[ 'equity' ]
        action_option = {}
        action_equity = {}

        if equity[ 'price' ] == 0:
            return action

        delta = pd.Timedelta( "{} days".format( date.dayofweek + ( date.dayofweek % 4 )))
        oom = 5
       
        if not self.next_action:
            
            if option[ 'price' ] <= .05 and option[ 'cost' ] > option[ 'price' ] and option[ 'price' ] != 0 and option[ 'lots' ] != 0:
                action[ 'kind' ] = 'close'
                action[ 'extrinsic' ] = 'buy'

                action_option[ 'kind' ] = 'c'
                action_option[ 'lots' ] = abs( option[ 'lots' ] )

            elif equity[ 'price' ] > ( option[ 'strike' ] + ( option[ 'strike' ] * .01 )) and option[ 'lots' ] != 0:
                action[ 'kind' ] = 'close'
                action[ 'extrinsic' ] = 'buy'

                action_option[ 'lots' ] = abs( option[ 'lots' ] )
                action_option[ 'kind' ] = 'c'

                self.next_action[ 'kind' ] = 'close'
                self.next_action[ 'extrinsic' ] = 'sell'

                self.next_action[ 'equity' ] = { 'lots': equity[ 'lots' ] }
            # If there is no equity, open a position by buying equity
            elif equity[ 'lots' ] == 0:

                if observation[ 'balance' ] / equity[ 'price' ] < 100:
                    balance = observation[ 'balance' ]
                    logging.info( f'** Not enough funds to cover any calls. Balance: {balance}' )
                    return action

                action[ 'kind' ] = 'open'
                action[ 'extrinsic' ] = 'buy'
                action_equity[ 'lots' ] = int( observation[ 'balance' ] / ( equity[ 'price' ] *  100 ))

            # If agent holds equity and no option, open an option position
            elif ( option[ 'lots' ] == 0 ) and ( equity[ 'lots' ] > option[ 'lots' ] ):
                
                action[ 'kind' ] = 'open'
                action[ 'extrinsic' ] = 'sell'

                action_option[ 'kind' ] = 'c'
                action_option[ 'lots' ] = equity[ 'lots' ]
                action_option[ 'strike' ] = oom * np.round( ( np.ceil( equity[ 'price' ] + ( oom / 2 ) ) ) / oom )
                
                action_option[ 'date' ] = date + delta

        else:
            action = self.next_action
            self.next_action = {}

        self.prev_lots = abs(option[ 'lots' ]) 

        if action_equity:
            action[ 'equity' ] = action_equity
        if action_option:
            action[ 'option' ] = action_option
        return action


class Agent():

    def __init__( self, gym_id, dataset_underlying, dataset_file, dataset_multiplier ):
        logging.info( '** initializing agent,...' )

        self.env = gym.make( 
            gym_id,
            dataset_underlying=dataset_underlying,
            dataset_file=dataset_file,
            dataset_multiplier=dataset_multiplier
        )
        self.model = Model()

    def train( self ):
        logging.info( '** begin training,...' )

        pass

    def predict( self ):
        logging.info( '** begin prediction,...' )
        
        # bootstrap env and determine first action
        observation = self.env.reset()
        action = self.model.action( observation )


        # run loop until done
        done = False
        while not done:

            # get observation, reward (unused) and done from env
            observation, _, done, _ = self.env.step( action )

            global date 
            date = self.env.dataset.C.index[ observation[ 'index' ] ]
            # log progress
            index = observation[ 'index' ]
            balances.append( observation[ 'balance' ] )
            if index % 10000 == 0:
                balance = observation[ 'balance' ]
                logging.info( f'** current index, {index} balance, {balance}' )
                
            # determine next action
            action = self.model.action( observation )

        plt.plot( balances )
        plt.show() 

        


def main( _ ):

    agent = Agent(
        'td_gym:td-gym-v1',
        FLAGS.dataset_underlying,
        FLAGS.dataset_file,
        FLAGS.dataset_multiplier
    )
    agent.predict()


if __name__ == "__main__":
    app.run( main )
