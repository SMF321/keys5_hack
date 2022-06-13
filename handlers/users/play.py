from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from data.config import ADMINS
from states.bot_states import States_Zagotovka
from keyboards.default.bot_button import *
from loader import dp
from utils.db_api.DB_functions import Dueling

#Набор функционала для игры
@dp.message_handler(state=States_Zagotovka.priglos, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    id = Dueling.get_id(message.chat.id)
    if message.text == priglos[0]:
        await dp.bot.send_message(id, f'Приглашение {message.chat.first_name} приянто')
        await dp.bot.send_message(id, f'Внимание вопрос!!!!')
        await message.answer(f'Внимание вопрос!!!!')
        photo = open('vopros.jpg', 'rb')
        await dp.bot.send_photo(id,photo,reply_markup=add_button(test_vopros))
        photo = open('vopros.jpg', 'rb')
        await message.answer_photo(photo,reply_markup=add_button(test_vopros))
        state1 = dp.current_state(chat=id, user=id)
        await state1.set_state(States_Zagotovka.vopros_otvet)
        await States_Zagotovka.vopros_otvet.set()
    elif message.text == priglos[1]:
        await dp.bot.send_message(id, f'Приглашение {message.chat.username} отклонено ')
        state1 = dp.current_state(chat=id, user=id)
        await state1.set_state(States_Zagotovka.user_menu)
        await dp.bot.send_message(id,f"Меню пользователя:",reply_markup=add_button(user_bat))
        await States_Zagotovka.user_menu.set()
        await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))

@dp.message_handler(state=States_Zagotovka.vopros_otvet, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    ids = Dueling.get_ids(message.chat.id)
    if message.text == test_vopros[2]:
        # await message.answer_sticker('CAACAgIAAxkBAAEE8A5ioHxoplI2aUoObmgG87ALV-DBlAACGhoAAriIAAFJY4R42V0X5BQkBA')
        await dp.bot.send_message(ids[0], f'{message.chat.username} ответил первее и правильно')
        await dp.bot.send_message(ids[1], f'{message.chat.username} ответил первее и правильно')
        state1 = dp.current_state(chat=ids[0], user=ids[0])
        await state1.set_state(States_Zagotovka.user_menu)
        state1 = dp.current_state(chat=ids[1], user=ids[1])
        await state1.set_state(States_Zagotovka.user_menu)
        await dp.bot.send_message(ids[1],f"Меню пользователя:",reply_markup=add_button(user_bat))
        await dp.bot.send_message(ids[0],f"Меню пользователя:",reply_markup=add_button(user_bat))
    else:
        await message.answer('Ответ неверный')
        await States_Zagotovka.user_menu.set()
        await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))