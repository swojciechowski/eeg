#include "udp.h"

#include <iostream>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

static int active_socket = -1;

struct sockaddr_in serv_addr;

void udp_connect() {
	struct hostent *server;
    active_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    int portno = atoi(DEFAULT_PORT);

    if (active_socket == -1) {
    	std::cout << "Socket error" << std::endl;
    	return;
    }

    server = gethostbyname(DEFAULT_SERVER_ADDR);

    if (server == NULL) {
    	std::cout << "Server error" << std::endl;
    	return;
    }

    // build an internet socket address structure, defining port.
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family      = AF_INET;
    serv_addr.sin_addr.s_addr = ((struct in_addr *)(server->h_addr))->s_addr;
    serv_addr.sin_port        = htons(portno);

    /* connect to PORT on HOST */
	if (connect(active_socket,(struct sockaddr *)  &serv_addr, sizeof(serv_addr)) == -1) {
		std::cout << "Connect error" << std::endl;
		exit(1);
	}

    bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons(portno);
}

void send_message(char *sendbuf, unsigned int bufsize) {
	sendto(active_socket, sendbuf, bufsize, 0 , (struct sockaddr *) &serv_addr, sizeof(serv_addr));
}

void udp_disconnect() {
	 close(active_socket);
}
