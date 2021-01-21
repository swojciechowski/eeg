import os

import numpy

from emotiv.file import EmotivFile, FS
from feature_extraction.rythm import extract_rhythm_features

file_loc = os.path.dirname(os.path.realpath(__file__))
DEFAULT_DATA_SET_PATH = os.path.join(file_loc, '..', '..', 'dataset')


class EmotivDataSet:
    WINDOW_SIZE = 3
    STEP_SIZE = 1

    def __init__(self, path=DEFAULT_DATA_SET_PATH):
        self.target = []
        self.data = []

        for root, dirs, files in os.walk(path, topdown=False):
            for f in files:
                if '.csv' not in f:
                    continue

                data = EmotivFile(os.path.join(root, f))

                for window in data.get_windows(EmotivDataSet.WINDOW_SIZE, EmotivDataSet.STEP_SIZE):
                    features = []
                    for channel in window.T[1:]:
                        features.extend(extract_rhythm_features(channel, FS, [numpy.mean]))
                    self.data.append(numpy.array(features))
                    self.target.append(os.path.basename(root))

        self.data = numpy.array(self.data)
        self.target = numpy.array(list(map(int, self.target)))

    def get_set(self):
        return self.data, self.target
