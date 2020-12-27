#!/usr/bin/env python
#
# https://www.dexterindustries.com/GoPiGo/
# https://github.com/DexterInd/GoPiGo3
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md
#
# This code is an example for controlling the GoPiGo3 Motors
#
# Results:  When you run this program, the GoPiGo3 Motors will rotate back and forth.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import gopigo3 # import the GoPiGo3 drivers
import json
import socket

GPG = gopigo3.GoPiGo3() # Create an instance of the GoPiGo3 class. GPG will be the GoPiGo3 object.

UDP_IP = "192.168.0.112"
UDP_PORT = 5005

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM) # UDP

server_address = (UDP_IP, UDP_PORT)
sock.bind(server_address)

try:    
    while True:
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

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    GPG.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the GoPiGo3 firmware.
