from datetime import time, timedelta
import random
from aiogram import Bot, types
from aiogram.dispatcher import FSMContext

from states.bot_states import States_Zagotovka
from keyboards.default.bot_button import *
from keyboards.inline.inline_botton import *
from aiogram.dispatcher.filters import Text
from loader import dp,bot
from utils.db_api.DB_functions import Competitions, FuncM, Test, mailing_list, mood

# Сделать рассылку по пользователям (приглашение на вебинар и прочее), добавленмие задачек + удаление задачек

@dp.message_handler(state=States_Zagotovka.admin_menu, content_types=types.ContentTypes.TEXT)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == admin_bat[0]:
        await message.answer(f"Введите текст рассылки:")
        await States_Zagotovka.text_rassilka.set()
    elif message.text == admin_bat[1]:
        await message.answer('В какую категорию хотите добывить вопрос?',reply_markup=add_button(category))
        await States_Zagotovka.vibor_testa.set()
    elif message.text == admin_bat[2]:
        msg = 'Отзывы пользователей:\n'
        ids = FuncM.GET_ID()
        for i in range(len(ids)):
            msg = msg +f'@{FuncM.get_username_by_id1(ids[i])}\n'
            for index,x in enumerate(FuncM.get_feedback(ids[i])):
                if x == '':
                    continue
                else:
                    msg = msg +f'{index+1}-й отзыв: '+ f'{x}'+'\n'
            msg = msg +'\n'
        await message.answer(f'{msg}')
        await States_Zagotovka.admin_menu.set()
        await message.answer(f"Меню админа:",reply_markup=add_button(admin_bat))
    elif message.text == admin_bat[3]:
        await message.answer('Добавьте эмоциональный тон вопроса',reply_markup=add_button(mood_bat))
        await States_Zagotovka.add_mood.set()
    else:
        await message.answer(f"Что-то пошло не так...")
        # await message.answer(f"Меню админа:",reply_markup=admin_inline_keyboad)

@dp.message_handler(state=States_Zagotovka.add_mood, content_types=types.ContentTypes.TEXT)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text in mood_bat:
        mood.post_question_mood(message.text)
        await message.answer('Добавьте вопрос интеллектуальной рефлексии')
        await States_Zagotovka.add_mood1.set()

@dp.message_handler(state=States_Zagotovka.add_mood1, content_types=types.ContentTypes.TEXT)
async def bot_echo_all(message: types.Message, state: FSMContext):
    mood.post_question(message.text)
    await message.answer('Вопрос добавлен!')
    await States_Zagotovka.admin_menu.set()
    await message.answer(f"Меню админа:",reply_markup=add_button(admin_bat))


@dp.message_handler(state=States_Zagotovka.vibor_testa, content_types=types.ContentTypes.TEXT)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == 'Для соревнований':
        await message.answer('Прикрепите фотографию для вопроса')
        await States_Zagotovka.competition_wopros.set()
    elif message.text == 'Для проверки зананий':
        await message.answer('Прикрепите фотографию для вопроса')
        await States_Zagotovka.test_wopros.set()


@dp.message_handler(state=States_Zagotovka.competition_wopros, content_types=types.ContentTypes.PHOTO)
async def bot_echo_all(message: types.Message, state: FSMContext):
    file_info = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file_info.file_path,destination_dir="C:/hakaton/preparation_for_the_hackathon/utils/db_api")
    await States_Zagotovka.competition_answer.set()
    await message.answer('Напишите правильный ответ')
    Competitions.post_question(str(random.randint(1, 10000)),file_info.file_path.split('photos/')[1])

