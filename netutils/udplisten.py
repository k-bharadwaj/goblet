'''
Simple UDP listen test, with the target being the driver

Steps to run: 
    * Set IP of host to 192.168.1.11
    * Target IP should be configured to 192.168.1.10
    * Host Port: 8001
    * Target Port: 8000
	* Run this script
    * Reset the target, host should now be listening for packets
	* Script breaks out of forever loop if data is not what's expected
    * Set DEBUG = True for packet count
'''

import socket
import time

# TurnMeOn
DEBUG = True

PC_IP = "192.168.1.11"
PC_PORT = 8001
TMS_IP = "192.168.1.10"
TMS_PORT = 8000

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((PC_IP, PC_PORT))

expectedData = "Hello, How are you doing today?"

counter = 0

while True:
    rxData, addr = sock.recvfrom(1024)
    if rxData != expectedData:
        print "Data Mismatch @ counter {}. : Expected: {}, GOT: {}".format(counter, expectedData, rxData)
        break
    counter = counter + 1
    if DEBUG:
        print "pkt rx ctr: {}".format(counter)

