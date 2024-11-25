from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from admin import*




api = "7527901227:AAF9qrgQGQ8EItHrb1HACw2Q5sK6ons9_VM"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = 'Рассчитать'),
            KeyboardButton(text = 'Информация')
        ],
        [KeyboardButton(text = 'Купить')]
    ], resize_keyboard = True
)

check_menu=InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data = "calories")],
        [InlineKeyboardButton(text="Формулы расчёта", callback_data = "formulas")]
    ]
)



buy_menu=InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = 'Product1', callback_data = 'product_buying')],
        [InlineKeyboardButton(text = 'Product2', callback_data = 'product_buying')],
        [InlineKeyboardButton(text = 'Product3', callback_data = 'product_buying')],
        [InlineKeyboardButton(text = 'Product4', callback_data = 'product_buying')]
    ]
)

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пользователи",callback_data="users")],
        [InlineKeyboardButton(text= "Статистика",callback_data="stat")],
        [
        InlineKeyboardButton(text="Блокировка",callback_data="block"),
        InlineKeyboardButton(text="Разблокировка",callback_data="unblock")
        ]
    ]
)

import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INT PRIMARY KEY,
title TEXT NOT NULL,
description TEXT NOT NULL,
price INT NOT NULL
)
''')
cursor.execute("DELETE FROM Products")
for num in range(4):
    cursor.execute("INSERT INTO Products(id,title, description,price)VALUES(?,?,?,?)",(f"{num+1}",f"Продукт{num+1}",f"Описание{num+1}",f"{num*100}"))
    #cursor.execute("UPDATE Products SET price = ? WHERE id +?", (100,0))
    connection.commit()

def get_all_products():
    cursor.execute('SELECT*FROM Products')
    return cursor.fetchall()

connection.commit()
connection.close()


@dp.message_handler(commands= ['start'])
async def start(message):
     await message.answer(f"Привет! Я бот помогающий твоему здоровью",reply_markup = start_menu)

@dp.message_handler(text='Products')
async def get_all_products(message):
    await message.answer()
@dp.message_handler(text='Купить')
async def get_all_products(message):
    with open('1.png',"rb")as img:
        await message.answer_photo(img,f"Название: title1/Описание discription:/Цена:price{100}",reply_markup=start_menu)
    with open('2.png', "rb") as img:
        await message.answer_photo(img,f"Название:title2 /Описание discription:/Цена:price{200}",reply_markup=start_menu)
    with open('3.jpg', "rb") as img:
        await message.answer_photo(img,f"Название: title3/Описание discription:/Цена:price{300}",reply_markup=start_menu)
    with open('4.jpg', "rb") as img:
        await message.answer_photo(img,f"Название: title4/Описание discription:/Цена:price{400}",reply_markup=start_menu)
        await message.answer(" Выберите продукт для покупки:",reply_markup=buy_menu)

#@dp.message_handler(text='Информация')
#async def info(message):
    #await message.answer("Выберите продукт для покупки:",reply_markup=start_menu2)
@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer("Выбери опцию:",reply_markup=check_menu)

@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    await call.message.answer("10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(г) - 161")
    await call.answer()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()
    await call.answer()
@dp.message_handler(state = UserState.age)
async def set_growth(message,state):
    await state.update_data(age=message.text)
    await message.answer(f"Введите свой рост")
    await UserState.growth.set()
@dp.message_handler(state=UserState.growth)
async def set_weight(message,state):
    await state.update_data(growth=message.text)
    await message.answer(f"Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message,state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories_wom = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f"Ваша норма калорий {calories_wom}")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)