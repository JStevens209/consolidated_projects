# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import datetime
import tensorflow as tf
from tensorflow import keras
import tensorflow.keras.layers as kl
import option_pricing.option_pricing as options

print( tf.__version__ )


# %%
dataset = pd.read_csv( '/Users/joshua/source/golang/src/github.com/obolary/lambda-asset-corpus/ALL/XAUUSD_1M_ALL.csv' , ';', names=[ 'date-time','O','H','L','C','V' ] )
dataset['date-time'] =  pd.to_datetime( dataset['date-time'], format='%Y-%m-%d')
dataset = dataset.set_index( ['date-time'] )

close = dataset['C']
daily = close.groupby( by=close.index.date ).apply( lambda x: x[0] )
hist_vol_offset = 0.125
hv = daily.pct_change().rolling( 365 ).std() * ( 252 ** 0.5 ) + hist_vol_offset
hv[0:365] = np.arange( start=0.2, stop=hv[365], step=(hv[365]-0.2)/365 )


# %%
def send_strike( dataset ):
        for closes in dataset[ 'C' ]:
            yield 5 * np.round( ( np.ceil( closes + ( 5 / 2 ) ) ) / 5 )

def send_hv( dataset ):
    for date in dataset[ 'C' ].index:
        yield hv[ datetime.date( date.year, date.month, date.day ) ]

def send_option_price( dataset ):
    days   = 7
    kind   = 'c'
    strike =  send_strike( dataset )
    vol    = send_hv( dataset )
    close  = send_close( dataset )
    for closes in dataset[ 'C' ]:
        yield options.american( kind, next( close ), next(strike), days/365, 0.01, 0.0, next(vol) )

def send_close( dataset ):
    for closes in dataset[ 'C' ]:
        yield closes

def send_data( dataset ):
    opt_price = send_option_price( dataset )
    strikes = send_strike( dataset )
    closes = send_close( dataset )

    for price in opt_price:
        yield ( next(closes) , price )


# %%
model = tf.keras.Sequential([
                             kl.Dense(64, activation= 'relu'),
                             kl.Dense(32, activation= 'relu'),
                             kl.Dense(16, activation= 'relu'),
                             kl.Dense(1, activation= 'relu')
                            ])

model.compile(loss='mean_absolute_error', optimizer='adam')
data = send_data( dataset )


# %%
model.fit(x= data, epochs= 100, verbose= True, use_multiprocessing= False)


# %%
preds = []
for j in np.linspace(800,1000,100000):
  preds.append(model.predict([j]))


# %%
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
fig.set_size_inches(10, 8)
plt.xlabel('imput')
plt.ylabel("output")
plt.plot( y_values, label="trainings data")
plt.plot( np.squeeze(preds), label="predictions")
plt.legend()


# %%
model.summary()


# %%



