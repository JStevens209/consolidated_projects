import gym
from datetime import date, datetime as dt
from dateutil import parser as ps
import time
import asyncio
import signal
import sys
import threading

from absl import logging
from absl import flags

from gym import error, spaces, utils
from gym.utils import seeding

from td.client import TDClient

from ..state import State



class TDGymEnvV1( gym.Env ):

    metadata = { 'render.modes': [ 'human' ] }

    def __init__( self, symbol, CLIENT_ID, REDIRECT_URI, CREDENTIALS_PATH, ACCOUNT_NUMBER ):

        self.symbol = symbol
        self.action_timestamp = 0
        self.access_key_timestamp = time.time()

        # Create a new session using variables imported from context
        self.TDSession = TDClient(
            client_id = CLIENT_ID,
            redirect_uri = REDIRECT_URI,
            credentials_path= CREDENTIALS_PATH,
            account_number= ACCOUNT_NUMBER
        )

        self.account_number = ACCOUNT_NUMBER 
        # Login to the session
        self.TDSession.login()

        # Create a streaming sesion
        self.TDStreamingClient = self.TDSession.create_streaming_session()

        # Subscribes to level one symbol quotes mark price
        self.TDStreamingClient.level_one_quotes(
            symbols=[ self.symbol ],
            fields= list( range( 0, 50 ) )
        )
        self.TDStreamingClient.heartbeat()

        # Intercepts SIGINT or SIGTERM signals to exit gracefully from pipeline and TDSession
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        self.done = False

        self.condition = threading.Condition()
        pipeline = threading.Thread( target= self.start_pipeline )

        pipeline.start()

    # Pipeline to continously stream data from TD
    async def pipeline( self ):
        # Build the Pipeline.
        await self.TDStreamingClient.build_pipeline()

        last_account_call = 0
        heartbeat = 0

        while not self.done:
            with self.condition:
                
                # Start the Pipeline.
                data = await self.TDStreamingClient.start_pipeline()

                if data != None and 'notify' in data:
                    notify = data[ 'notify' ]
                    heartbeat = float( notify[0][ 'heartbeat' ] )
                
                if time.time() - heartbeat > 15 and heartbeat != 0:
                    logging.error( "** Connection to server lost, shutting down" )
                    self.done = True

                # Grab the Data, if there was any. Remember not every message will have `data.`
                if data != None and 'data' in data:
                    heartbeat = time.time()

                    data = data[ 'data' ][0]
                    # Check for Mark in Quote data
                    if data[ 'service' ] == 'QUOTE' and '49' in data[ 'content' ][0].keys():
                        self.state[ 'equity' ][ 'price' ] = data[ 'content' ][0][ '49' ]

                    if time.time() - last_account_call >= 60:

                        # Grabs and a new access token key every 15 minutes
                        if time.time() - self.access_key_timestamp >= 900:
                            self.TDSession.grab_refresh_token()
                            self.access_key_timestamp = time.time()

                        # Set Timestamp
                        last_account_call = time.time()
                        # Get account info
                        accounts = self.TDSession.get_accounts( self.account_number, [ 'positions', 'orders' ])
                        if accounts == None:
                            continue
                        else:
                            accounts = accounts[ 'securitiesAccount' ]
                        
                        # Set account balance to the current tradeable balance
                        self.state[ 'account_balance' ] = accounts[ 'currentBalances' ][ 'cashAvailableForTrading' ]

                        # Sets the number of equity/option lots and the cost of the equity/option
                        self.set_state.set_lots( self.symbol, accounts )
                        self.set_state.update_cost( self.symbol, accounts )

                        # Gets the current option mark price
                        option = self.state[ 'option' ]
                        if option[ 'strike' ] > 0:
                            strikes, option_chain = self.get_option_chains( self.state )
                            for strike in strikes:
                                if float( strike ) == option[ 'strike' ]:
                                    option[ 'price' ] = strikes[ strike ][0][ 'mark' ]
                                    option[ 'days' ] = strikes[ strike ][0][ 'daysToExpiration' ]
                        
                    self.set_state.ready = True
                    self.condition.notifyAll()
                    

        # Runs when a SIGINT or SIGTERM signal is caught, exits gracefully from pipeline and program
        logging.info( "** Unsubscribing...")
        await self.TDStreamingClient.unsubscribe( service = 'LEVELONE_QUOTES' )
        await self.TDStreamingClient.unsubscribe( service = 'LEVELONE_OPTIONS' )

        self.condition.release()
        self.set_state.ready = True

        logging.info( "** Closing Stream...")
        await self.TDStreamingClient.close_stream()

        logging.info( "** Logging Out...")
        self.TDSession.logout()

        logging.info( "** Exiting...")
        sys.exit(0)

    def step( self, action ):
        with self.condition:
            while not self.set_state.ready:
                self.condition.wait()

            if self.done == True:
                return None, 0, True, {}

            s, done = self._state( action )
            r = self._reward()

            self.set_state.ready = False

            return s, r, done, {}

    def reset(self):

        self.set_state = State( self.TDSession )
        self.state = self.set_state.state
        
        return self.state

    def render(self, mode='human'):

        pass

    def close(self):

        pass

    def _state( self, action ):
        # Checks if the action is trying to do more than 1 trade per minute
        # Does this by checking if the agent is not holding, then comparing timestamp of the last action to current timestamp
        if action[ 'kind' ] != 'hold' and ( time.time() - self.action_timestamp < 30 ):
            logging.error( "** Agent tried to do more than one trade in 1 minute" )
            return self.state, False

        elif action[ 'kind' ] != 'hold':
            self.action_timestamp = time.time()

        option = self.state[ 'option' ]
        equity = self.state[ 'equity' ]
        kind = option[ 'kind' ]

        valid_option_order = False

        keys = action.keys()

        if 'extrinsic' in keys:
            # if there was a buy or sell
            # check if the action was already performed,
            # then update the state appropriately
            if 'option' in keys and action[ 'kind' ] == 'open':
            # Check if the order that the action is giving is valid, given the current state
                option_shorted     = False
                action_shorting    = False

                # If lots is negative, the option was shorted, if it is positive the option was longed
                if option[ 'lots' ] < 0:
                    option_shorted = True

                # selling_to_open is the same thing as a short, 
                if action[ 'extrinsic' ] == 'sell' and action[ 'kind' ] == 'open':
                    action_shorting = True
  
                #               [ days, strike, kind, true/false (Shorting or not) ]
                action_option = [ action[ 'option' ][ 'date' ], action[ 'option' ][ 'strike' ], action[ 'option' ][ 'kind' ], action_shorting ]
                state_option  = [ option[ 'date' ], option[ 'strike' ], option[ 'kind' ], option_shorted ]
        
                # The action is giving a valid option order, when either there is no active option, 
                # or the strike price, type, expiration time, and  of the option are all the same
                 # or if the order is only closing, and not opening
                if option[ 'lots' ] == 0 or action[ 'option' ][ 'lots' ] == 0 or action_option == state_option or action[ 'kind' ] == 'close':
                    valid_option_order = True
            else:
                valid_option_order = True

            qualified_actions = [
                # { open/close/hold, buy/sell, valid_option, action }
                    [ 'hold', '', '', None ],
                    ['open', 'buy', True, self.buy_to_open ],
                    [ 'open', 'buy', False, 'log_error' ],
                    [ 'open', 'sell', True, self.sell_to_open ],
                    [ 'open', 'sell', False, 'log_error' ],
                    [ 'close', 'buy', True, self.buy_to_close ],
                    [ 'close', 'sell', True, self.sell_to_close ],
                ]

            current_state = [ action[ 'kind' ], action[ 'extrinsic' ], valid_option_order ]

            for actions in qualified_actions:
                    if current_state == actions[0:3]:
                        if actions[3] == 'log_error':
                            logging.info( '** Logic Error: Agent passed Invalid option order. ' )
                        else:
                            actions[3]( action )
                            if action[ 'kind' ] != 'hold':
                                logging.info( f"** Agent performed the action {actions[3].__name__}")
        
        return self.state, False

    def _reward( self) :
        return 0.0 

    def signal_handler(self, sig, frame):
        self.done = True

    def buy_to_open( self, action ):
        keys = action.keys()
        order = {}
        
        # If Agent wants to buy equity, fill an order to buy equity
        if 'equity' in keys: 
            if action[ 'equity' ][ 'lots' ] >= 0:
                equity = self.state[ 'equity' ]
                equity_order = action[ 'equity' ]
                order = {
                    "orderType": "MARKET",
                    "session": "NORMAL",
                    "duration": "DAY",
                    "orderStrategyType": "SINGLE",
                    "orderLegCollection": [{
                        "instruction": "BUY",
                        "quantity": ( equity_order[ 'lots' ] * 100 ),
                        "instrument": {
                            "symbol": self.symbol,
                            "assetType": "EQUITY" 
                        }
                    }]
                }            

                self.TDSession.place_order( self.account_number, order )
        
            elif action[ 'equity' ][ 'lots' ] > 0:
                logging.error( f"** Agent tried to Buy to Open a short position. Equity lots: {action[ 'equity' ][ 'lots' ]}")


        # If Agent wants to buy option, get the option chain, check for Agent strike in chain, then fill order
        if 'option' in keys: 
            if action[ 'option' ][ 'lots' ] >= 0:
            
                option_order= action[ 'option' ]
                symbol = option_order[ 'symbol' ]
                
                if symbol != "":
                    order = {
                        "complexOrderStrategyType": "NONE",
                        "orderType": "MARKET",
                        "session": "NORMAL",
                        "duration": "DAY",
                        "orderStrategyType": "SINGLE",
                        "orderLegCollection": [{
                            "instruction": "BUY_TO_OPEN",
                            "quantity":option_order[ 'lots' ],
                            "instrument": {
                                "symbol": symbol,
                                "assetType": "OPTION"
                            }
                        }]
                    }

                    self.TDSession.place_order( self.account_number, order )

                else:
                    logging.info( "** Agent passed unknown strike price" )

            elif action[ 'option' ][ 'lots' ] < 0:
                logging.error( f"** Agent tried to Buy to Open a short position. Option lots: {action[ 'option' ][ 'lots' ]}")


    def sell_to_open( self, action ):
        keys = action.keys()
        order = {}

        if 'equity' in keys:
            if action[ 'equity' ][ 'lots' ] <= 0:
                equity_order= action[ 'equity' ]

                order = {
                    "orderType": "MARKET",
                    "session": "NORMAL",
                    "duration": "DAY",
                    "orderStrategyType": "SINGLE",
                    "orderLegCollection": [{
                        "instruction": "SELL_SHORT",
                        "quantity": ( equity_order[ 'lots' ] * 100 ),
                        "instrument": {
                            "symbol": self.symbol,
                            "assetType": "EQUITY"
                        }
                    }]
                }

                self.TDSession.place_order( self.account_number, order )
        
            elif action[ 'equity' ][ 'lots' ] > 0:
                logging.error( f"** Agent tried to Sell Short a long position. Equity lots: {action[ 'equity' ][ 'lots' ]}")

        if 'option' in keys:
            if action[ 'option' ][ 'lots' ] <= 0:
                option_order = action[ 'option' ]

                symbol = option_order[ 'symbol' ]

                if symbol != "":
                    order = {
                            "complexOrderStrategyType": "NONE",
                            "orderType": "MARKET",
                            "session": "NORMAL",
                            "duration": "DAY",
                            "orderStrategyType": "SINGLE",
                            "orderLegCollection": [{
                                "instruction": "SELL_TO_OPEN",
                                "quantity": option_order[ 'lots' ],
                                "instrument": {
                                    "symbol": symbol,
                                    "assetType": "OPTION"
                                }
                            }]
                        }

                    self.TDSession.place_order( self.account_number, order )

                else:
                    logging.info( "** Agent passed unknown strike price" )

            elif action[ 'option' ][ 'lots' ] > 0:
                logging.error( f"** Agent tried to Sell to Open a long position. Option lots: {action[ 'option' ][ 'lots' ]}")

        

    def buy_to_close( self, action ):
        keys = action.keys()

        if 'equity' in keys:
            if action[ 'equity' ][ 'lots' ] < 0:
                equity_order = action[ 'equity' ]
                order = {
                    "orderType": "MARKET",
                    "session": "NORMAL",
                    "duration": "DAY",
                    "orderStrategyType": "SINGLE",
                    "orderLegCollection": [{
                        "instruction": "BUY_TO_COVER",
                        "quantity": ( equity_order[ 'lots' ] * 100 ),
                        "instrument": {
                            "symbol": self.symbol,
                            "assetType": "EQUITY"
                        }
                    }]
                }

                self.TDSession.place_order( self.account_number, order )

            elif action[ 'equity' ][ 'lots' ] > 0:
                logging.error( f"** Agent tried to Buy to Close a long position. Equity lots: {action[ 'equity' ][ 'lots' ]}")

        if 'option' in keys:
            if action[ 'option' ][ 'lots' ] < 0:
                option_order = action[ 'option' ]
                symbol = option_order[ 'symbol' ]

                order = {
                    "complexOrderStrategyType": "NONE",
                    "orderType": "MARKET",
                    "session": "NORMAL",
                    "duration": "DAY",
                    "orderStrategyType": "SINGLE",
                    "orderLegCollection": [{
                        "instruction": "BUY_TO_CLOSE",
                        "quantity": option_order[ 'lots' ],
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "OPTION"
                        }
                    }]
                }

                self.TDSession.place_order( self.account_number, order )

            elif action[ 'option' ][ 'lots' ] > 0:
                logging.error( f"** Agent tried to Buy to Close a long position. Option lots: {action[ 'option' ][ 'lots' ]}")

    def sell_to_close( self, action ):
        keys = action.keys()

        if 'equity' in keys:
            if action[ 'equity' ][ 'lots' ] > 0:
                equity_order= action[ 'equity' ]

                order = {
                    "orderType": "MARKET",
                    "session": "NORMAL",
                    "duration": "DAY",
                    "orderStrategyType": "SINGLE",
                    "orderLegCollection": [{
                        "instruction": "SELL",
                        "quantity": ( equity_order[ 'lots' ] * 100 ),
                        "instrument": {
                            "symbol": self.symbol,
                            "assetType": "EQUITY"
                        }
                    }]
                }

                self.TDSession.place_order( self.account_number, order )

            elif action[ 'equity' ][ 'lots' ] < 0:
                logging.error( f"** Agent tried to Sell to Close a short position. Equity lots: {action[ 'equity' ][ 'lots' ]}")

        if 'option' in keys:
            if action[ 'option' ][ 'lots' ] > 0:
                option_order= action[ 'option' ]
                symbol = option_order[ 'symbol' ]

                order = {
                    "complexOrderStrategyType": "NONE",
                    "orderType": "MARKET",
                    "session": "NORMAL",
                    "duration": "DAY",
                    "orderStrategyType": "SINGLE",
                    "orderLegCollection": [{
                        "instruction": "SELL_TO_CLOSE",
                        "quantity": option_order[ 'lots' ],
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "OPTION"
                        }
                    }]
                }

                self.TDSession.place_order( self.account_number, order )

            elif action[ 'option' ][ 'lots' ] < 0:
                logging.error( f"** Agent tried to Sell to Close a short position. Option lots: {action[ 'option' ][ 'lots' ]}")
 
    # Recieves and parses an option chain for the given action at the closest date to given date
    def get_option_chains( self, action ):
        keys = action.keys()
        
        # Checks if an option order was given
        if 'option' not in keys:
            logging.info( "** Invalid order given to get option chain." )
            return None, None

        option_order = action[ 'option' ]

        option_kind = ''
        if option_order[ 'kind' ] == 'c':
            option_kind = 'CALL'
        elif option_order[ 'kind' ] == 'p':
            option_kind = 'PUT'

        # Parses Agent's date into a datetime object, then changes it to needed format. 
        # ps.parser is limited and deals with ambiguous cases by assuming month first
        date = ps.parse( option_order[ 'date'] ).isoformat()

        option_chain = {
            'symbol': self.symbol,
            'contractType': option_kind,
            'strikeCount': 14,
            'includeQuotes': 'TRUE',
            'strategy': 'SINGLE',
            'optionType': 'ALL',
            'toDate': date
        } 
        
        option_chain = self.TDSession.get_options_chain( option_chain )
        strikes = list( option_chain[ 'callExpDateMap' ].values() )[0]

        return strikes, option_chain

    def start_pipeline( self ):
        asyncio.run( self.pipeline() )

