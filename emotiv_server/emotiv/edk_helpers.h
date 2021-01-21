#ifndef EDK_HELPERS_H_
#define EDK_HELPERS_H_

#include "IEegData.h"

IEE_DataChannel_t *get_channel_list();

int get_channel_list_size();

char const *get_error_info(int error);

char const *get_event_type(IEE_Event_t event);

char const *get_channel_name(IEE_DataChannel_t channel);

void print_headset_config(const unsigned int &user_id);

#endif /* EDK_HELPERS_H_ */
