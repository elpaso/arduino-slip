#!/usr/bin/python
import sys
import time
import serial
serial_port = '/dev/ttyACM0'

arduino = serial.Serial(
	serial_port,
	9600,
	serial.EIGHTBITS,
	serial.PARITY_NONE,
	serial.STOPBITS_ONE,
	timeout=1)
	
time.sleep(2)

while 1:
	da_arduino = str(arduino.readline().rstrip())
	if (da_arduino):
		print(str(da_arduino))
