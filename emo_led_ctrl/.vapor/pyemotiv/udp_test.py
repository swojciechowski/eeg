import numpy
import time

from client import Client
from server import Server

DEFAULT_IP = "localhost"
DEFAULT_PORT = 6666

PACKETS = 100


def data_generator():
    for _ in range(PACKETS):
        snd_data = numpy.random.rand(10)
        print('>', snd_data)
        yield snd_data.tobytes()
        time.sleep(0.1)


def data_handle(data):
    rcv_data = numpy.frombuffer(data)
    print('<', rcv_data)


if __name__ == '__main__':
    serv = Server(DEFAULT_IP, DEFAULT_PORT, data_generator)
    clnt = Client(DEFAULT_IP, DEFAULT_PORT, data_handle)

    print("Starting Test ...")

    serv.start()
    clnt.start()

    try:
        time.sleep(10)
    except Exception as e:
        print("Test canceled")
        print(str(e))
    finally:
        serv.join()
        clnt.join()

    print("Done")

