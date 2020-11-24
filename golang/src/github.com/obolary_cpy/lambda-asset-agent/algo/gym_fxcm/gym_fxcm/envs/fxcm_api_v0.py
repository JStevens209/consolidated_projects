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

class Fxcm( gym.Env ):

  metadata = { 'render.modes': [ 'human' ] }

  def __init__(self, **kwargs):
    
    pass

  def step(self, action):

    s, done = self._state( action )
    r = self._reward()
    return s, r, done, {}

  def reset(self):

    s, _ = self._state( action = 0 )
    return s

  def render(self, mode='human'):

    pass

  def close(self):
    
    pass

  def _state(self,action):

    return np.asarray( self.queue ), False

  def _reward( self) :

    return 0.0 
