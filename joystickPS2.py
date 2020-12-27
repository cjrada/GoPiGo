#!/usr/bin/env python
#------------------------------------------------------
#
#		This is a program for JoystickPS2 Module.
#
#		This program depend on ADC0832 ADC chip. Follow 
#	the instruction book to connect the module and 
#	ADC0832 to your Raspberry Pi.
#
#------------------------------------------------------
import ADC0832
import RPi.GPIO as GPIO
import time


import socket
import json

UDP_IP = "192.168.0.112"
UDP_PORT = 5005

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_DGRAM) # UDP



btn = 15	# Define button pin

def setup():
	ADC0832.setup()				# Setup ADC0832
	GPIO.setmode(GPIO.BOARD)	# Numbers GPIOs by physical location
	GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Setup button pin as input an pull it up
	global state
	state = ['up', 'down', 'left', 'right']	

def printResult():	#get joystick result
	if ADC0832.getResult(1) == 0:
		print('up')		#up
	if ADC0832.getResult(1) == 255:
		print('down')		#down
		
	if ADC0832.getResult(0) == 0:
		print('left')		#left
	if ADC0832.getResult(0) == 255:
		print('right')		#right

	if GPIO.input(btn) == 0:
		print('Button is pressed!')		# Button pressed

def sendResult():
        coordinates = {
                "x": ADC0832.getResult(0),
                "y": ADC0832.getResult(1),
                "z": (GPIO.input(btn) == 0)
                }
        print(coordinates)
        sock.sendto(json.dumps(coordinates).encode(), (UDP_IP, UDP_PORT))

def loop():
	while True:
                time.sleep(0.02)
                sendResult()
                printResult()

def destory():
	GPIO.cleanup()				# Release resource

if __name__ == '__main__':		# Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destory()
