import numpy as np
from numpy.fft import fft

from config import *

def extract_fft(channel_data):
    return np.abs(fft(channel_data - np.mean(channel_data)))[:int(len(channel_data)/2.0)]


def extract_rhythm_features(signal, fs=FS, rhythms=RHYTHMS, aggregation=np.mean):
    signal_len = int(len(signal) / fs)
    fft_data = extract_fft(signal)

    return [
         aggregation(fft_data[int(range_lower): int(range_upper)])
         for range_lower, range_upper in rhythms.values()
    ]
