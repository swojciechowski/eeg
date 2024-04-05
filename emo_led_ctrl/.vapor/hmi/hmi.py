import numpy
import serial
import msvcrt
import time

from emotiv.file import FS
from emotiv.receiver import EmotivReceiver
from feature_extraction.rythm import extract_rhythm_features
from neural_network.neural_network import NeuralNetwork

DEFAULT_IP = "localhost"
DEFAULT_PORT = 6666

# This value is empirically discovered during learning
# TODO: Find way to store this in order to reuse in non-'magic number' manner
normalizer = 16365.11520027733


def normalize(array):
    norm = lambda val: val / normalizer
    vfunc = numpy.vectorize(norm)
    return vfunc(array)


if __name__ == '__main__':
    ser = serial.Serial(
        port='COM3',
        baudrate=9600,
    )

    receiver = EmotivReceiver(DEFAULT_IP, DEFAULT_PORT)
    clf = NeuralNetwork()

    clf.load_model()
    receiver.start()

    while not msvcrt.kbhit():
        data, pending = receiver.get_data(window_size=3, step=1)
        if data is not None:
            features = []
            for channel in data.T[1:]:
                features.extend(extract_rhythm_features(channel, FS, [numpy.mean]))

            support = clf.classify(normalize(numpy.array(features)))[0][0]
            print(support, pending, 'dim' if support < 0.5 else 'bright')

            if support > 0.8:
                ser.write(bytes([0x31]))
            elif support < 0.8:
                ser.write(bytes([0x30]))

            print(ser.read())

    receiver.stop()
    receiver.join()

    ser.close()
