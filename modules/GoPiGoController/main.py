# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import gopigo3 # import the GoPiGo3 drivers
import json
import socket

import time
import os
import sys
import asyncio
from six.moves import input
import threading
# from azure.iot.device.aio import IoTHubModuleClient
from signal import signal, SIGINT, SIGTERM
import gopigo3 # import the GoPiGo3 drivers
import json
import socket

exiting = False

async def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
        print ( "Starting GoPiGo Controller" )

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

        async def joystick_listen():
            global exiting
            GPG = gopigo3.GoPiGo3() # Create an instance of the GoPiGo3 class. GPG will be the GoPiGo3 object.

            UDP_IP = "192.168.0.112"
            UDP_PORT = 5005

            print("UDP target IP:", UDP_IP)
            print("UDP target port:", UDP_PORT)

            sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

            server_address = (UDP_IP, UDP_PORT)
            sock.bind(server_address)
            while not exiting:
                try:
                    data, address = sock.recvfrom(4096)
                    coordinatesJson = data.decode('utf-8')
                    coordinates = json.loads(coordinatesJson)

                    powerLeft = (127 - coordinates['y']) - ((127 - coordinates['x']) / 2)
                    if (powerLeft > 100):
                        powerLeft = 100
                    elif (powerLeft < -100):
                        powerLeft = -100
                    
                    powerRight = (127 - coordinates['y']) + ((127 - coordinates['x']) / 2)
                    if (powerRight > 100):
                        powerRight = 100
                    elif (powerRight < -100):
                        powerRight = -100

                    if (abs(127 - coordinates['y']) < 15 & (127 - coordinates['x']) > 110):
                        powerLeft = -100
                        powerRight = 100
                    elif (abs(127 - coordinates['y']) < 15 & (127 - coordinates['x']) < -110):
                        powerLeft = 100
                        powerRight = -100
                    
                    GPG.set_motor_power(GPG.MOTOR_LEFT, powerLeft)
                    GPG.set_motor_power(GPG.MOTOR_RIGHT, powerRight)

                except Exception as e:
                    print(e)

            # Reset the GoPiGo
            GPG.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the GoPiGo3 firmware.

        # def until_exiting():
        #     while not exiting:
        #         await asyncio.sleep(1)            

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

        await joystick_listen()

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