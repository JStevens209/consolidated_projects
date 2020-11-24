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
        # the axis = -1 parameter says that the resulting dimension should be 1D
        result = tf.squeeze( tf.random.categorical( logits, 1 ), axis=-1 )
        return result

class Model( tf.keras.Model ):

    def __init__( self, **kwargs ):
        super().__init__( 'mlp_policy' )

        # attributes
        self.num_actions = 4
        self.num_observations = (8,)
        self.dropout = 0.2

        # overwrite attributes any given args
        for key in dir(self):
            if key in kwargs.keys():
                v = kwargs.pop( key )
                setattr( self, key, v )

        # common
        self.common = km.Sequential([
            # CNN expects (samples,timesteps,features)
            # TODO - use larger window, but break in to 256 size samples, e.g., 2048, or 8 samples
            kl.Reshape( (1, 256, 1) ),
            # Batch Size must be divisible by 24
            kl.TimeDistributed( kl.Conv1D( 256, kernel_size=5, input_shape=(24, None, 256, 1) ) ),
            # NOTE - BatchNormalization causes the LSTM loss to explode
            kl.TimeDistributed( kl.LayerNormalization() ),
            kl.TimeDistributed( kl.MaxPool1D( 2 ) ),
            kl.TimeDistributed( kl.Flatten() ),
        ])

        # policy logits
        self.hidden1 = km.Sequential([
            kl.Bidirectional( kl.LSTM( 128, return_sequences=True ) ),
            kl.Bidirectional( kl.LSTM( 256 ) ),
            kl.Flatten(),
            kl.Dense( 256, activation='relu' ),            
            kl.Dense( 128, activation='relu' ),            
            kl.Dense( 64, activation='relu' ),            
        ])
        self.logits = kl.Dense( self.num_actions, activation='softmax' )

        # value estimate
        self.hidden2 = km.Sequential([
            kl.Flatten(),
            kl.Dense( 1024, activation='relu' ),
            kl.Dense( 512, activation='relu' ),
            kl.Dense( 256, activation='relu' ),
        ])
        self.value = kl.Dense( 1, activation='linear' )

        # pi( a | s )?
        self.dist = ProbabilityDistribution()
        
    def call( self, inputs, training=False ):


        # inputs is a numpy array, convert to Tensor
        x = tf.convert_to_tensor( inputs, dtype=tf.float32 )
        #if training:
        #    x = tf.nn.dropout( x, self.dropout )

        # common
        common = self.common( x )

        # action
        hidden_logits = self.hidden1( common )
        logits = self.logits( hidden_logits )

        # value
        hidden_values = self.hidden2( common )
        value = self.value( hidden_values )

        return logits, value

    def action_value( self, obs ):

        # executes call() under the hood
        logits, value = self.predict( obs )
        action = self.dist.predict( logits )

        # a simpler option, will become clear later why we don't use it
        # action = tf.random.categorical( logits, 1 )
        return np.squeeze( action, axis=-1 ), np.squeeze( value, axis=-1 )

