#include "udp.h"

#include <iostream>
#include <winsock2.h>

static WSADATA wsaData;
static SOCKET SendingSocket;
static SOCKADDR_IN ReceiverAddr;
static int Port = 8888;

void udp_connect()
{
    if( WSAStartup(MAKEWORD(2,2), &wsaData) != 0){
        WSACleanup();
        return;
    }

    SendingSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (SendingSocket == INVALID_SOCKET){
        WSACleanup();
        return;
    }

    /*Set up a SOCKADDR_IN structure that will identify who we will send datagrams to.*/
    ReceiverAddr.sin_family = AF_INET;
    ReceiverAddr.sin_port = htons(Port);
    ReceiverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
}

void send_message(char *sendbuf, unsigned int bufsize)
{
    sendto(SendingSocket, sendbuf, bufsize, 0, (SOCKADDR *)&ReceiverAddr, sizeof(ReceiverAddr));
}

void udp_disconnect()
{
    closesocket(SendingSocket);
    WSACleanup();
}