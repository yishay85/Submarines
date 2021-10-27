class Sub:
    def __init__(self, cells):
        self.cells = cells
        self.is_dead = 0

    def Hit(self):
        """
        בודק האם הפגיעה גרמה להשמדת הצוללת
        :return: 1 אם כן
        """
        hitcells = list(filter(lambda x: x.isHit(), self.cells))
        if len(hitcells) == len(self.cells):
            self.is_dead = 1
        return self.is_dead

    def SockString(self):
        buf = ",".join(map(lambda x: x.SockString(), self.cells))
        return buf
