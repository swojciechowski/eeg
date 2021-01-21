import socket

from .stoppable_threaad import StoppableThread


class Server(StoppableThread):
    def __init__(self, ip, port, data_generator):
        super(Server, self).__init__()

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.target = (ip, port)
        self.data_cb = data_generator

    def run(self):
        for data in self.data_cb():
            self._sock.sendto(data, self.target)
            if self.is_stopped():
                break
