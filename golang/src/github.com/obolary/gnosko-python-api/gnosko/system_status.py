from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time
import warnings
import requests
import json

from pathlib import Path
from absl import logging
from absl import flags
from absl import app

import matplotlib as mpl
from matplotlib import pylab as plt

import numpy as np
import pandas as pd

from datetime import datetime
from datetime import timedelta
from datetime import timezone

# System Status Tracking
#   Example Usage:
#
#   system_status = SystemStatus( url, client_id, client_secret )
#   system_status.begin( system_type, system_name )
#   ...
#   system_status.add_message_info( 'starting system' )
#   system_status.commit()
#   ...
#   system_status.set_status( 'opened_covered_call' )
#   system_status.set_balance( balance )
#   system_status.set_position( '-10 SLV_072021C16, +1000 SLV' )
#   system_status.set_position_value( value )
#   system_status.commit()
#   ...
#   system_status.add_message_error( 'connection failed,...' )
#   system_status.commit()
#   ...
#
class SystemStatus():

    def __init__( self, gnosko_url, gnosko_client_id, gnosko_client_secret, **kwargs ):
        logging.info( '** initializing system status tracking,...' )

        self.param_last_message_max = 5
        self.__dict__.update( **kwargs )

        self.gnosko_url = gnosko_url
        self.gnosko_client_id = gnosko_client_id
        self.gnosko_client_secret = gnosko_client_secret

        self.tokens = None
        self.access_token = None
        self.access_token_expires_in = None

        self.system_status = None
        self.dirty = False

    # bookmark begin
    # update local version from server given the name and type
    # e.g., system_type='td-ameritrade-session-state', system_name='covered-call-naked-put-v1'
    def begin( self, system_type, system_name ):

        # obtain or refresh access_token
        self._login()

        # TODO - check for td-ameritrade credentials    
        # curl -v -H 'Authorization: Bearer 1qeN1UCGTaaFkaxI5GeQGA' -H 'Content-Type: application/json' -d '{"$condition":{"objectmeta.content":"td-ameritrade-session-state"}}' -X POST https://gnosko.obolary.com/gnosko/1.0/object:query
        filter = {
            '$condition': {
                'objectmeta.content': system_type,
                'objectmeta.contenttype': system_name
            }
        }
        system_status_response = requests.post( 
            self.gnosko_url + '/gnosko/1.0/object:query',
            headers = {
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json'
            },
            json = filter
        )
        if system_status_response.status_code < 300:

            system_status_response_json = system_status_response.json()
            if len( system_status_response_json ) > 0:

                self.system_status = system_status_response_json[ 0 ]
                logging.info( f'** system status, {self.system_status}' )

            else:

                self.system_status = {
                    '$content': system_type,
                    '$content_type': system_name
                }
                system_status_response = requests.post(
                    self.gnosko_url + '/gnosko/1.0/object:create',
                    headers = {
                        'Authorization': 'Bearer ' + self.access_token,
                        'Content-Type': 'application/json'
                    },
                    json = self.system_status
                )
                if system_status_response.status_code < 300:

                    self.system_status = system_status_response.json()

                    attach_request = { 'object_ids': [ self.system_status[ 'id' ] ] }
                    attach_response = requests.post(
                        self.gnosko_url + '/gnosko/1.0/label:attach/eyJlIjoiNWM3MDI0NWYxZjZkNzMwMDAxM2RkY2I2IiwiayI6ImxhYmVsIn0=',
                        headers = {
                            'Authorization': 'Bearer ' + self.access_token,
                            'Content-Type': 'application/json'
                        },
                        json = attach_request
                    )
                    if attach_response.status_code >= 300:

                        logging.error( f'** failed to make new status global, {attach_response}' )

                else:

                    system_status_response_json = system_status_response.json()
                    raise Exception( f'** failed to create new status, {system_status_response_json}' )

        else:

            raise Exception( f'** failed to find persistent status object, {system_status_response}' )

    # bookmark checkpoint commit
    def commit( self ):
        logging.info( '** update system status,...' )

        if self.dirty:

            self.dirty = False
            system_status_response = requests.post(
                self.gnosko_url + '/gnosko/1.0/object:set/' + self.system_status[ 'id' ],
                headers = {
                    'Authorization': 'Bearer ' + self.access_token,
                    'Content-Type': 'application/json'
                },
                json = self.system_status
            )
            if system_status_response.status_code < 300:

                self.system_status = system_status_response.json()

            else:

                logging.error( f'** failed to update status object, {system_status_response}' )

    # bookmark end (i.e., commit and initialize for new begin)
    def end( self ):

        self.commit()
        self.system_status = None
        self.dirty = False

    # update state
    def set_status( self, state_name ):
        logging.info( f'** set state name, {state_name}' )

        if self.system_status is not None:
            self.system_status[ 'status' ] = state_name
            self.dirty = True

    # position state
    def set_position( self, position_name ):
        logging.info( f'** set position name, {position_name}' )

        if self.system_status is not None:
            self.system_status[ 'position' ] = position_name
            self.dirty = True

    # update current balance
    def set_balance( self, balance ):
        logging.info( f'** set balance, {balance}' )

        if self.system_status is not None:
            self.system_status[ 'balance' ] = balance
            self.dirty = True
   
    # add profit and balance history array
    def add_history( self, profit, balance ):
        logging.info( f'** set profit amount from recent close, {profit} for new balance, {balance}' )

        if self.system_status is not None:

            if 'history' not in self.system_status:
                self.system_status[ 'history' ] = []

            #now = datetime.now().isoformat()
            now = datetime.now().strftime( '%d/%m/%y %H:%M:%S' )
            history = self.system_status[ 'history' ]
            history.append( [ now, profit, balance ] )
            self.system_status[ 'history' ] = history
            self.dirty = True
    
    # clear the history array
    def clear_history( self ):

        if self.system_status is not None:

            self.system_status[ 'history' ] = []
            self.dirty = True

    # add information message
    def add_message_info( self, message ):

        self._add_message( f'(INFO)  {message}' )

    # add information message
    def add_message_error( self, message ):

        self._add_message( f'(ERROR) {message}' )

    # #######################################################
    # begin private section

    # login to the gnosko api
    def _login( self ):

        now = datetime.now()
        if self.access_token is None or now > self.access_token_expires_in:
            logging.info( '** login to gnosko api' )

            # connect to gnosko
            access_token_response = requests.post( 
                self.gnosko_url + '/auth/2.0/token', 
                data={ 'grant_type': 'client_credentials' },
                allow_redirects=False,
                auth=( self.gnosko_client_id, self.gnosko_client_secret )
            )

            # print response
            logging.info( f'** response, {access_token_response.text}' )
            self.tokens = access_token_response.json()
            if 'access_token' in self.tokens:

                self.access_token = self.tokens[ 'access_token' ]

                expires_in = self.tokens[ 'expires_in' ]
                self.access_token_expires_in = now + timedelta( seconds=expires_in )

                logging.info( f'** gnosko access-token, {self.access_token} expires in {expires_in} seconds' )

            else:

                raise Exception( f'** missing access-token, {self.tokens}' )

    # add message to last messages array
    def _add_message( self, message ):

        now = datetime.now()
        message = f'{now}: {message}'
        logging.info( f'** add last message, {message}' )

        if self.system_status is not None:

            if 'last_messages' not in self.system_status:
                self.system_status[ 'last_messages' ] = []

            last_messages = self.system_status[ 'last_messages' ]
            last_messages.append( message )
            last_messages = last_messages[-self.param_last_message_max:]
            self.system_status[ 'last_messages' ] = last_messages
            self.dirty = True
