import msvcrt
from time import sleep
import numpy as np

from emotiv_receiver import EmotivReceiver
from eeg import extract_rhythm_features
from led import USBLed
from joblib import load

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 8888

from config import *

if __name__ == '__main__':
    led = USBLed()
    led.open()

    model = load("model")

    receiver = EmotivReceiver(DEFAULT_IP, DEFAULT_PORT)
    receiver.start()

    while not msvcrt.kbhit():
        data, pending = receiver.get_data()

        if data is not None:
            X = np.hstack([extract_rhythm_features(f) for f in data[:, EEG_CHANNEL_MAP].T]).reshape(1, -1)
            pred = model.predict_proba(X).ravel()
            led.set_color([0, int(pred[1] * 1 * 255), 0])
            print(pred)
            # print(pred)

            if pending > FS:
                print(f"[WARNING] Model is desynchronized.")

    receiver.stop()
    receiver.join()

    led.close()
