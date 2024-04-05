from threading import Thread, Event, Semaphore
import socket
import numpy as np

from config import *

DEFAULT_IP = "localhost"
DEFAULT_PORT = 6666

class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()

    def join(self, *args, **kwargs):
        self.stop()
        super(StoppableThread, self).join(*args, **kwargs)


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

class EmotivReceiver(Client):
    def __init__(self, ip, port):
        super().__init__(ip, port, data_handle_cb=self.data_handle)

        self.data_buffer = []
        self.semaphore = Semaphore()

    def data_handle(self, data):
        with self.semaphore:
            self.data_buffer.append(np.frombuffer(data, dtype=np.double))

    def get_data(self,  window_size=WINDOW_SIZE, step=STEP_SIZE):
        window_size = window_size
        cutoff_size = step

        with self.semaphore:
            if len(self.data_buffer) > window_size:
                ret = self.data_buffer[:window_size]
                self.data_buffer = self.data_buffer[cutoff_size:]
                return np.vstack(ret), len(self.data_buffer)
            else:
                return None, len(self.data_buffer)
