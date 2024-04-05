FS = 128
WINDOW_SIZE = 128
STEP_SIZE = 32

CHANNELS_INFO = [
    "IED_AF3",
    "IED_AF4",
    "IED_F3",
    "IED_F4",
    "IED_FC5",
    "IED_FC6",
    "IED_F7",
    "IED_F8",
    "IED_O1",
    "IED_O2",
    "IED_P7",
    "IED_P8",
    "IED_T7",
    "IED_T8",
]

EEG_CHANNEL_MAP = [
    False, # IED_COUNTER
    True, # IED_AF3
    True, # IED_AF4
    True, # IED_F3
    True, # IED_F4
    True, # IED_FC5
    True, # IED_FC6
    True, # IED_F7
    True, # IED_F8
    True, # IED_O1
    True, # IED_O2
    True, # IED_P7
    True, # IED_P8
    True, # IED_T7
    True, # IED_T8
    False, # IED_GYROX
    False, # IED_GYROY
    False, # IED_INTERPOLATED
    False, # IED_RAW_CQ
    False, # IED_TIMESTAMP
    False, # IED_ES_TIMESTAMP
    False, # IED_FUNC_ID
    False, # IED_FUNC_VALUE
    False, # IED_MARKER
    False, # IED_SYNC_SIGNAL
]

RHYTHMS = {
    "DELTA": (1.0, 3.0),
    "THETA": (4.0, 7.0),
    "ALPHA": (8.0, 12.0),
    "BETA": (13.0, 30.0),
    "GAMMA": (31.0, 64.0),
}