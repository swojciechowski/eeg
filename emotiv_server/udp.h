#ifndef UDP_H_
#define UDP_H_

#define DEFAULT_PORT "6666"
#define DEFAULT_SERVER_ADDR "127.0.0.1"

void udp_connect();

void send_message(char *sendbuf, unsigned int bufsize);

void udp_disconnect();

#endif /* UDP_H_ */
