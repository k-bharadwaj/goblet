import sys
import can
import argparse
import struct
import errno

class Can(object):
  FORMAT = "<IB3x8s"

  def __init__(self, channel="can0"):
    self.channel = channel
    self.bus = can.interface.Bus(channel, bustype='socketcan_native')


  def send(self, can_id, data, is_extended=False, flags=0, timeout=1):
    data_send = bytearray(data)
    msg = can.message.Message(arbitration_id=can_id, extended_id=is_extended, 
            channel=self.channel, dlc=len(data), data=data_send)
    try:
        self.bus.send(msg, timeout=timeout)
    except can.CanError:
        print("Failed to send msg with id {} on {}".format(can_id, self.channel))

  def recv(self, flags=0, timeout=1):
    try:
        msg = self.bus.recv(timeout=timeout)
    except can.CanError:
        print("Failed to receive msg on {} for {} sec".format(self.channel, timeout))

    return msg
