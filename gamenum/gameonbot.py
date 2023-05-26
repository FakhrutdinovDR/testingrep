from gamenum.numbergame import Gameuser
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command
import pickle
import os

BOT_TOKEN: str = ''
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
usersdict = {}
if os.path.exists('baseusers.pkl'):
    with open('baseusers.pkl', 'rb') as file:
        data = pickle.load(file)
        for key, value in data.items():
            usersdict.setdefault(key, value)

def writeupdateusers(): # Обновление инфы о юзерах
    with open('baseusers.pkl', 'wb') as file:
        pickle.dump(usersdict, file)

@dp.message(Command(commands=['start']))
async def proccessing_start(message: Message):
    usersdict.setdefault(str(message.from_user.id), Gameuser(message.from_user.id))
    writeupdateusers()
    await message.answer(text='Добро пожаловать в бот по игре:\n'
                              'Угадай число от 1 до 100\n'
                              'Инструкции - /help\n'
                              'Хочешь начать играть? На любом этапе, если не играешь напиши да')

@dp.message(Command(commands=['help']))
async def proccessing_help(message: Message):
    await message.answer(text='Правила у игры просты:\n'
                              'Чтобы начать отправь мне Да\n'
                              'Если не хочешь, то Нет\n'
                              'Попыток отгадать мое число будет ровно 5\n'
                              'Если не захочешь играть - сообщи мне командой /cancel\n'
                              'Посмотреть статистику - /stat\n'
                              'Сыграем?')

@dp.message(Command(commands=['cancel']))
async def proccesing_cancelgame(message: Message):
    user = usersdict[str(message.from_user.id)]
    user.cancelgame() # Отмена игры
    if not user.statusingame:
        await message.answer(text='Игра завершена')
    else:
        await message.answer(text='Что-то пошло не так, получил некорректный ответ от бэкенда')

@dp.message(Command(commands=['stat']))
async def proccessing_statistic(message: Message):
    user = usersdict[str(message.from_user.id)]
    countpop = f'Число попыток: {user.countchanses}'
    await message.answer(text='Вот твоя статистика\n'
                              f'{("Ты не в игре", "Ты в игре")[user.statusingame]}\n'
                              f'{("Счета попыток нет, ты не в игре", countpop)[user.statusingame]}\n'
                              f'Всего игр: {user.totalgames} из них побед: '
                              f'{user.wins}')

@dp.message(Text(text=['Да', 'Хочу поиграть', 'Давай', 'Сыграем'], ignore_case=True))
async def startgame(message: Message):
    user = usersdict[str(message.from_user.id)]
    if not user.statusingame:
        user.initgame()
        await message.answer(text='Игра началась, пиши только цифры от 1 до 100, цифру я загадал :)')
    else:
        await message.answer(text='Мы уже играем, пиши пожалуйста только цифры от 1 до 100')

@dp.message(Text(text=['Нет', 'Не хочу', 'Не буду', 'Давай потом'], ignore_case=True))
async def answerno(message: Message):
    user = usersdict[str(message.from_user.id)]
    if user.statusingame:
        await message.answer(text='Ты не закончил еще прошлую игру, вызови пожалуйста тогда /cancel')
    else:
        await message.answer(text='Жаль, возвращайся скорее! Чтобы начать, если захочешь, напиши мне "Хочу поиграть"')

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def game(message: Message):
    user = usersdict[str(message.from_user.id)]
    if user.statusingame:
        res = user.setstatus(int(message.text))
        if res:
            await message.answer(text='Ты победил, можешь проверить статистику - /stat')
            writeupdateusers()
        if not res and user.countchanses is not None:
            await message.answer(text=f'К сожалению, ты не угадал число, у тебя еще {user.countchanses} попыток')
            if user.howmuch(int(message.text)):
                await message.answer(text='Я бы попробовал число по выше')
            else:
                await message.answer(text='Я бы попробовал число по ниже')
        if not res and user.countchanses is None:
            await message.answer(text='Ты проиграл, попробуем еще раз? Да/Нет\n'
                                      'Посмотреть статистику - /stat')
            writeupdateusers()
    else:
        await message.answer(text='Мы не начали играть, сходи сюда /help, либо напиши хочу играть')

@dp.message()
async def proccessing_anyword(message: Message):
    user = usersdict[str(message.from_user.id)]
    if user.statusingame:
        await message.answer(text='Идет игра, пиши только цифры пожалуйста, либо заверши игру - /cancel')
    else:
        await message.answer(text='Я умею только играть, если нужны инструкции - /help')

if __name__ == '__main__':
    dp.run_polling(bot)