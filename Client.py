# Client
# For more info: https://docs.python.org/2/library/socket.html
from socket import *

RECV_SIZE = 1024


class Client:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.s = socket()

    def Connection(self):
        try:
            self.s.connect((self.HOST, self.PORT))
        except ConnectionRefusedError:  # Couldn't establish a connection to the remote host
            print("No connection could be made because the target machine refused it")
            return 0
        except ConnectionResetError:  # The established connection was reset by the remote host
            print("An existing connection was forcibly closed by the remote host")
            return 0

        return 1

    def Send(self, stringSend):
        """
        sending a message to the client
        :param stringSend: the string to send
        :return: None
        """
        self.s.send(stringSend.encode())

    def Recv(self):
        """
        getting message from the client
        :return: the message from the client
        """
        return self.s.recv(RECV_SIZE).decode('UTF-8')
