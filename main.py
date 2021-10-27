from Cell import *

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
from Player import *
from socket import gethostname

HOST = gethostname()
PORT = 12345


def my_input(messag, type_func=str):
    ok = 0
    while not ok:
        try:
            x = input(messag)
            y = type_func(x)
            ok = 1
        except ValueError as e:
            print("Bad value givne ", e, "Try agian")

    return y


def int_input(messag):
    return my_input(messag, int)


def is_server_client(string):
    if string.lower() not in ["s", "c"]:
        raise ValueError("not s or c.")
    return string.lower()


if __name__ == '__main__':
    try:
        s_c = my_input("Press S to run a server, C to run a client: ", is_server_client)
        if s_c == "s":
            board_size = int_input("What is the board size? ")
            subs_level = int_input("What is the submarines level? ")
            s = Player(board_size, subs_level)
            s.RunServer(HOST, PORT)
        else:
            s = Player()
            s.RunClient(HOST, PORT)
    except KeyboardInterrupt:
        print("\n\nProgram stopped.\nGoodBye.")

