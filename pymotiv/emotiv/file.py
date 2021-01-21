import numpy
import os

IED_COUNTER = "COUNTER"
IED_AF3 = "AF3"
IED_F7 = "F7"
IED_F3 = "F3"
IED_FC5 = "FC5"
IED_T7 = "T7"
IED_P7 = "P7"
IED_O1 = "O1"
IED_O2 = "O2"
IED_P8 = "P8"
IED_T8 = "T8"
IED_FC6 = "FC6"
IED_F4 = "F4"
IED_F8 = "F8"
IED_AF4 = "AF4"

CHANNELS = [
    IED_COUNTER, IED_AF3, IED_F7, IED_F3, IED_FC5, IED_T7, IED_P7, IED_O1, IED_O2, IED_P8, IED_T8, IED_FC6,
    IED_F4, IED_F8, IED_AF4
]

FS = 128


class EmotivFile:
    def __init__(self, file):
        self.data = numpy.genfromtxt(file, dtype=numpy.float64, delimiter=';', skip_header=True)

    def __getitem__(self, key):
        try:
            idx = CHANNELS.index(key)
        except ValueError:
            raise KeyError(key)

        return self.data[:, idx]

    def get_windows(self, window_size=1, step=1):
        window_size = window_size * FS
        cutoff_size = step * FS

        def generate():
            data_copy = self.data
            while len(data_copy) > window_size:
                yield data_copy[:window_size]
                data_copy = data_copy[cutoff_size:]

        return tuple(generate())
