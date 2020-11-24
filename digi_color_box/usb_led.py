from threading import Thread, Event

from digi_usb import DigiUSB

CTRL_BYTE = b'\n'
DELAY = 0.01

class USBLed:
    def __init__(self, initial_color=None, transision=None):
        if initial_color is None:
            self.color = (0, 0, 0)
        else:
            self.color = initial_color

        self._device = None

        self.__communiation_thread = Thread(target=self.__communication)
        self.__communication_stop = Event()

    def __communication(self):
        while not self.__communication_stop.wait(DELAY):
            self._device.write(ord(CTRL_BYTE))
            ctrl = self._device.read()
            # print(f"Received: {type(ctrl)} {ctrl}")

            if ctrl != CTRL_BYTE:
                continue

            for _ in self.color:
                self._device.write(_)
            # print(f"Written: {bytes(self.color)}")

        self._device = None

    @staticmethod
    def instant_transition(target_color):
        return target_color

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
