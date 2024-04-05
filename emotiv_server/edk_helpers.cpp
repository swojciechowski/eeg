#include "edk_helpers.h"

#include <iostream>

static IEE_DataChannel_t channel_array[] = {
    IED_COUNTER,      //!< Sample counter
    IED_AF3,          //!< Channel AF3
    IED_AF4,          //!< Channel AF4
    IED_F3,           //!< Channel F3
    IED_F4,           //!< Channel F4
    IED_FC5,          //!< Channel FC5
    IED_FC6,          //!< Channel FC6
    IED_F7,           //!< Channel F7
    IED_F8,           //!< Channel F8
    IED_O1,           //!< Channel O1
    IED_O2,           //!< Channel O2
    IED_P7,           //!< Channel P7
    IED_P8,           //!< Channel P8
    IED_T7,           //!< Channel T7
    IED_T8,           //!< Channel T8
    IED_GYROX,        //!< Gyroscope X-axis
    IED_GYROY,        //!< Gyroscope Y-axis
    IED_INTERPOLATED, //!< Indicate if data is interpolated
    IED_RAW_CQ,       //!< Raw contact quality value
    IED_TIMESTAMP,    //!< System timestamp
    IED_ES_TIMESTAMP, //!< EmoState timestamp
    IED_FUNC_ID,      //!< Reserved function id
    IED_FUNC_VALUE,   //!< Reserved function value
    IED_MARKER,       //!< Marker value from hardware
    IED_SYNC_SIGNAL   //!< Synchronisation signal
};

IEE_DataChannel_t *get_channel_list()
{
    return channel_array;
}

int get_channel_list_size()
{
    return sizeof(channel_array) / sizeof(IEE_DataChannel_t);
}

char const *get_error_info(int error)
{
    switch (error)
    {

    case EDK_UNKNOWN_ERROR:
        return "An internal error occurred.";

    case EDK_INVALID_DEV_ID_ERROR:
        return "Invalid Developer ID.";

    case EDK_INVALID_PROFILE_ARCHIVE:
        return "The buffer supplied to IEE_SetUserProfile() is not a valid, serialized EmoEngine profile.";

    case EDK_NO_USER_FOR_BASEPROFILE:
        return "Returned from IEE_EmoEngineEventGetuser_id() if the event supplied contains a base profile and is not associated with specific user.";

    case EDK_CANNOT_ACQUIRE_DATA:
        return "The EmoEngine is unable to acquire data for processing.";

    case EDK_BUFFER_TOO_SMALL:
        return "The buffer supplied to the function is not large enough.";

    case EDK_OUT_OF_RANGE:
        return "A parameter supplied to the function is out of range.";

    case EDK_INVALID_PARAMETER:
        return "One of the parameters supplied to the function is invalid";

    case EDK_PARAMETER_LOCKED:
        return "The parameter is currently locked by the detection and cannot be modified at this time.";

    case EDK_MC_INVALID_TRAINING_ACTION:
        return "The supplied MentalCommand training action flag is invalid.";

    case EDK_MC_INVALID_TRAINING_CONTROL:
        return "The supplied MentalCommand training control flag is invalid.";

    case EDK_MC_INVALID_ACTIVE_ACTION:
        return "The MentalCommand action bits vector is invalid.";

    case EDK_MC_EXCESS_MAX_ACTIONS:
        return "The MentalCommand action bits vector contains more action types than it is allowed.";

    case EDK_FE_NO_SIG_AVAILABLE:
        return "A trained signature is not currently available for use, addition actions (including neutral) may be required.";

    case EDK_FILESYSTEM_ERROR:
        return "A filesystem error occurred.";

    case EDK_INVALID_USER_ID:
        return "The user ID supplied to the function is invalid.";

    case EDK_EMOENGINE_UNINITIALIZED:
        return "The EDK needs to be initialized via IEE_EngineConnect() or IEE_EngineRemoteConnect().";

    case EDK_EMOENGINE_DISCONNECTED:
        return "The connection with a remote instance of the EmoEngine made via EE_EngineRemoteConnect() has been lost.";

    case EDK_EMOENGINE_PROXY_ERROR:
        return "The API was unable to establish a connection with a remote instance of the EmoEngine.";

    case EDK_NO_EVENT:
        return "There are no new EmoEngine events at this time.";

    case EDK_GYRO_NOT_CALIBRATED:
        return "The gyro is not calibrated. Please ask the user to stay still for at least 0.5 seconds.";

    case EDK_OPTIMIZATION_IS_ON:
        return "Operation failure due to optimization.";

    case EDK_RESERVED1:
        return "Reserved return value.";

    default:
        return "Unknown Error.";
    }
}

