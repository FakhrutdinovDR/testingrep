from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

API_TOKEN = ''
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start']))
async def proccesing_start_answer(message: Message):
    await message.answer('Здарова, ты попугай')

@dp.message(F.photo)
async def proccessing_photo(message: Message):
    await message.answer_photo(photo=message.photo[0].file_id)

@dp.message()
async def proccessing_anything(message: Message):
    await message.answer_photo(photo='https://www.meme-arsenal.com/memes/087f286f5440d6fb308d063d5646a204.jpg')
    await message.answer(text='Пиши по понятнее, над тобой Том ржет')


if __name__ == '__main__':
    dp.run_polling(bot)


