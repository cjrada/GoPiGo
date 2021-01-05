# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
import os
import sys
import asyncio
from six.moves import input
import threading
# from azure.iot.device.aio import IoTHubModuleClient
import joystickPS2
from signal import signal, SIGINT, SIGTERM

exiting = False

async def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
        print ( "Starting joystick" )

        # # The client object is used to interact with your Azure IoT hub.
        # module_client = IoTHubModuleClient.create_from_edge_environment()

        # # connect the client.
        # await module_client.connect()

        # # define behavior for receiving an input message on input1
        # async def input1_listener(module_client):
        #     while True:
        #         input_message = await module_client.receive_message_on_input("input1")  # blocking call
        #         print("the data in the message received on input1 was ")
        #         print(input_message.data)
        #         print("custom properties are")
        #         print(input_message.custom_properties)
        #         print("forwarding mesage to output1")
        #         await module_client.send_message_to_output(input_message, "output1")        

        # define behavior for receiving an input message on input1
        async def read_and_send():
            global exiting
            joystickPS2.setup()

            while not exiting:
                try:
                    asyncio.sleep(0.02)
                    joystickPS2.sendResult()
                except Exception as e:
                    print(e)

            joystickPS2.destory()

        def exit_handler(signal_received, frame):
            global exiting
            # Handle any cleanup here
            print('SIGINT, CTRL-C or SIGTERM detected. Exiting gracefully')
            exiting = True                 

        # Setup exit handlers
        signal(SIGINT, exit_handler)
        signal(SIGTERM, exit_handler)

        # # Schedule task for C2D Listener
        # listeners = asyncio.gather(input1_listener(module_client))

        print ( "Now listening for instructions" )

        await read_and_send()

        # # Cancel listening
        # listeners.cancel()

        # # Finally, disconnect
        # await module_client.disconnect()

    except Exception as e:
        print ( "Unexpected error %s " % e )
        raise

if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()

    # If using Python 3.7 or above, you can use following code instead:
    asyncio.run(main())