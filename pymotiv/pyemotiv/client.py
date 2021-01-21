import socket

from .stoppable_threaad import StoppableThread


class Client(StoppableThread):
    def __init__(self, ip, port, data_handle_cb, packet_size=0x1000):
        super(Client, self).__init__()

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((ip, port))
        self._sock.settimeout(0.1)

        self.data_handle_cb = data_handle_cb
        self.packet_size = packet_size

    def run(self):
        while not self.is_stopped():
            try:
                self.data_handle_cb(self._sock.recv(self.packet_size))
            except socket.timeout:
                continue
