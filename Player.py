import socket

from Server import *
from Client import *
from Board import *
from main import *

RECV_SIZE = 1024


class Player:
    def __init__(self, board_size=0, subs_level=0):
        self.soc = None
        self.board_size = board_size
        self.subs_level = subs_level

    def RecvMove(self):
        buf = self.soc.Recv()
        x, y = buf.split(':')
        return int(x), int(y)

    def GetMoveFromOtherPlayer(self):
        print("Waiting for opponent to move...")
        x, y = self.RecvMove()
        hit = self.my_board.Hit(x, y)
        if hit == 0:
            print("Opponent missed...")
        elif hit == 1:
            print("You were hit!")
        else:
            print("You were hit and lost a submarine!")
        self.PrintBoard()
        return hit

    def GetMoveFromPlayer(self):
        x, y = my_input("Please enter your guess: ", self.CheckCoordinates)
        self.soc.Send(str(x) + ":" + str(y))
        hit = self.other_board.Hit(int(x), int(y))
        if hit == 0:
            print("You missed...")
        elif hit == 1:
            print("You hit!")
        else:
            print("You hit and sunk a submarine!")
        self.PrintBoard()
        return hit

    def Game(self, other_player_start=0):
        while True:
            if other_player_start:
                while self.GetMoveFromOtherPlayer():
                    if self.my_board.is_done:
                        print("You lost!")
                        return
                    else:
                        print("Opponent has another turn")
                other_player_start = 0
            else:
                while self.GetMoveFromPlayer():
                    if self.other_board.is_done:
                        print("You Win")
                        return
                    else:
                        print("You have another turn")
                other_player_start = 1

    def CheckCoordinates(self, string):
        x_s, y_s = string.split(' ')
        x, y = int(x_s), int(y_s)
        if x < 0 or x >= self.board_size or y < 0 or y >= self.board_size:
            raise ValueError("The coordinates should be between 0 and " + str(self.board_size))
        return x, y

    def PrintBoard(self):
        print("Your Board")
        print(self.my_board.ToString())
        print("Competitor Board")
        print(self.other_board.ToString(0))

    # -----------------------------------------#
    #           Functions for Client           #
    # -----------------------------------------#

    def RunClient(self, IP, PORT):
        self.soc = Client(IP, PORT)
        # connect to server
        print("Connecting to play...")
        if not self.ConnnectPlayer():
            return
        print("... Done.")
        self.GetSubsFromPlayer()
        # read subs from other player
        print("Waiting for opponent to select subs...")
        self.RecvSubs()
        # send subs to other player
        self.SendSubs()
        print("... Done.")
        # play the game!
        self.Game()

    def ConnnectPlayer(self):
        if not self.soc.Connection():
            return 0
        buf = self.soc.Recv()
        size_s, subs_level_s = buf.split(' ')
        self.board_size = int(size_s)
        self.subs_level = int(subs_level_s)
        # FF read num of subs and sizes using ConfigParser
        self.UpdateBoard()
        return 1

    # -----------------------------------------#
    #           Functions for server           #
    # -----------------------------------------#
    def RunServer(self, HOST, PORT):
        self.soc = Server_Handler(HOST, PORT)
        if not self.AcceptPlayer():
            return
        self.GetSubsFromPlayer()
        # send subs to other player
        self.SendSubs()
        # read subs from other player
        print("Waiting for opponent to select subs...")
        self.RecvSubs()
        # play the game!
        self.Game(1)

    def AcceptPlayer(self):
        if self.soc.Connection():
            buf = str(self.board_size) + " " + str(self.subs_level)
            self.soc.Send(buf)
            self.UpdateBoard()
            return 1
        else:
            return 0

    # ---------------------------------------------------#
    #       Common functions for server and client       #
    # ---------------------------------------------------#
    def UpdateBoard(self):
        self.my_board = Board(self.board_size, self.board_size)
        self.other_board = Board(self.board_size, self.board_size)

    def GetSubsFromPlayer(self):
        print("Please enter the locations of your subs:")
        for sub_size in range(self.subs_level, 0, -1):
            for i in range(self.subs_level - sub_size + 1):
                rc = 0
                while rc == 0:
                    print("Please enter sub of size", sub_size)
                    sub = []
                    for c in range(sub_size):
                        x, y = my_input("Please enter coordinates of cell " + str(c) + ": ", self.CheckCoordinates)
                        sub.append(self.my_board.cells[y][x])
                    rc, err = self.my_board.AddSub(sub)
                    if rc == 0:
                        print("Bad input given:", err)
                    else:
                        print("Your Board:")
                        print(self.my_board.ToString())

    def SendSubs(self):
        buf = " ".join(map(lambda x: x.SockString(), self.my_board.subs))
        self.soc.Send(buf)

    def RecvSubs(self):
        buf = self.soc.Recv()
        print(buf)
        for sub_str in buf.split(' '):
            cells = []
            for cell_str in sub_str.split(','):
                x, y = cell_str.split(':')
                cells.append(self.other_board.cells[int(x)][int(y)])
                # I assume that errors are detected at opponent's side
            self.other_board.AddSub(cells)
