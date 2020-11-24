from IPython import get_ipython


import gym
import logging
import numpy as np
from pandas import Timedelta
import matplotlib.pyplot as plt

import tensorflow as tf
import tensorflow.keras.layers as kl
import tensorflow.keras.losses as kls
import tensorflow.keras.optimizers as ko
import tensorflow.keras.models as km

#get_ipython().run_line_magic('matplotlib', 'inline')

print("TensorFlow Ver: ", tf.__version__)

class ProbabilityDistribution(tf.keras.Model):
    def call(self, logits, **kwargs):
        # Sample a random categorical action from the given logits.
        return tf.squeeze(tf.random.categorical(logits, 1), axis=-1)


class Model(tf.keras.Model):
    def __init__(self, num_actions, num_observations ):
      
        super().__init__('model')

        # attributes
        self.num_actions = num_actions
        self.num_observations = num_observations

        # common layers
        self.common = km.Sequential([
            kl.Bidirectional( kl.LSTM( self.num_observations, return_sequences=True ) ),
            kl.Bidirectional( kl.LSTM( self.num_observations * 2 ) )
        ])

        # policy logits
        self.hidden1 = km.Sequential([
            kl.Dense( 65536, activation='relu' ),            
            kl.Dense( 4096, activation='relu' ),            
            kl.Dense( 256, activation='relu' ),
        ])
        self.logits = kl.Dense( self.num_actions, activation='softmax' )

        # value estimate
        self.hidden2 = km.Sequential([
            kl.Dense( 65536, activation='relu' ),            
            kl.Dense( 4096, activation='relu' ),            
            kl.Dense( 256, activation='relu' ),            
        ])
        self.value = kl.Dense( 1, activation='linear' )

        # pi( a | s )?
        self.dist = ProbabilityDistribution()

    def call(self, inputs, training=False, **kwargs):
        dropout = 0.0

        # inputs is a numpy array, convert to Tensor
        x = tf.convert_to_tensor( inputs, dtype=tf.float32 )
        if training:
            x = tf.nn.dropout( x, dropout )

        # common
        common = self.common( x )
        if training:
            common = tf.nn.dropout( common, dropout )

        # action
        hidden_logits = self.hidden1( common )
        if training:
            hidden_logits = tf.nn.dropout( hidden_logits, dropout )
        logits = self.logits( hidden_logits )

        # value
        hidden_values = self.hidden2( common )
        if training:
            hidden_values = tf.nn.dropout( hidden_values, dropout )
        value = self.value( hidden_values )

        return logits, value

    def action_value(self, obs):
        # Executes `call()` under the hood.
        logits, value = self.predict_on_batch(obs)
        action = self.dist.predict_on_batch(logits)
 
        # Another way to sample actions:
        #   action = tf.random.categorical(logits, 1)
        # Will become clearer later why we don't use it.
        return np.squeeze(action, axis=-1), np.squeeze(value, axis=-1)

class A2CAgent:
    def __init__(self, model, lr=7e-4, gamma=0.99, value_c=0.5, entropy_c=1e-4):
        # `gamma` is the discount factor; coefficients are used for the loss terms.
        self.gamma = gamma
        self.value_c = value_c
        self.entropy_c = entropy_c

        self.model = model
        self.model.compile(
        optimizer=ko.RMSprop(lr=lr),
        # Define separate losses for policy logits and value estimate.
        loss=[self._logits_loss, self._value_loss])

    def train(self, env, batch_sz=64, updates=250):
        # Storage helpers for a single batch of data.
        actions = np.empty((batch_sz, ), dtype=np.int32)
        rewards, dones, values = np.empty((3, batch_sz))
        observations = np.empty((batch_sz, ) + env.observation_space.shape)

        # Training loop: collect samples, send to optimizer, repeat updates times.
        ep_rewards = [0.0]
        next_obs = env.reset()

        for update in range(updates):
            for step in range(batch_sz):
                observations[step] = next_obs.copy()
                actions[step], values[step] = self.model.action_value(next_obs[None, :])
                next_obs, rewards[step], dones[step], _ = env.step( actions[ step ] )

                ep_rewards[-1] += rewards[step]

                if dones[step]:
                    ep_rewards.append(0.0)
                    next_obs = env.reset()

                    logging.info("Episode: %03d, Reward: %03d" % (len(ep_rewards) - 1, ep_rewards[-2]))

        _, next_value = self.model.action_value(next_obs[None, :])
        returns, advs = self._returns_advantages(rewards, dones, values, next_value)

        # A trick to input actions and advantages through same API.
        acts_and_advs = np.concatenate([actions[:, None], advs[:, None]], axis=-1)

        # Performs a full training step on the collected batch.
        # Note: no need to mess around with gradients, Keras API handles it.
        losses = self.model.train_on_batch(observations, [acts_and_advs, returns])
        logging.debug("[%d/%d] Losses: %s" % (update + 1, updates, losses))

        return ep_rewards

    def _returns_advantages(self, rewards, dones, values, next_value):
        # `next_value` is the bootstrap value estimate of the future state (critic).
        returns = np.append(np.zeros_like(rewards), next_value, axis=-1)

        # Returns are calculated as discounted sum of future rewards.
        for t in reversed(range(rewards.shape[0])):
            returns[t] = rewards[t] + self.gamma * returns[t + 1] * (1 - dones[t])

        returns = returns[:-1]

        # Advantages are equal to returns - baseline (value estimates in our case).
        advantages = returns - values

        return returns, advantages

    def _value_loss(self, returns, value):
        # Value loss is typically MSE between value estimates and returns.
        return self.value_c * kls.mean_squared_error(returns, value)

    def _logits_loss(self, actions_and_advantages, logits):
        # A trick to input actions and advantages through the same API.
        actions, advantages = tf.split(actions_and_advantages, 2, axis=-1)

        # Sparse categorical CE loss obj that supports sample_weight arg on `call()`.
        # `from_logits` argument ensures transformation into normalized probabilities.
        weighted_sparse_ce = kls.SparseCategoricalCrossentropy(from_logits=True)

        # Policy loss is defined by policy gradients, weighted by advantages.
        # Note: we only calculate the loss on the actions we've actually taken.
        actions = tf.cast(actions, tf.int32)
        policy_loss = weighted_sparse_ce(actions, logits, sample_weight=advantages)

        # Entropy loss can be calculated as cross-entropy over itself.
        probs = tf.nn.softmax(logits)
        entropy_loss = kls.categorical_crossentropy(probs, probs)

        # We want to minimize policy and maximize entropy losses.
        # Here signs are flipped because the optimizer minimizes.
        return policy_loss - self.entropy_c * entropy_loss


# Verify everything works by sampling a single action.
env = gym.make( 
    'gym_fxcm:fxcm-v5',
    bias_profit=False,
    bias_action=0, 
    bias_runner=False, 
    dataset_file= '/Users/joshua/source/golang/src/github.com/obolary/lambda-asset-corpus/ALL/XAUUSD_1M_ALL.csv' )
    
model = Model(
    num_actions= env.action_space.n,
    num_observations=env.observation_space.shape[0] 
            )

# set to logging.WARNING to disable logs or logging.DEBUG to see losses as well

agent = A2CAgent(model)

rewards_history = agent.train(env)
print("Finished training! Testing...")






