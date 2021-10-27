# Server
# For more info: https://docs.python.org/2/library/socket.html
from socket import *  # Import socket module
from os import system

RECV_SIZE = 1024


class Server_Handler:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.c = None

    def Connection(self):
        """
        connection to server and whit to the client
        :return: None
        """
        try:
            system(
                f'netsh advfirewall firewall add rule name="Open Port {self.PORT}" dir=in action=allow protocol=TCP localport={self.PORT} remoteip={self.HOST}')
            with socket() as s:  # Create a socket object
                print('Server started!')
                print('Waiting for clients...')
                s.bind((self.HOST, self.PORT))  # Bind to the port
                s.listen(5)  # Now wait for client connection.
                self.c, addr = s.accept()  # Establish connection with client.
                # Remote client machine connection
                print('Got connection from', addr)
        except error as strerror:
            print("Network problems:", strerror)
            return 0
        return 1

    def Send(self, stringSend):
        """
        sending a message to the client
        :param stringSend: the string to send
        :return: None
        """
        self.c.send(stringSend.encode())

    def Recv(self):
        """
        getting message from the client
        :return: the message from the client
        """
        return self.c.recv(RECV_SIZE).decode('UTF-8')
