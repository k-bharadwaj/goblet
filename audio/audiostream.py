#!/usr/bin/python3
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
import subprocess

# TurnMeOn
DEBUG = True

PC_IP = "192.168.1.11"
PC_PORT = 55555

MAGIC = bytearray([0xab, 0xcd, 0xef, 0x10])
HEADER_SIZE = 2*len(MAGIC) + 1
fd_list = []

def init():
    subprocess.call("./deletewavs.sh", shell=True)
    for channel in range(9):
        f = open('channel_{}.raw'.format(channel), 'wb')
        fd_list.append(f)


def processData(data):
    magic_len = len(MAGIC)
    meta = data[0:magic_len]
    if (MAGIC != meta) or (MAGIC != data[magic_len + 1 : HEADER_SIZE]):
        print("malformed packet (header: {})".format(data[0:HEADER_SIZE]))
        return
    
    channel = int(data[magic_len])
    data = data[magic_len + 1:]
    fd = fd_list[channel]
    fd.write(data)


def main():
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((PC_IP, PC_PORT))

    counter = 0

    init()

    while True:
        rxData, addr = sock.recvfrom(32775)
        counter = counter + 1

        processData(rxData)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("closing files")
        for fd in fd_list:
            fd.close()

        print("converting raw to wav")
        subprocess.call("./convert.sh", shell=True)
        print("Done")
        print("")
