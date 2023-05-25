from random import randint
class Gameuser:
    def __init__(self, userid: int):
        self.userid: int = userid
        self.statusingame: bool = False
        self.totalgames: int = 0
        self.wins: int = 0
        self.countchanses = None

    def initgame(self):
        self.secrnum: int = randint(1, 101)
        print(self.secrnum)
        self.statusingame: bool = True
        self.totalgames += 1
        self.countchanses = 5

    def validatenum(self, num: str):
        if int(num) != self.secrnum:
            return False
        else:
            return True

    def setstatus(self, num: str):
        resultbool = self.validatenum(num)
        if resultbool is False and self.countchanses > 0:
            self.countchanses -= 1
            return False
        if resultbool is False and self.countchanses == 0:
            self.statusingame = False
            self.countchanses = None
            return False
        if resultbool is True:
            self.wins += 1
            self.statusingame = False
            self.countchanses = None
            return True


    def cancelgame(self):
        self.statusingame = False
        self.countchanses = None




