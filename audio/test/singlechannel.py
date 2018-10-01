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
PACKET_HDR_SIZE = (2 * WORD_SIZE_BYTES)
CHANNEL_HDR_SIZE = (4 * WORD_SIZE_BYTES)

MAX_CHANNELS = 9

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
    for i in range(MAX_CHANNELS):
        fd = open('channel_{}_test.raw'.format(i), 'wb')
        fd_list.append(fd)


def processData(data):
    # TODO - make header a class later
    pkt_hdr_bytes = data[0 : PACKET_HDR_SIZE]
    data = data[PACKET_HDR_SIZE:]
    [hdr_magic, n_channels] = unpack('!II', pkt_hdr_bytes)
    dbgprint("Header: {}, n_channels: {}".format(hex(hdr_magic), hex(n_channels)))
	
    if n_channels >= MAX_CHANNELS:
        raise Exception("Maximum channels supported is {}".format(MAX_CHANNELS))

    for i in range(n_channels):
        chan_hdr_bytes = data[0 : CHANNEL_HDR_SIZE]
        data = data[CHANNEL_HDR_SIZE:]
        [chan_magic, chan_id, data_len, padding_len] = unpack('IIII', chan_hdr_bytes)
        if (chan_id >= MAX_CHANNELS):
            raise Exception("Channel ID cannot be > {}".format(MAX_CHANNELS))
        channel_payload = data[0 : data_len]
        data = data[(data_len + padding_len):]

        fd_list[chan_id].write(channel_payload)


def main():
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((PC_IP, PC_PORT))

    counter = 0

    init()

    while True:
        rxData, addr = sock.recvfrom(32768 + PACKET_HDR_SIZE)
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
