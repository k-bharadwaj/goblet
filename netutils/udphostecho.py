'''
Simple UDP Echo test, with the host being the driver

Steps to run: 
	* Set IP of host to 192.168.1.11
	* Target IP should be configured to 192.168.1.10
	* Host Port: 8001
	* Target Port: 8000
	* run this script
	* Reset the target, target should now be spamming  packets
	* host echoes back packets, for the target to compare
	* Set DEBUG = True for packet count
'''

import socket
import time

# TurnMeOn
DEBUG = False

PC_IP = "192.168.1.11"
PC_PORT = 8001
TMS_IP = "192.168.1.10"
TMS_PORT = 8000

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((PC_IP, PC_PORT))

counter = 0

while True:
    rxData, addr = sock.recvfrom(1024)
    counter = counter + 1
	sock.sendto(rxData, (TMS_IP, TMS_PORT)) #echo back
    if DEBUG:
    	print "pkt send ctr: {}".format(counter)
