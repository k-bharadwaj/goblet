'''
Simple UDP Echo test, with this script being the driver

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

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((PC_IP, PC_PORT))

txData = "Hello, How are you doing today?"
txDataBytes = len(txData)

# calculate the max data rate we can spam the eth IF on.
# assume 100 MBPS
# PPS = 16.5MBPS / (txDataBytesperpacket)
# seconds per packet = 1/pps

pps = 16.5 * 1000000 / txDataBytes
delayPerPacket = 1/pps

counter = 0

while True:
    sock.sendto(txData, (TMS_IP, TMS_PORT))
    rxData, addr = sock.recvfrom(1024)
    if rxData != txData:
    	print "Data Mismatch @ counter {}. : SENT: {}, GOT: {}".format(counter, txData, rxData)
    counter = counter + 1
    if DEBUG:
    	print "pkt send ctr: {}".format(counter)
    time.sleep(delayPerPacket)
