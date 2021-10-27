class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 0  # empty
        self.mySub = 0

    def isHit(self):
        return self.state == 3

    def IsAdjacent(self, cell):
        """
        בודק אם התאים הם שכנים
        :param cell:    תא נוסף
        :return: אמת- אם התאים שכנים
        """
        return abs(self.x - cell.x) == 1 and self.y == cell.y or abs(
            self.y - cell.y) == 1 and self.x == cell.x

    def Hit(self):
        """
        בודק אם יש פגיעה בצוללת ומעדכן בהתאם
        :return: 1 אם הייתה פגיעה
        """
        if self.state == 0:
            self.state = 2
            return 0
        elif self.state == 1:
            self.state = 3
            self.mySub.Hit()
            return 1

    def SetSub(self, sub):
        """
        מעדכן שיש צוללת בתא
        :param sub: הצוללת
        :return: None
        """
        self.state = 1
        self.mySub = sub

    def SetDead(self):
        self.state = 4  # dead

    def ToString(self, is_private=1):
        if self.state == 0:  # empty
            return '.'
        elif self.state == 1:  # miss
            if is_private:
                return '0'
            else:
                return '.'
        elif self.state == 2:
            return '*'  # miss
        elif self.state == 3:
            return '@'  # hit
        elif self.state == 4:
            return '#'  # dead

    def SockString(self):
        buf = ""
        ## - Remember to write about this kind of initialization as python type declaration
        buf += str(self.x) + ":" + str(self.y)
        return buf
