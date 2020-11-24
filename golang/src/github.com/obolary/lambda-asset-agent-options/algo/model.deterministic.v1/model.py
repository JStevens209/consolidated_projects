from datetime import datetime as dt
from gnosko.system_status import SystemStatus
from absl import logging
from context import *
from pandas import Timedelta



class Model():

    def __init__( self, symbol ):
        
        logging.info( '** initializing model,...' )

        self.symbol = symbol
        self.next_action = None
    
        # Create a new session connected to Gnosko
        self.SystemStatus = SystemStatus(
            GNOSKO_URL,
            GNOSKO_API_KEY, 
            GNOSKO_API_SECRET
        )

        self.SystemStatus.add_message_info( "** Intializing Model" )

        self.SystemStatus.clear_history

        pass

    def action( self, observation ):
        self.update_system_status( observation )

        action = { 'kind':'hold'}

        statuses = [
            [ 'market_closed',           None ],
            [ 'unknown',                 None ],
            [ 'pending',                 None ],
            [ 'market_open_closed',      self.market_open_closed ],
            [ 'opened_long_equity',      self.opened_long_equity ],
            [ 'opened_covered_call',     self.opened_covered_call]
        ]
        
        if self.next_action != None:
            action = self.next_action
            self.next_action = None
            return action

        for status in statuses:
            if status[ 0 ] in observation[ 'status' ]:
                if status[ 1 ] == None:
                    return action
                else:
                     action = status[ 1 ]( observation )
                     return action 


    def update_system_status( self, state ):
        # Login to Gnosko Session
        self.SystemStatus.begin( 'td-ameritrade-session-state', 'covered-call-v2' )

        status = 'unknown'
        position = ''
        unrealized_profit = 0

        option = state[ 'option' ]
        equity = state[ 'equity' ]

        accounts = state[ 'session' ].get_accounts( ACCOUNT_NUMBER, [ 'positions', 'orders' ])
        hours = state[ 'session' ].get_market_hours( markets= [ 'EQUITY' ], date= dt.now().isoformat() )[ 'equity' ][ 'EQ' ]

        if accounts == None or hours == None:
            return
        else:
            accounts = accounts[ 'securitiesAccount' ]

        if 'isOpen' in hours.keys():
            if hours[ 'isOpen' ] == True:
                status = 'market_open'

            elif hours[ 'isOpen' ] == False:
                status = 'market_closed'
        else:
            status = 'unknown'

        # Checks for pending orders
        if 'orderStrategies' in accounts.keys():
            for orders in accounts[ 'orderStrategies' ]:
                if orders[ 'status' ] == 'WORKING':
                    status += '_pending'
        
        if 'positions' in accounts.keys():
            have_short_call   = False
            have_long_put     = False
            have_long_equity  = False

            # Goes through each position to update the status, the unrealized_profit and the position
            for positions in accounts[ 'positions' ]:
                instrument = positions[ 'instrument' ]

                # Checks for long equity position
                if instrument[ 'assetType' ] == 'EQUITY' and positions[ 'longQuantity' ] > 0 and self.symbol == instrument[ 'symbol' ]:
                    have_long_equity = True

                    unrealized_profit += ( positions[ 'marketValue' ] - positions[ 'averagePrice' ] ) *  positions[ 'longQuantity' ]
                    position += ": +" + str( positions[ 'longQuantity' ] ) + " " + instrument[ 'symbol' ] + " "
                
                # Checks for short equity position
                if instrument[ 'assetType' ] == 'EQUITY' and positions[ 'shortQuantity' ] > 0 and self.symbol == instrument[ 'symbol' ]:
                    status += '_opened_short_equity'

                    unrealized_profit += ( positions[ 'averagePrice' ] - positions[ 'marketValue' ] ) * positions[ 'shortQuantity' ]
                    position += ": -" + str( positions[ 'shortQuantity' ] ) + " " + instrument[ 'symbol' ] + " "

                # Checks for long call position
                if instrument[ 'assetType' ] == 'OPTION' and instrument[ 'putCall' ] == 'CALL' and positions[ 'longQuantity' ] > 0 and self.symbol == instrument[ 'underlyingSymbol' ]:
                    status += '_opened_long_call'

                    unrealized_profit += ( positions[ 'marketPrice' ] - positions[ 'averagePrice' ] ) * positions[ 'longQuantity' ]
                    position += ": +" + str( positions[ 'longQuantity' ] ) + " " + instrument[ 'symbol' ] + " "

                # Checks for short call position
                if instrument[ 'assetType' ] == 'OPTION' and instrument[ 'putCall' ] == 'CALL' and positions[ 'shortQuantity' ] > 0 and self.symbol == instrument[ 'underlyingSymbol' ]:
                    have_short_call = True

                    unrealized_profit += ( positions[ 'averagePrice' ] - positions[ 'marketValue' ] ) * positions[ 'shortQuantity' ]
                    position += ": -" + str( positions[ 'shortQuantity' ] ) + " " + instrument[ 'symbol' ] + " "

                # Checks for long put position
                if instrument[ 'assetType' ] == 'OPTION' and instrument[ 'putCall' ] == 'PUT' and positions[ 'longQuantity' ] > 0 and self.symbol == instrument[ 'underlyingSymbol' ]:
                    have_long_put = True

                    unrealized_profit += ( positions[ 'marketPrice' ] - positions[ 'averagePrice' ] ) * positions[ 'longQuantity' ]
                    position += ": +" + str( positions[ 'longQuantity' ] ) + " " + instrument[ 'symbol' ] + " "

                # Checks for short put position
                if instrument[ 'assetType' ] == 'OPTION' and instrument[ 'putCall' ] == 'PUT' and positions[ 'shortQuantity' ] > 0 and self.symbol == instrument[ 'underlyingSymbol' ]:
                    status += '_opened_short_put'

                    unrealized_profit += ( positions[ 'averagePrice' ] - positions[ 'marketValue' ] ) * positions[ 'shortQuantity' ]
                    position += ": -" + str( positions[ 'shortQuantity' ] ) + " " + instrument[ 'symbol' ] + " "

            # Checks for a covered call position
            if have_short_call and have_long_equity and option[ 'lots' ] <= equity[ 'lots' ]:
                status += '_opened_covered_call'

            elif have_short_call:
                status += '_opened_short_call'
            
            elif have_long_equity:
                status += '_opened_long_equity'
            
            # Checks for a naked put position
            if have_long_equity and have_long_put:
                status += '_opened_long_put'
            
            elif have_long_put:
                status += '_opened_naked_put'
        
        # If there are no open positions...
        if 'positions' not in accounts.keys() or ( len( accounts[ 'positions' ] ) == 1 and accounts[ 'positions' ][0][ 'instrument' ][ 'type' ] == 'MONEY_MARKET_FUND' ):
            status += '_closed'

        # Gets rid of the first colon in the position string
        if position:
            position = position[ 1: ]

        # Update Gnosko
        self.SystemStatus.add_history( unrealized_profit, accounts[ 'currentBalances' ][ 'cashAvailableForTrading' ] )
        self.SystemStatus.set_balance( accounts[ 'currentBalances' ][ 'cashAvailableForTrading' ] - self.SystemStatus.system_status[ 'balance' ])
        self.SystemStatus.set_status( status )
        if position:
            self.SystemStatus.set_position( position )

        self.SystemStatus.commit()
        self.SystemStatus.end()

        state[ 'status' ] = status

    def market_open_closed( self, observation ):

        option = observation[ 'option' ]
        equity = observation[ 'equity' ]
        
        action = { 'kind': 'hold' }

        if (( observation[ 'account_balance' ] * .9 ) / ( equity[ 'price' ]))> 0:
            action[ 'kind' ] = 'open'
            action[ 'extrinsic' ] = 'buy'
            action[ 'equity' ] = {
                'lots': observation[ 'account_balance' ] / equity[ 'price' ]
            }
        else:
            logging.info( "** Not enough money to open a covered call position" )

        return action

    def opened_long_equity( self, observation ):

        action = { 'kind': 'hold' }
        equity = observation[ 'equity' ]

        if equity[ 'lots' ] > 0:

            call = self._find_nearest_covered_call( observation[ 'session' ] )

            action[ 'kind' ] = 'open'
            action[ 'extrinsic' ] = 'sell'
            action[ 'option' ] = {
                'strike': call[ 'strike' ],
                'symbol': call[ 'symbol' ],
                'lots': equity[ 'lots' ]
                'kind': 'c'
                'date': dt.today() + Timedelta( f'{call[ 'daysToExpiration' ]} days')
            }
        elif (( observation[ 'account_balance' ] *.9 ) / ( equity[ 'price' ] )) > 0:
            action[ 'kind' ] = 'open'
            action[ 'extrinsic' ] = 'buy'
            action[ 'equity' ] = {
                'lots': observation[ 'account_balance' ] / equity[ 'price' ]
            }
        else:
            logging.info( "** Not enough money to open a covered call position" )

        return action

    def opened_covered_call( self, observation ):

        option = observation[ 'option' ]
        equity = observation[ 'equity' ]
        action = { 'kind':'hold' }
        symbol = ''

        option_chain, strikes = self.get_option_chain( observation[ 'session' ] )
        for strike in strikes:
            if float( strike ) == option[ 'strike' ]:
                symbol = strikes[ strike ][0][ 'symbol' ]

        # If the value is decreasing close to zero, close out the trade
        if option[ 'price' ] < option[ 'cost' ] and option[ 'price' ] < .05:
            action[ 'kind' ] = 'close'
            action[ 'extrinsic' ] = 'buy'
            action[ 'option' ] = {
                'lots': option[ 'lots' ],
                'symbol': symbol
            }

        if equity[ 'price' ] > option[ 'strike' ]:
            action[ 'kind' ] = 'close'
            action[ 'extrinsic' ] = 'buy'
            action[ 'option' ] = {
                'lots': option[ 'lots' ],
                'symbol': symbol
            }

            self.next_action = {
                'kind':'close',
                'extrinsic':'sell',
                'equity': {
                    'lots': equity[ 'lots' ]
                }
            }

    def get_option_chain( self, session ):
        date = ( dt.today() + Timedelta( f'7 days' ) ).isoformat()

        option_chain = {
            'symbol': self.symbol,
            'contractType': 'CALL',
            'strikeCount': 14,
            'includeQuotes': 'TRUE',
            'strategy': 'SINGLE',
            'optionType': 'ALL',
            'toDate': date
        } 
        
        option_chain = session.get_options_chain( option_chain )
        strikes = list( option_chain[ 'callExpDateMap' ].values() )[0]

        return option_chain, strikes

    def _find_nearest_covered_call( self, session, minimum_days_til_expire = 4, minimum_mark = 0.10 ):
        covered_call = None

        td_chain, strikes = self.get_option_chain( session )
        
        underlyingPrice = td_chain[ 'underlyingPrice' ]
        volatility = td_chain[ 'volatility' ]
        interestRate = td_chain[ 'interestRate' ]
        callExpDateMap = td_chain[ 'callExpDateMap' ]
        for date_key in callExpDateMap.keys():
            strikes = callExpDateMap[ date_key ]
            for strike_key in strikes.keys():
                strike = strikes[ strike_key ]
                for contract in strike:
                    strike_price = float( strike_key )
                    symbol = contract[ 'symbol' ]
                    inTheMoney = contract[ 'inTheMoney' ]
                    daysToExpiration = contract[ 'daysToExpiration' ] 
                    mark = contract[ 'theoreticalOptionValue' ]
                    if not inTheMoney:
                        if daysToExpiration >= minimum_days_til_expire and mark >= minimum_mark:
                            if strike_price - underlyingPrice < mark:
                                if covered_call is not None:
                                    if daysToExpiration < covered_call[ 'daysToExpiration' ]:
                                        covered_call = {
                                            'symbol': symbol,
                                            'strike': strike_price,
                                            'mark': mark,
                                            'daysToExpiration': daysToExpiration,
                                            'underlyingPrice': underlyingPrice,
                                            'interestRate': interestRate,
                                            'volatility': volatility
                                        }
                                else:
                                    covered_call = {
                                        'symbol': symbol,
                                        'strike': strike_price,
                                        'mark': mark,
                                        'daysToExpiration': daysToExpiration,
                                        'underlyingPrice': underlyingPrice,
                                        'interestRate': interestRate,
                                        'volatility': volatility
                                    }
        return covered_call