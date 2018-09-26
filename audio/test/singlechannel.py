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

fd_list = []

def init():
    f = open('channel_{}_test.raw'.format(0), 'wb')
    fd_list.append(f)


def processData(data):
    channel = 0

    fd = fd_list[channel]
    fd.write(data)


def main():
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((PC_IP, PC_PORT))

    counter = 0

    init()

    while True:
        rxData, addr = sock.recvfrom(32768)
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
