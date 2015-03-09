import time
import random
import multiprocessing
from Hardware.HardwareBase import HardwareBase

__author__ = 'Malte-Christian'


class HardwareMock(HardwareBase):
    channel = multiprocessing.Queue()

    def __init__(self, port):
        self._port = port
        self.node = None

    def register_node(self, node):
        self.node = node

    def send_packet(self, frame_id, packet, dest, ack=1):
        time.sleep(0.5 * random.random())
        HardwareMock.channel.put(packet)

    def check_channel(self):
        while True:
            try:
                data = HardwareMock.channel.get(block=False)
                self.node.received_packet(data)
            except Exception:
                break

    def run(self):
        pass

    def stop(self):
        pass