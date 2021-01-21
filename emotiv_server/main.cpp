#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>

#include "IEegData.h"

#include "edk_helpers.h"
#include "udp.h"

#include "config.h"

std::ostream *output = &std::cout;

IEE_DataChannel_t *channel_list = get_channel_list();
int channel_count =  get_channel_list_size();

void write_to_stream(double **buffer, int number_of_samples) {

    for (int j = 0; j < number_of_samples; j++) {
        for (int i = 0; i < channel_count; i++) {
            *output << buffer[i][j] << CSV_SEPARATOR;
        }

        *output << CSV_NEW_LINE;
    }
}

void transmit_udp_packet(double **buffer, int number_of_samples) {
    double *sample_buffer = new double[channel_count];

    std::cout << "Sending " << number_of_samples << std::endl;

    for (int j = 0; j < number_of_samples; j++) {
        for (int i = 0; i < channel_count; i++) {
            sample_buffer[i] = buffer[i][j];
        }

        send_message((char*)sample_buffer, sizeof(double) * channel_count);
    }

    delete sample_buffer;
}

void (*data_sending_func)(double**, int) = &transmit_udp_packet;

// TODO: Add ending condition to infinite loop
void data_acuisition_handle(unsigned int user_id) {
    int status = 0;
    unsigned int number_of_samples = 0;
    double **buffer = NULL;

    DataHandle data_handle = IEE_DataCreate();
    udp_connect();

    status = IEE_DataAcquisitionEnable(user_id, true);
    if (status) throw std::runtime_error(get_error_info(status));

    while (true) {
        status = IEE_DataUpdateHandle(user_id, data_handle);
        if (status) throw std::runtime_error(get_error_info(status));

        IEE_DataGetNumberOfSample(data_handle, &number_of_samples);
        if (number_of_samples) {
            buffer = new double*[channel_count];
            for (int i = 0; i < channel_count; i++) {
                buffer[i] = new double[number_of_samples];
            }

            IEE_DataGetMultiChannels(data_handle, channel_list, channel_count, buffer, number_of_samples);

            data_sending_func(buffer, number_of_samples);

            for (int i = 0; i < channel_count; i++) delete[] buffer[i];
            delete[] buffer;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    status = IEE_DataAcquisitionEnable(user_id, false);
    if (status) throw std::runtime_error(get_error_info(status));

    udp_disconnect();
    IEE_DataFree(data_handle);

}

int main(int argc, char **argv) {
    int status = 0;
    std::fstream file;

    std::thread acquisition_thread;

    std::cout << "Connecting ... ";
    status = IEE_EngineConnect();
    if (status) throw std::runtime_error(get_error_info(status));
    std::cout << "OK" << std::endl;

    IEE_DataSetBufferSizeInSec(BUFFER_SIZE_IN_SEC);

    EmoEngineEventHandle event_handle = IEE_EmoEngineEventCreate();

//    while (!GetAsyncKeyState(VK_ESCAPE)) {
    while (true) {
        if (IEE_EngineGetNextEvent(event_handle) == EDK_OK) {
            unsigned int user_id;

            IEE_Event_t event_type = IEE_EmoEngineEventGetType(event_handle);
            IEE_EmoEngineEventGetUserId(event_handle, &user_id);

#if FUNC_EVENT_LOG_ENABLE
            std::cout << '[' << user_id << "] EVENT: " << get_event_type(event_type) << std::endl;
#endif
            switch (event_type) {

            case IEE_UserAdded:
                acquisition_thread = std::thread(data_acuisition_handle, user_id);
                break;

            default:
                break;
            }
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }

    acquisition_thread.join();

    IEE_EmoEngineEventFree(event_handle);
    IEE_EngineDisconnect();

    return 0;
}
