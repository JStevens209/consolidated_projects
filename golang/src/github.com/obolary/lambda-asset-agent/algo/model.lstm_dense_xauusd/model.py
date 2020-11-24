# python 3.6.9
# tensorflow >= 2.0.0

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import tensorflow.keras.models as km
import tensorflow.keras.layers as kl
import tensorflow.keras.losses as kls
import tensorflow.keras.optimizers as koz

import tensorflow_addons as tfa
import tensorflow_probability as tfp

import numpy as np
import gym

from pathlib import Path

class ProbabilityDistribution( tf.keras.Model ):

    def call( self, logits ):

        # sample a random categorical action from given logits
        #
        # tf.squeeze will convert tf.rank( logits ) = 2 to 1, e.g., the variable
        #   <tf.Tensor: shape=(1, 5), numpy=array( [[6]], dtype=int32 )>
        # becomes,
        #   <tf.Tensor: shape=(5,  ), numpy=array( [6], dtype=int32 )>
        # the axis = -1 par
        obs, done, ep_reward = env.reset(), False, 0
        while not done:
            action, _ = self.model.action_value( obs[None, :] )
            obs, reward, done, _ = env.step(action)
            ep_reward += reward
            if render:
                env.render()
        return ep_reward

    def _value_loss(self, returns, value):

        # value loss is typically MSE between value estimates and returns
        return self.params[ 'value' ] * kls.mean_squared_error( returns, value )

    def _logits_loss(self, acts_and_advs, logits):

        # a trick to input actions and advantages through same API
        actions, advantages = tf.split( acts_and_advs, 2, axis=-1 )

        # sparse categorical CE loss obj that supports sample_weight arg on call()
        # from_logits argument ensures transformation into normalized probabilities
        weighted_sparse_ce = kls.SparseCategoricalCrossentropy( from_logits=True )

        # policy loss is defined by policy gradients, weighted by advantages
        # note: we only calculate the loss on the actions we've actually taken
        actions = tf.cast( actions, tf.int32 )
        policy_loss = weighted_sparse_ce( actions, logits, sample_weight=advantages )

        # entropy loss can be calculated via CE over itself
        #
        # Cross-entropy loss, or log loss, measures the performance of a classification 
        # model whose output is a probability value between 0 and 1. Cross-entropy loss 
        # increases as the predicted probability diverges from the actual label. So 
        # predicting a probability of .012 when the actual observation label is 1 would 
        # be bad and result in a high loss value. A perfect model would have a log loss of 0.
        entropy_loss = kls.categorical_crossentropy( logits, logits, from_logits=True )

        # here signs are flipped because optimizer minimizes
        return policy_loss - self.params[ 'entropy' ] * entropy_loss

    def load( self, filepath ):

        self.model.load_weights( filepath )

    def save( self, filepath ):

        self.model.save_weights( filepath )

def train( dataset_file ):

    # set up gym and reset
    env = gym.make( 
        'gym_fxcm:fxcm-v4',
        bias_profit=False,
        bias_action=-1, 
        bias_runner=True, 
        margin_ratio=1.0,
        dataset_tick_ratio=1.0,
        dataset_window=128,
        dataset_window_fast=1440,
        dataset_window_slow=14400,
        dataset_file=dataset_file, 
    )

    # create and train
    print( "Training..." )
    model = Model( 
        num_actions=env.action_space.n, 
        num_observations=env.observation_space.shape 
    )
    agent = A2CAgent( model )

    if Path( 'graph' ).exists():
        print( 'Load previous before training,...')
        agent.load( 'graph/' )

    updates = 1
    for i in range( 100000 ): 
        
        raw_ep = agent.train( 
            env, 
            updates=updates, 
            batch_sz=1440 
        )
        updates = updates + 1
        
        if i % 10 == 0:
            print( '** SAVING ITERATION', i, 'EP', raw_ep )
            agent.save( 'graph/')

def predict( dataset_file ):

    # set up gym and reset
    env = gym.make( 
        'gym_fxcm:fxcm-v4', 
        bias_profit=False,
        bias_action=-1, 
        bias_runner=True, 
        margin_ratio=1.0,
        dataset_tick_ratio=1.0,
        dataset_window=128,
        dataset_window_fast=1440,
        dataset_window_slow=14400,
        dataset_file=dataset_file, 
    )

    # evaluate
    print( "Evaluating..." )
    model = Model(
        num_actions=env.action_space.n, 
        num_observations=env.observation_space.shape 
    )
    agent = A2CAgent( model )

    if Path( 'graph' ).exists():
        agent.load( 'graph/' )
        agent.test( env )

    else:
        print( '** missing model file' )

device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
    # This error most likely means that this notebook is not 
    # configured to use a GPU.  Change this in Notebook Settings via the 
    # command palette (cmd/ctrl-shift-P) or the Edit menu.
    device_name = '/device:CPU:0'

print( 'tf version :', tf.__version__ )
print( 'tfp version:', tfp.__version__ )
print( 'devide name:', device_name )

with tf.device( device_name ):
    train( '../../../lambda-asset-corpus/ALL/XAUUSD_1M_ALL.csv' )

predict( '../../../lambda-asset-corpus/ALL/XAUUSD_1M_ALL.csv' )
