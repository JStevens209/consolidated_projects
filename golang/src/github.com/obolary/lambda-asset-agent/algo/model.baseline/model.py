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

def predict( dataset_file ):

    # set up gym and reset
    env = gym.make( 
        'gym_fxcm:fxcm-v4',
        bias_profit=False,
        bias_action=-1, 
        bias_runner=True, 
        margin_ratio=50.0,
        position_spread=2.0,
        dataset_tick_ratio=10000.0,
        dataset_window=1,
        dataset_window_fast=60,
        dataset_window_slow=120,
        dataset_file=dataset_file, 
    )

    # evaluate
    print( "Evaluating..." )
    trigger = 3.0
    enabled = False
    action = 0
    prev_fast_zscore = 0
    done = False
    while not done:
        
        next_ob, _, done, _ = env.step( action )

        fast_zscore = next_ob[0][-1]
        slow_zscore = next_ob[1][-1]
        lots = next_ob[3][-1]

        action = 0
        if lots == 0:

            if prev_fast_zscore < -trigger and fast_zscore >= -trigger and right(enabled, slow_zscore):
                action = 1
            elif prev_fast_zscore > trigger and fast_zscore <= trigger and left(enabled, slow_zscore):
                action = 2

        elif lots > 0:

            if fast_zscore > (trigger-1):
                action = 3
            elif prev_fast_zscore < -trigger and fast_zscore >= -trigger and right(enabled, slow_zscore):
                action = 1

        else:

            if fast_zscore < -(trigger-1):
                action = 3
            elif prev_fast_zscore > trigger and fast_zscore <= trigger and left(enabled, slow_zscore):
                action = 2

        prev_fast_zscore = fast_zscore
        
def left(enabled, value):
    if enabled:
        return value < 0.0
    else:
        return True

def right(enabled, value):
    if enabled:
        return value > 0.0
    else:
        return True

predict( '../../../lambda-asset-corpus/ALL/EURUSD_1M_ALL.csv' )
