from gamenum.numbergame import Gameuser
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command

BOT_TOKEN: str = ''
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
usersdict = {}

@dp.message(Command(commands=['start']))
async def proccessing_start(message: Message):
    user = usersdict.setdefault(str(message.from_user.id), Gameuser(message.from_user.id))
    await message.answer(text='Добро пожаловать в бот по игре:\n'
                              'Угадай число от 1 до 100\n'
                              'Инструкции - /help')

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
    usersdict[str(message.from_user.id)].cancelgame()
    if usersdict[str(message.from_user.id)].statusingame == False:
        await message.answer(text='Игра завершена')
    else:
        await message.answer(text='Что-то пошло не так, получил некорректный ответ от бэкенда')

@dp.message(Command(commands=['stat']))
async def proccessing_statistic(message: Message):
    status = usersdict[str(message.from_user.id)].statusingame
    countpop = f'Число попыток: {usersdict[str(message.from_user.id)].countchanses}'
    await message.answer(text='Вот твоя статистика\n'
                              f'{("Ты не в игре", "Ты в игре")[status]}\n'
                              f'{("Счета попыток нет, ты не в игре", countpop)[status]}\n'
                              f'Всего игр: {usersdict[str(message.from_user.id)].totalgames} из них побед: '
                              f'{usersdict[str(message.from_user.id)].wins}')

@dp.message(Text(text=['Да', 'Хочу поиграть'], ignore_case=True))
async def startgame(message: Message):
    status = usersdict[str(message.from_user.id)].statusingame
    if status is False:
        usersdict[str(message.from_user.id)].initgame()
        await message.answer(text='Игра началась, пиши только цифры от 1 до 100, цифру я загадал :)')
    else:
        await message.answer(text='Мы уже играем, пиши пожалуйста только цифры от 1 до 100')

@dp.message(Text(text=['Нет'], ignore_case=True))
async def answerno(message: Message):
    status = usersdict[str(message.from_user.id)].statusingame
    if status is True:
        await message.answer(text='Ты не закончил еще прошлую игру, вызови пожалуйста тогда /cancel')
    else:
        await message.answer(text='Жаль, возвращайся скорее! Чтобы начать, если захочешь, напиши мне "Хочу поиграть"')

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def game(message: Message):
    user = usersdict[str(message.from_user.id)]
    if user.statusingame is True:
        res = user.setstatus(int(message.text))
        if res is True:
            await message.answer(text='Ты победил, можешь проверить статистику - /stat')
    else:
        await message.answer(text='Мы не начали играть, сходи сюда /help')

if __name__ == '__main__':
    dp.run_polling(bot)