@dp.message_handler(state=States_Zagotovka.competition_answer, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    Competitions.post_answer(message.text)
    await message.answer("Напишите все вариатны ответов через '|' \n( Например : Ответ1|Ответ2|Ответ3 )")
    await States_Zagotovka.competition_varianti_otveta.set()

@dp.message_handler(state=States_Zagotovka.competition_varianti_otveta, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    Competitions.post_words(message.text)
    await message.answer("Напишите весовой коэффициент сложности вопроса")
    await States_Zagotovka.competition_ves.set()

@dp.message_handler(state=States_Zagotovka.competition_ves, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    Competitions.post_weight(message.text)
    await States_Zagotovka.admin_menu.set()
    await message.answer(f"Меню админа:",reply_markup=add_button(admin_bat))

@dp.message_handler(state=States_Zagotovka.test_wopros, content_types=types.ContentTypes.PHOTO)
async def bot_echo_all(message: types.Message, state: FSMContext):
    file_info = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file_info.file_path,destination_dir="C:/hakaton/preparation_for_the_hackathon/utils/db_api")
    await States_Zagotovka.test_answer.set()
    await message.answer('Напишите правильный ответ')
    Test.post_test_question(str(random.randint(1, 10000)),file_info.file_path.split('photos/')[1])

@dp.message_handler(state=States_Zagotovka.test_answer, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    Test.post_test_answer(message.text)
    await message.answer("Напишите все вариатны ответов через '|' \n( Например : Ответ1|Ответ2|Ответ3 )")
    await States_Zagotovka.test_varianti_otveta.set()

@dp.message_handler(state=States_Zagotovka.test_varianti_otveta, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    Test.post_test_words(message.text)
    await message.answer("Напишите весовой коэффициент сложности вопроса")
    await States_Zagotovka.test_ves.set()

@dp.message_handler(state=States_Zagotovka.test_ves, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    Test.post_test_weight(message.text)
    await message.answer("Напишите к какой теме будет относться данный вопрос")
    await States_Zagotovka.test_tema.set()

@dp.message_handler(state=States_Zagotovka.test_tema, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):   
    Test.post_modul(message.text)
    await message.answer("Вопрос добавлен")
    await States_Zagotovka.admin_menu.set()
    await message.answer(f"Меню админа:",reply_markup=add_button(admin_bat))

@dp.message_handler(state=States_Zagotovka.text_rassilka, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    mailing_list.post_text(message.text)
    await message.answer('Прикрепить картинку к данному сообщению?',reply_markup=add_button(yes_no))
    await States_Zagotovka.if_png_Jpg.set()

@dp.message_handler(state=States_Zagotovka.if_png_Jpg, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == yes_no[0]:
        await message.answer('Прикрепите фотографию')
        await States_Zagotovka.png_jpg.set()
    elif message.text == yes_no[1]:
        await message.answer('Такое сообщение Вы хотите отправить?\nДалее будет собранное сообщение',reply_markup=add_button(yes_no))
        await States_Zagotovka.yes_no.set()




@dp.message_handler(state=States_Zagotovka.png_jpg, content_types=types.ContentTypes.PHOTO)
async def bot_echo_all(message: types.Message, state: FSMContext):
    file_info = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file_info.file_path,destination_dir="utils/db_api/")
    mailing_list.post_image(file_info.file_path.split('photos/')[1])
    # if message.text == 'Все':
    await message.answer('Такое сообщение Вы хотите отправить?\nДалее будет собранное сообщение',reply_markup=add_button(yes_no))
    all_message = mailing_list.get_all()
    media = types.MediaGroup()
    # try:
    if len(all_message[0]) > 1:
        # for i in range(len(all_message)):
        media.attach_photo(types.InputFile('utils/db_api/photos/'+all_message[1],f'{all_message[0]}'), all_message[0])
        await message.answer_media_group(media=media)
        await States_Zagotovka.yes_no.set()
    elif len(all_message[0]) == 1:
        media.attach_photo(types.InputFile('utils/db_api/photos/'+all_message[1]), all_message[0])
        await message.answer_media_group(media=media)
        await States_Zagotovka.yes_no.set()
        # except:
        #     # await message.answer(all_message[1])
        #     await States_Zagotovka.yes_no.set()

@dp.message_handler(state=States_Zagotovka.yes_no, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == yes_no[0]:
        await message.answer('Данное сообщение будет отправлено пользователям бота')
        for i in FuncM.GET_ID():
            # await dp.bot.send_message(chat_id=i,text='Рассылка админа')
            all_message = mailing_list.get_all()
            # print(all_message)
            media = types.MediaGroup()
            if len(all_message[0]) > 1:
            # for i in range(len(all_message)):
                media.attach_photo(types.InputFile('utils/db_api/photos/'+all_message[1],f'{all_message[0]}'), all_message[0])
                await dp.bot.send_media_group(chat_id=i,media=media)
                await States_Zagotovka.yes_no.set()
            elif len(all_message[0]) == 1:
                media.attach_photo(types.InputFile('utils/db_api/photos/'+all_message[1],f'{all_message[0]}'), all_message[0])
                await dp.bot.send_media_group(chat_id=i,media=media)
                await States_Zagotovka.yes_no.set()
        mailing_list.clear_table()
        await States_Zagotovka.admin_menu.set()
        await message.answer(f"Меню админа:",reply_markup=add_button(admin_bat))
    elif message.text == yes_no[1]:
        await message.answer('Придется заполнить ещё раз. Какое сообщение хотите отправить пользователям?')
        await States_Zagotovka.text_rassilka.set()


