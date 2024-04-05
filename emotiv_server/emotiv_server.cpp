#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>
#include <iomanip>
#include <IEegData.h>
#include <windows.h>

#include "config.h"
#include "edk_helpers.h"

#if USE_UDP
#include "udp.h"
#endif

#if USE_CSV_LOGGING
std::string file_name = "reading.csv";
std::ofstream csv_file;
#endif

std::ostream *output = &std::cout;

IEE_DataChannel_t *channel_list = get_channel_list();
int channel_count = get_channel_list_size();

void write_to_stream(double **buffer, int number_of_samples)
{
    for (int j = 0; j < number_of_samples; j++)
    {
        for (int i = 0; i < channel_count; i++)
        {
            *output << buffer[i][j] << CSV_SEPARATOR;
        }

        *output << CSV_NEW_LINE;
    }
}

#if USE_UDP
void transmit_udp_packet(double **buffer, int number_of_samples) {
    double sample[channel_count];
    std::cout << "Sending [" << number_of_samples << "]" << std::endl;

    for (int i = 0; i < number_of_samples; i++) {

        for (int j = 0; j < channel_count; j++) {
            sample[j] = buffer[j][i];
        }

        send_message((char*)sample, sizeof(double) * channel_count);
    }
}
#endif

// TODO: Add ending condition to infinite loop
void data_acuisition_handle(unsigned int user_id)

{
    int status = 0;
    unsigned int number_of_samples = 0;
    double **buffer = NULL;

    DataHandle data_handle = IEE_DataCreate();
    print_headset_config(user_id);

#if USE_UDP
    udp_connect();
#endif

#if USE_CSV_LOGGING
    csv_file.open(file_name);
    output = &csv_file;
#endif

    *output << std::fixed << std::setprecision(5);

    status = IEE_DataAcquisitionEnable(user_id, true);
    if (status)
        throw std::runtime_error(get_error_info(status));

    auto start = std::chrono::high_resolution_clock::now();

    // while(std::chrono::duration_cast<std::chrono::seconds>(
    //     std::chrono::high_resolution_clock::now() - start).count() <= 30.0)
    while(1)
    {
        status = IEE_DataUpdateHandle(user_id, data_handle);
        if (status)
            throw std::runtime_error(get_error_info(status));

        IEE_DataGetNumberOfSample(data_handle, &number_of_samples);
        if (number_of_samples)
        {
            buffer = new double *[channel_count];
            for (int i = 0; i < channel_count; i++)
            {
                buffer[i] = new double[number_of_samples];
            }

            IEE_DataGetMultiChannels(data_handle, channel_list, channel_count, buffer, number_of_samples);

            #if USE_UDP
                transmit_udp_packet(buffer, number_of_samples);
            #else
                write_to_stream(buffer, number_of_samples);
            #endif

            for (int i = 0; i < channel_count; i++)
                delete[] buffer[i];
            delete[] buffer;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    status = IEE_DataAcquisitionEnable(user_id, false);
    if (status)
        throw std::runtime_error(get_error_info(status));

#if USE_UDP
    udp_disconnect();
#endif

#if USE_CSV_LOGGING
    csv_file.close();
#endif

    IEE_DataFree(data_handle);

    Beep(523,500);
}

int main(int argc, char **argv)
{
    int status = 0;
    std::fstream file;

    std::thread acquisition_thread;

    std::cout << "Connecting ... ";
    std::this_thread::sleep_for(std::chrono::milliseconds(5000));

    status = IEE_EngineConnect();
    if (status)
        throw std::runtime_error(get_error_info(status));
    std::cout << "OK" << std::endl;
    Beep(523,500);

    IEE_DataSetBufferSizeInSec(BUFFER_SIZE_IN_SEC);

    EmoEngineEventHandle event_handle = IEE_EmoEngineEventCreate();

    // Fixme
    while (true)
    // while (!GetAsyncKeyState(VK_ESCAPE))
    {
        if (IEE_EngineGetNextEvent(event_handle) == EDK_OK)
        {
            unsigned int user_id;

            IEE_Event_t event_type = IEE_EmoEngineEventGetType(event_handle);
            IEE_EmoEngineEventGetUserId(event_handle, &user_id);

#if USE_EVENT_LOGGING
            std::cout << '[' << user_id << "] EVENT: " << get_event_type(event_type) << std::endl;
#endif
            switch (event_type)
            {
            case IEE_UserAdded:
                acquisition_thread = std::thread(data_acuisition_handle, user_id);
                break;

            default:
                break;
            }
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    acquisition_thread.join();

    IEE_EmoEngineEventFree(event_handle);
    IEE_EngineDisconnect();

    return 0;
}
