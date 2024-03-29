__author__ = 'Malte-Christian Scharenberg'


class HardwareException(Exception):
    pass


class IHardware:
    def __init__(self):
        raise NotImplementedError("Should have implemented this")

    def register_node(self, node):
        raise NotImplementedError("Should have implemented this")

    def run(self):
        """
        This method gets invoked after process fork.
        Serial Port association, etc, should be implemented here.

        :raises HardwareException:
        """
        raise NotImplementedError("Should have implemented this")

    def stop(self):
        """
        This method gets invoked when process shuts down.
        """
        raise NotImplementedError("Should have implemented this")

    def send_packet(self, frame_id, packet, dest, ack=True):
        raise NotImplementedError("Should have implemented this")

    def check_channel(self):
        """
        This method gets invoked on a regular basis.
        You can use this to handle incoming packets.
        Ignore this method if you are working with callbacks.
        (pass)
        """

    def set_address(self, address):
        raise NotImplementedError("Should have implemented this")

    def at_command(self, address):
        raise NotImplementedError("Should have implemented this")