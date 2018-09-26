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
    * Set DEBUG = True for debug stuff
'''

import socket
import time
import subprocess
from struct import unpack

# TurnMeOn
DEBUG = True

PC_IP = "192.168.1.11"
PC_PORT = 55555

PACKET_MAGIC = 0xdeadbeef
MIC_MAGIC = 0xfeedbeef

WORD_SIZE_BYTES = 4
PACKET_HDR_SIZE = (3 * WORD_SIZE_BYTES)

'''

------------
PACKET_MAGIC (U32)
------------
PACKET_ID (U32)
------------
NUM_CHANS (U32)
------------
MIC_MAGIC(0)  (U32)
------------
MIC_CHANNEL(0) (U32)
------------
DATALEN(0)      (U32)
------------
PADDING(0)      (U32)
------------
DATA(0)
------------
.
.
------------
PADDING(0)
------------
.
.
------------
MIC_MAGIC(1)
------------
.
.
------------
MIC_MAGIC(N)
------------

'''


fd_list = []

def dbgprint(msg):
    if DEBUG:
        print(msg)

def init():
    f = open('channel_{}_test.raw'.format(0), 'wb')
    fd_list.append(f)


def processData(data):
    # TODO - make header a class later
    pkt_hdr_bytes = data[0 : PACKET_HDR_SIZE]
    data = data[PACKET_HDR_SIZE:]
    [hdr_magic, pkt_id, n_chans] = unpack('!III', pkt_hdr_bytes)
    dbgprint("Header: {}, PktId: {}, NChannels: {}".format(hdr_magic, pkt_id, n_chans))

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