class A2CAgent:

    def __init__(self, model):

        # hyperparameters for loss terms
        self.params = { 'value': 0.5, 'entropy': 0.0007, 'gamma': 0.99 }

        self.model = model
        self.model.compile(

            # a popular optimizer (simular to adam) that uses
            # an adaptive learning rate, see https://towardsdatascience.com/understanding-rmsprop-faster-neural-network-learning-62e116fcf29a
            optimizer = koz.RMSprop( lr=0.0007 ),

            # define separate losses for policy logits and value estimate
            loss=[self._logits_loss, self._value_loss]
        )

    def train( self, env, batch_sz=48, updates=1024 ):

        # storage helpers for a single batch of data
        actions = np.empty( (batch_sz,), dtype=np.int32 )
        rewards, dones, values = np.empty( (3, batch_sz) )
        observations = np.empty( (batch_sz,) + env.observation_space.shape )

        # training loop: collect samples, send to optimizer, repeat updates times
        ep_rews = [0.0]
        next_obs = env.reset()
        for update in range( updates ):

            for step in range( batch_sz ):

                observations[step] = next_obs.copy()
                actions[step], values[step] = self.model.action_value( next_obs[None, :] )
                next_obs, rewards[step], dones[step], _ = env.step( actions[step] )

                ep_rews[-1] += rewards[step]
                if dones[step]:
                    ep_rews.append( 0.0 )
                    next_obs = env.reset()

            _, next_value = self.model.action_value( next_obs[None, :] )
            returns, advs = self._returns_advantages( rewards, dones, values, next_value )

            # a trick to input actions and advantages through same API
            acts_and_advs = np.concatenate( [actions[:, None], advs[:, None]], axis=-1 )

            # performs a full training step on the collected batch
            # note: no need to mess around with gradients, Keras API handles it
            losses = self.model.train_on_batch( observations, [acts_and_advs, returns] )
            print( update, losses )

        return ep_rews

    def _returns_advantages( self, rewards, dones, values, next_value ):

        # next_value is the bootstrap value estimate of a future state (the critic)
        returns = np.append( np.zeros_like(rewards), next_value, axis=-1 )

        # returns are calculated as discounted sum of future rewards
        for t in reversed( range( rewards.shape[0] ) ):
            returns[t] = rewards[t] + self.params['gamma'] * returns[t+1] * (1-dones[t])
        returns = returns[:-1]

        # advantages are returns - baseline, value estimates in our case
        advantages = returns - values
        return returns, advantages

    def test(self, env, render=True):

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

current_balance = 10000.00

def balance_update( balance ):
    global current_balance
    current_balance = balance

def train( dataset_file, reward_func='mean' ):
    global current_balance

    # set up gym and reset
    env = gym.make( 
        'gym_fxcm:fxcm-v1',
        bias_profit=False, 
        bias_action=-1, 
        bias_runner=False, 
        reward_func=reward_func, 
        reward_return_window=1,
        dataset_file=dataset_file, 
        balance_callback=balance_update
    )
    env.reset()

    # create and train
    print( "Training..." )
    model = Model( num_actions = env.action_space.n, num_observations = env.observation_space.shape )
    agent = A2CAgent( model )

    if Path( 'graph' ).exists():
        print( 'Load previous before training,...')
        agent.load( 'graph/' )

    updates=10
    previous_balance = current_balance
    for i in range( 10000 ): 
        
        raw_ep = agent.train( env, updates=updates, batch_sz=48 )
        # if raw_ep[-1] < 0.0 or current_balance < previous_balance:
        if current_balance < previous_balance:
            print( '** RESET: RAW_EP,', raw_ep[-1], 'UPDATE SIZE,', updates, 'AND EXPECTED BALANCE,', previous_balance, 'VS CURRENT,', current_balance )
            _ = env.reset()
        else:
            print( '** CONTINUE: RAW_EP,', raw_ep[-1], 'UPDATE SIZE,', updates, 'AND EXPECTED BALANCE,', previous_balance, 'VS CURRENT,', current_balance )
            previous_balance = current_balance
            updates = updates + 10
        
        if i % 10 == 0:
            print( '** SAVING ITERATION', i, 'EP', raw_ep )
            agent.save( 'graph/')

def predict( dataset_file, reward_func='mean' ):

    # set up gym and reset
    env = gym.make( 
        'gym_fxcm:fxcm-v1', 
        bias_profit=True, 
        bias_action=1, 
        bias_runner=False, 
        reward_func=reward_func, 
        reward_return_window=1,
        dataset_file=dataset_file, 
        balance_callback=balance_update
    )
    env.reset()

    # evaluate
    print( "Evaluating..." )
    model = Model( num_actions = env.action_space.n, num_observations = env.observation_space.shape )
    agent = A2CAgent( model )

    if Path( 'graph' ).exists():
        agent.load( 'graph/' )
        agent.test( env )

    else:

        print( 'missing model file' )

#reward_func='sortino'
#reward_func='calmar'
#reward_func='omega'
#reward_func='mean'
reward_func='profit'

#train( '../../../obo-corpus/ALL/ALL.csv', reward_func )
predict( '../../../obo-corpus/HISTDATA_COM_ASCII_XAUUSD_M12018/DAT_ASCII_XAUUSD_M1_2018.csv', reward_func )

