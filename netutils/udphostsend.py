'''
Simple UDP packet send, with this script being the driver

Steps to run: 
	* Set IP of host to 192.168.1.11
	* Target IP should be configured to 192.168.1.10
	* Host Port: 8001
	* Target Port: 8000
	* Reset the target, target should now be listening for packets
	* Run this script. Target echoes back the sent data, this script
	  compares sent and received data. No exceptions, just prints if there's an error.
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

# ChangeMe
KILOBITS_PER_SEC = 50

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((PC_IP, PC_PORT))

txData = "forklyft"
txDataBytes = len(txData)

# this is to test the CAN fwding svc, so calculate data rate for 'kbps' kbps 
kiloBytesPerSec = KILOBITS_PER_SEC / 8.0
bytesPerSec = kiloBytesPerSec * 1000
packetsPerSec = bytesPerSec / txDataBytes
delayPerPacket = 1.0/packetsPerSec

counter = 0

print("Sending data @ {} kbitsPerSec".format(KILOBITS_PER_SEC))

while True:
    sock.sendto(txData, (TMS_IP, TMS_PORT))
    counter = counter + 1
    if DEBUG:
    	print "pkt send ctr: {}".format(counter)
    time.sleep(delayPerPacket)
	#time.sleep(1)
