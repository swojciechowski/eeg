import os
import numpy as np

from config import *
from eeg import extract_rhythm_features
from itertools import product

import pandas as pd

DS_DIR = 'dataset'

EEG_TRACKS = os.listdir(DS_DIR)

def split_windows(stream, widnow_size=WINDOW_SIZE, step=STEP_SIZE):
    start = 0

    while True:
        if start + widnow_size > len(stream):
            break
        
        yield stream[start:start+widnow_size]
        start += step

dataset = []

FEATURE_NAMES = [
    f"{channel_name}_{freq}" for channel_name, freq in product(CHANNELS_INFO, RHYTHMS)
] + ["USER_ID", "TRACK_ID", "CLASS"]

for eeg_track in EEG_TRACKS:
    # Strip csv error col
    user_id, class_id, track_id = eeg_track.split('.')[0].split('_')

    eeg_data = np.genfromtxt(os.path.join(DS_DIR, eeg_track), delimiter=',')[:, :-1]
    eeg_data = eeg_data[:, EEG_CHANNEL_MAP]
    
    print(eeg_data.shape)
    for eeg_window in split_windows(eeg_data):
        row = [f for ff in eeg_window.T for f in extract_rhythm_features(ff)] + [int(user_id), int(track_id), int(class_id)]
        dataset.append(row)


df = pd.DataFrame(dataset, columns=FEATURE_NAMES)
print(df)
df.to_csv("dataset.csv")
