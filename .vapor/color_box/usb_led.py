from threading import Thread, Event

from digi_usb import DigiUSB

CTRL_BYTE = b'\n'
DELAY = 0.01

TRANSITION = 1

def sign(x):
    return (x > 0) - (x < 0)

class USBLed:
    def __init__(self, initial_color=None):
        self.color = initial_color if initial_color else [0, 0 ,0]
        self._current_color = self.color
        self._device = None

        self.__communiation_thread = Thread(target=self.__communication)
        self.__communication_stop = Event()

    def __communication(self):
        while not self.__communication_stop.wait(DELAY):
            if self._current_color == self.color:
                continue

            self._device.write(ord(CTRL_BYTE))
            ctrl = self._device.read()

            if ctrl != CTRL_BYTE:
                continue

            if TRANSITION == 0:
                self._current_color = self.color
            elif TRANSITION == 1:
                self._current_color = [cc + sign(c - cc) for c, cc in zip(self.color, self._current_color)]

            for _ in self._current_color:
                self._device.write(_)

        self._device = None

    def open(self):
        if self._device is not None:
            return None  # TODO: Handle error

        self._device = DigiUSB(idVendor=0x16c0, idProduct=0x05df)
        self.__communiation_thread.start()

    def close(self):
        self.__communication_stop.set()
        self.__communiation_thread.join()

    def set_color(self, color):
        self.color = color
