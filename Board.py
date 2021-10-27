from Cell import *
from Sub import *
from functools import reduce


class Board:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.cells = []
        for x in range(rows):
            self.cells.append([])
            for y in range(columns):
                self.cells[x].append(Cell(x, y))
        self.subs = []
        self.is_done = 0

    def AddSub(self, cells):
        # go over cells - check space legality
        for c in cells:
            # check that cell is empty
            if c.state != 0:
                return 0, "Sub located on non empty cell"
            # check that its neighbors are empty
            for x_ in range(c.x - 1, c.x + 2):
                for y_ in range(c.y - 1, c.y + 2):
                    if not (x_ == c.x and y_ == c.y) and not self.IsCellEmpty(x_, y_):
                        return 0, "You can not put the submarine, there is a submarine nearby!"
            # check that all cells of the sub are adjacent
            found_adjacent = 0
            for c_ in cells:
                if c.IsAdjacent(c_):
                    found_adjacent = 1
            if not found_adjacent and len(cells) > 1:
                return 0, "cells do not constrct a sub!"
        # all is legal- create a sub on the board
        sub = Sub(cells)
        self.subs.append(sub)
        # go over cells and mark submarin
        for c in cells:
            c.SetSub(sub)
        return 1, "OK"

    def IsCellEmpty(self, x, y):
        if x < 0 or x >= self.columns or y < 0 or y >= self.rows:  # out of range
            return 1
        elif self.cells[x][y].state == 0:  # empty cell
            return 1
        return 0

    def Hit(self, x, y):
        """
        המטודה מחזירה 1 במידה והיה פגיעה (ז"א תור נוסף)
        :return:
        """
        c = self.cells[x][y]
        if c.Hit():
            if c.mySub.is_dead:
                print("S")
                # mark all cells of sub as dead
                map(lambda x: x.SetDead(), c.mySub.cells)
                # mark all neighboring cells as Miss
                for c_ in c.mySub.cells:
                    for x_ in range(c_.x - 1, c_.x + 2):
                        for y_ in range(c_.y - 1, c_.y + 2):
                            self.MarkAsMiss(x_, y_)
                # check if all subs are dead
                if reduce(lambda x, y: x and y, map(lambda z: z.is_dead, self.subs)):
                    self.is_done = 1
                return 2  # killed sub
            return 1  # hit sub
        return 0  # missed

    def MarkAsMiss(self, x, y):
        if x < 0 or x >= self.columns or y < 0 or y >= self.rows:  # out of range
            return
        elif self.cells[x][y].state == 0:  # empty cell
            self.cells[x][y].state = 2  # miss

    def ToString(self, is_private=1):
        """
        שרשור הלוח
        :param is_private: של מי הלוח
        :return: מחזיר את הלוח כסטרינג
        """
        s = "   "
        s += " ".join(map(lambda x: str(x % 10), range(self.columns)))
        s += "\n"
        for x in range(self.rows):
            s += str(x % 10) + " "
            for y in range(self.columns):
                s += " " + self.cells[x][y].ToString(is_private)
            s += "\n"
        return s
