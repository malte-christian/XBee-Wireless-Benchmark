__author__ = 'Malte-Christian Scharenberg'

import serial
from xbee import XBee
from xbee.helpers.dispatch import Dispatch

from Hardware.HardwareBase import HardwareBase


class XBeeWrapper(HardwareBase):
    def __init__(self, port, address=None):
        self._port = port
        self._address = address
        self._serial = None
        self._xbee = None
        self._dispatcher = Dispatch()
        self.node = None

        # Init the dispatcher
        self._dispatcher.register(
            "tx_status",
            self.status_handler,
            lambda packet: packet['id'] == 'tx_status'
        )

        self._dispatcher.register(
            "rx",
            self.rx_handler,
            lambda packet: packet['id'] == 'rx'
        )

    def register_node(self, node):
        self.node = node

    def run(self):
        self._serial = serial.Serial(self._port, 115000, stopbits=serial.STOPBITS_TWO, rtscts=1)
        self._xbee = XBee(self._serial, callback=self._dispatcher.dispatch)

        # Set address
        if self._address:
            self._xbee.at(command='MY', parameter=chr(self._address), frame_id='\x01')

    def stop(self):
        self._xbee.halt()
        self._serial.close()

    def status_handler(self, name, packet):
        if self.node is not None:
            frame_id = ord(packet['frame_id'])
            status = packet['status']
            self.node.received_status(frame_id, status)

    def rx_handler(self, name, packet):
        if self.node is not None:
            data = packet['rf_data']

            self.node.received_packet(data)

    def send_packet(self, frame_id, data, dest, ack=1):
        self._xbee.tx(frame_id=chr(frame_id), dest_addr='\x00' + chr(dest), data=data, options=chr(ack))
