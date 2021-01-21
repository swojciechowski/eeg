import numpy
from numpy.fft import fft

RHYTHM_RANGES = {
    "DELTA": (1, 3), "THETA": (4, 7), "ALPHA": (8, 12), "BETA": (13, 30), "GAMMA": (31, 64),
}


def extract_fft(channel_data):
    return numpy.abs(fft(channel_data - numpy.mean(channel_data)))[:int(len(channel_data)/2.0)]


def extract_rhythm_features(signal, fs, features_func_vec, freq_ranges=RHYTHM_RANGES.values()):
    signal_len = int(len(signal) / fs)
    fft_data = extract_fft(signal)

    def generate():
        for range_lower, range_upper in freq_ranges:
            for func in features_func_vec:
                yield func(fft_data[range_lower * signal_len: range_upper * signal_len])

    return tuple(generate())
