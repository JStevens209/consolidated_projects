import asyncio
import pprint
import signal
import sys
import socket

from td.client import TDClient

going  = True

class TDEnvStream():

    def __init__(self):
        
        # Create a new session
        self.TDSession = TDClient(
            client_id = 'KYAPSIFUUPRBMCFY8PDXFWSDGILPI2S3',
            redirect_uri = 'https://gnosko.obolary.com',
            credentials_path='./credentials.json'
        )

        # Login to the session
        self.TDSession.login()

        # Create a streaming sesion
        self.TDStreamingClient = self.TDSession.create_streaming_session()

        # Level One Quote
        self.TDStreamingClient.level_one_quotes(
            symbols=["SLV"],
            fields=list(range(0,50))
        )

        signal.signal(signal.SIGINT, self.signal_handler)
        self.done = False

        try:
            asyncio.run( self.data_pipeline() )
        except Exception as ex:
            print( ex )

    # Listen for keyboard CTRL + C interrupt, exit gracefully
    def signal_handler(self, sig, frame):
        self.done = True
                
    # Data Pipeline function
    async def data_pipeline(self):
        # Build the Pipeline.
        await self.TDStreamingClient.build_pipeline()

        while not self.done:
            # Start the Pipeline.
            data = await self.TDStreamingClient.start_pipeline()

            # Grab the Data, if there was any. Remember not every message will have `data.`
            
            if data != None and 'data' in data:

                print('='*80)

                data_content = data['data'][0]['content']
                pprint.pprint(data_content, indent=4)

                # Here I can grab data as it comes in and do something with it.
                if 'key' in data_content[0]:
                    print('Here is my key: {}'.format(data_content[0]['key']))

                print('-'*80)

        print( 'Unsubscribing...')
        await self.TDStreamingClient.unsubscribe(service='LEVELONE_QUOTES')

        print( 'Closing Stream...' )
        await self.TDStreamingClient.close_stream()

        self.TDSession.logout()

        print( 'Exiting...' )
        sys.exit(0)


# Run the pipeline.
if __name__ == "__main__":
    pipeline = TDEnvStream()
    
    
