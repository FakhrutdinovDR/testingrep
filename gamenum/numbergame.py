from random import randint
class Gameuser:
    def __init__(self, userid: int):
        self.userid: int = userid
        self.statusingame: bool = False
        self.totalgames: int = 0
        self.wins: int = 0
        self.countchanses = None # По умолчанию, если не в игре

    def initgame(self): # Инициализация новой игры
        self.secrnum: int = randint(1, 101)
        print(f'{self.userid}: {self.secrnum}') # В консоль загаднное число
        self.statusingame: bool = True
        self.totalgames += 1
        self.countchanses = 5

    def validatenum(self, num: str): # Валидация введенного числа пользователем
        return int(num) == self.secrnum


    def setstatus(self, num: str):
        resultbool = self.validatenum(num)
        if resultbool is False and 2 <= self.countchanses <= 5:
            self.countchanses -= 1
            return False
        if resultbool is False and self.countchanses == 1:
            self.statusingame = False
            self.countchanses = None
            return False
        if resultbool is True:
            self.wins += 1
            self.statusingame = False
            self.countchanses = None
            return True

    def howmuch(self, num):
        return num < self.secrnum

    def cancelgame(self): # Прерывание игры, количество игр остается тем же, пользователь проиграл отменив
        self.statusingame = False
        self.countchanses = None