char const *get_event_type(IEE_Event_t event)
{
    switch (event)
    {

    case IEE_UnknownEvent:
        return "An unknown event.";

    case IEE_EmulatorError:
        return "Error event from emulator. Connection to EmoComposer could be lost.";

    case IEE_ReservedEvent:
        return "Reserved event.";

    case IEE_UserAdded:
        return "A headset is connected.";

    case IEE_UserRemoved:
        return "A headset has been disconnected.";

    case IEE_EmoStateUpdated:
        return "Detection results have been updated from EmoEngine.";

    case IEE_ProfileEvent:
        return "A profile has been returned from EmoEngine.";

    case IEE_MentalCommandEvent:
        return "A IEE_MentalCommandEvent_t has been returned from EmoEngine.";

    case IEE_FacialExpressionEvent:
        return "A IEE_FacialExpressionEvent_t has been returned from EmoEngine.";

    case IEE_InternalStateChanged:
        return "Reserved for internal use.";

    default:
        return "Unknown Event.";
    }
}

char const *get_channel_name(IEE_DataChannel_t channel)
{
    switch (channel)
    {
    case IED_COUNTER:
        return "Sample counter";
    case IED_INTERPOLATED:
        return "Indicate if data is interpolated";
    case IED_RAW_CQ:
        return "Raw contact quality value";
    case IED_AF3:
        return "Channel AF3";
    case IED_F7:
        return "Channel F7";
    case IED_F3:
        return "Channel F3";
    case IED_FC5:
        return "Channel FC5";
    case IED_T7:
        return "Channel T7";
    case IED_P7:
        return "Channel P7";
    case IED_O1:
        return "Channel O1";
    case IED_O2:
        return "Channel O2";
    case IED_P8:
        return "Channel P8";
    case IED_T8:
        return "Channel T8";
    case IED_FC6:
        return "Channel FC6";
    case IED_F4:
        return "Channel F4";
    case IED_F8:
        return "Channel F8";
    case IED_AF4:
        return "Channel AF4";
    case IED_GYROX:
        return "Gyroscope X-axis";
    case IED_GYROY:
        return "Gyroscope Y-axis";
    case IED_TIMESTAMP:
        return "System timestamp";
    case IED_MARKER_HARDWARE:
        return "Marker from extender";
    case IED_ES_TIMESTAMP:
        return "EmoState timestamp";
    case IED_FUNC_ID:
        return "Reserved function id";
    case IED_FUNC_VALUE:
        return "Reserved function value";
    case IED_MARKER:
        return "Marker value from hardware";
    case IED_SYNC_SIGNAL:
        return "Synchronisation signal";
    default:
        return "Unknown";
    }
}

void print_headset_config(const unsigned int &user_id)
{
    unsigned int EPOCmode;
    unsigned int eegRate;
    unsigned int eegRes;
    unsigned int memsRate;
    unsigned int memsRes;
    unsigned int sample_rate;

    IEE_DataGetSamplingRate(user_id, &sample_rate);
    std::cout << "Sampling rate: " << sample_rate << std::endl;

    IEE_GetHeadsetSettings(user_id, &EPOCmode, &eegRate, &eegRes, &memsRate, &memsRes);
    std::cout << "EPOCmode " << EPOCmode << "; " << "eegRate " << eegRate << "; " << "eegRes " << eegRes << "; " << "memsRate " << memsRate << "; " << "memsRes " << memsRes << std::endl;
}
