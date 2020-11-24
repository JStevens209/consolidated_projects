from itertools import combinations
from absl import logging
import itertools
import pprint as pp


class State():

    def __init__( self, session, state= None ):

        self.ready = False
        
        self.state = {
            # Holds the current session for the agent to use if needed
            'session' : session,

            # Holds account balance 
            'account_balance' : -1.0,

            # Holds current state of model
            'status': 'unknown',

            # equity position (only one type, but many lots)
            # note, the lots are in multiples of 100, negative means we've shorted, 
            #       and the cost is bid and price is ask. lots positive have the reverse
            'equity': {
                'lots': 0,
                'cost': -1.0,
                'price': -1.0
            },

            # option position (only one type, but many lots)
            # note, the lots are in number of contracts, negative means we've shorted
            #       and the cost is bid and price is ask. lots positive have the reverse
            'option': {
                'kind': 'c',
                'lots': 0,
                'cost': -1.0,
                'strike': -1.0,
                'date': '2020-01-01',
                'days': -1,
                'price': -1.0,
            }
        }

        if state != None:
            self.state = state

    def set_lots( self, symbol, accounts ):

        for position in accounts[ 'positions' ]:
            instrument = position[ 'instrument' ]
            equity = self.state[ 'equity' ]
            option = self.state[ 'option' ]

            # If it is an account position, it is either long or short, it will never be neither
            short_position = False
            if position[ 'shortQuantity' ] > 0:
                short_position = True

            # Gets the equity lots from the account
            if instrument[ 'assetType' ] == 'EQUITY' and instrument[ 'symbol' ] == symbol and not short_position:
                equity[ 'lots' ] = position[ 'longQuantity' ] / 100
            if instrument[ 'assetType' ] == 'EQUITY' and instrument[ 'symbol' ] == symbol and short_position:
                equity[ 'lots' ] = -1 * position[ 'shortQuantity' ] / 100
            
            # Gets the option lots from the account
            if instrument[ 'assetType' ] == 'OPTION' and instrument[ 'underlyingSymbol' ] == symbol and not short_position:
                option[ 'lots' ] = position[ 'longQuantity' ]
            if instrument[ 'assetType' ] == 'OPTION' and instrument[ 'underlyingSymbol' ] == symbol and short_position:
                option[ 'lots' ] = position[ 'shortQuantity' ]
        
        # Gets any partially filled lots
        if 'orderStrategies' in accounts.keys():
            for orders in accounts[ 'orderStrategies' ]:
                if orders[ 'status' ] == 'WORKING' and orders[ 'filledQuantity' ] > 0:
                    if orders[ 'orderLegCollection' ][0][ 'instruction' ] in [ "BUY", "BUY_TO_COVER" ]:
                        self.state[ 'equity' ][ 'lots' ] += orders[ 'filledQuantity' ]
                    if orders[ 'orderLegCollection' ][0][ 'instruction' ] in [ "SELL", "SELL_SHORT" ]:
                        self.state[ 'equity' ][ 'lots' ] -= orders[ 'filledQuantity' ]

                    if orders[ 'orderLegCollection' ][0][ 'instruction' ] in [ "BUY_TO_OPEN", "BUY_TO_CLOSE" ]:
                        self.state[ 'option' ][ 'lots' ] += orders[ 'filledQuantity' ]
                    if orders[ 'orderLegCollection' ][0][ 'instruction' ] in [ "SELL_TO_OPEN", "SELL_TO_CLOSE" ]:
                        self.state[ 'option' ][ 'lots' ] -= orders[ 'filledQuantity' ]

    def update_cost( self, symbol, accounts ):
        
        for positions in accounts[ 'positions' ]:
            instrument = positions[ 'instrument' ]
            equity = self.state[ 'equity' ]
            option = self.state[ 'option' ]

            if instrument[ 'assetType' ] == 'EQUITY' and instrument[ 'symbol' ] == symbol:
                equity[ 'cost' ] = positions[ 'averagePrice' ]

            if instrument[ 'assetType' ] == 'OPTION' and instrument[ 'underlyingSymbol' ] == symbol:
                option[ 'cost' ] = positions[ 'averagePrice' ]

            

