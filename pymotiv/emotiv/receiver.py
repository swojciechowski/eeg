from threading import Semaphore

import numpy

from emotiv.file import FS
from udp.client import Client


DEFAULT_IP = "localhost"
DEFAULT_PORT = 6666


class EmotivReceiver(Client):
    def __init__(self, ip, port):
        super().__init__(ip, port, data_handle_cb=self.data_handle)

        self.data_buffer = []
        self.semaphore = Semaphore()

    def data_handle(self, data):
        with self.semaphore:
            self.data_buffer.append(numpy.frombuffer(data, dtype='Float64'))

    def get_data(self,  window_size=1, step=1):
        window_size = window_size * FS
        cutoff_size = step * FS

        with self.semaphore:
            if len(self.data_buffer) > window_size:
                ret = self.data_buffer[:window_size]
                self.data_buffer = self.data_buffer[cutoff_size:]
                return numpy.vstack(ret), len(self.data_buffer)
            else:
                return None, len(self.data_buffer)
