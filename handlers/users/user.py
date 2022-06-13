import os
import random
import re
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.bot_states import States_Zagotovka
from keyboards.default.bot_button import *
from keyboards.inline.inline_botton import *
from datetime import time, timedelta
from loader import dp, scheduler
from utils.db_api.DB_functions import FEEDBACK, Answer_mood, Dueling, FuncM, Test, answer_mood, mood
from prettytable import PrettyTable
import time
from datetime import datetime

from utils.statistics.BD_statistic import Cloud
from utils.statistics.Graphs import Statistics
from utils.statistics.circle_diagram import circle_diagram
# В данном файле расположен весь
# функционал бота
@dp.message_handler(state=States_Zagotovka.user_menu, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == user_bat[0]:
        await States_Zagotovka.week_state.set()
        await message.answer(f"Выберите действие",reply_markup=add_button(reminder_menu))
        await States_Zagotovka.reminder_state.set()
    elif message.text == user_bat[1]:
        # await States_Zagotovka.statistics.set()
        await message.answer('Пару секунд и графики будут готовы')
        Statistics(message.chat.id,FEEDBACK.get_all_answers(message.chat.id))
        with open('utils/statistics/'+f'{message.chat.id}'+'_graph1.png', 'rb') as photo:
            await message.answer_photo(photo)
            photo.close()
        with open('utils/statistics/'+f'{message.chat.id}'+'_graph2.png', 'rb') as photo:
            await message.answer_photo(photo)
            photo.close()
        with open('utils/statistics/'+f'{message.chat.id}'+'_graph3.png', 'rb') as photo:
            await message.answer_photo(photo)
            photo.close()
        if os.path.isfile(f'utils/statistics/{message.chat.id}'+'_graph1.png'):
            os.remove(f'utils/statistics/{message.chat.id}'+'_graph1.png') 
            print("success") 
        else: 
            print("File doesn't exists!")
        if os.path.isfile(f'utils/statistics/{message.chat.id}'+'_graph2.png'):
            os.remove(f'utils/statistics/{message.chat.id}'+'_graph2.png') 
            print("success") 
        else: 
            print("File doesn't exists!")
        if os.path.isfile(f'utils/statistics/{message.chat.id}'+'_graph3.png'):
            os.remove(f'utils/statistics/{message.chat.id}'+'_graph3.png') 
            print("success") 
        else: 
            print("File doesn't exists!")
        circle_diagram(message.chat.id,FEEDBACK.get_all_mood(message.chat.id),answer_mood.get_mood(message.chat.id))
        with open('utils/statistics/'+f'{message.chat.id}'+'_circle.png', 'rb') as photo:
            await message.answer_photo(photo)
            photo.close()
        if os.path.isfile(f'utils/statistics/{message.chat.id}'+'_circle.png'):
            os.remove(f'utils/statistics/{message.chat.id}'+'_circle.png') 
            print("success") 
        else: 
            print("File doesn't exists!")
        await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
        await States_Zagotovka.user_menu.set()
    elif message.text == user_bat[2]:
        
        friends =FuncM.get_friends(message.chat.id)
        msg = ''
        print(friends)
        if friends == ['']:
            await message.answer('Ваш список друзей пуст')
            await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
            await States_Zagotovka.user_menu.set()
        else:
            await States_Zagotovka.game.set()
            await message.answer('Давай проверим твои знания!\nНапиши имя пользоваля с котором хочень соревноватья( Например : \'Example\')')
        
            for i in range(len(friends)):
                print(FuncM.get_username_by_id1(int(friends[i])))
                msg = msg + f'`{FuncM.get_username_by_id1(friends[i])}`'+'\n'
            await message.answer(f'Список Ваших друзей:\n{msg}',parse_mode='MarkDown')

    elif message.text == user_bat[3]:
        await States_Zagotovka.add_friend.set()
        await message.answer('Выберете действие',reply_markup=add_button(friend_button))

    elif message.text == user_bat[4]:
        await States_Zagotovka.check_knowledge.set()
        moduls = []
        print(Test.get_questions())
        for i in Test.get_questions():
            moduls.append(i[2])
        await message.answer(f"Давай проверим твои знания по модулям\nВыбери модуль:",reply_markup=add_button(list(set(moduls))))

    elif message.text == user_bat[5]:
        await States_Zagotovka.feedback.set()
        await message.answer('Оставьте отзыв админимтратору, посоветуйте что добавить или изменить')
        await States_Zagotovka.feedback.set()
    elif message.text == user_bat[6]:
        await States_Zagotovka.aim.set()
        await message.answer('Напишите цель')
    else:
        await message.answer(f"Что-то пошло не так...")
        await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))

@dp.message_handler(state=States_Zagotovka.check_knowledge, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    question=Test.get_random_question(message.text)
    with open('utils/db_api/photos/'+question[1], 'rb') as photo:
        await message.answer_photo(photo, reply_markup=add_button(question[4].split('|')))
        await States_Zagotovka.true_false_answer.set()
        photo.close()

async def send_mood_msg(dp: Dispatcher,x):
    await dp.bot.send_message(int(x), mood.get_question(x)[0])
    state1 = dp.current_state(chat=int(x), user=int(x))
    await state1.set_state(States_Zagotovka.mood_msg)

@dp.message_handler(state=States_Zagotovka.mood_msg, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    answer_mood.post_answer_mood(message.chat.id,message.text)
    await States_Zagotovka.user_menu.set()
    await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))

async def send_feedback(dp: Dispatcher,x):
    moduls = []
        
    for i in Test.get_questions():
        moduls.append(i[2])
    await dp.bot.send_message(int(x), 'По какому модулю сегодня работали?',reply_markup=add_button(list(set(moduls))))
    state1 = dp.current_state(chat=int(x), user=int(x))
    await state1.set_state(States_Zagotovka.feedback_testing)


@dp.message_handler(state=States_Zagotovka.feedback_testing, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    FEEDBACK.post_answer_question0(message.chat.id,message.text)
    moduls = []
        
    for i in Test.get_questions():
        moduls.append(i[2])
    if message.text in list(set(moduls)):
        await message.answer('Насколько Вы удовлетворены материалами модуля ( Ответ 1-10 ):')
        await States_Zagotovka.feedback_testing1.set()

@dp.message_handler(state=States_Zagotovka.feedback_testing1, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    try:
        if int(message.text) in range(1,11): 
            FEEDBACK.post_answer_question1(message.chat.id,message.text)
            await message.answer('Насколько материалы модуля были Вам интересны: ( Ответ 1-10 ):')
            await States_Zagotovka.feedback_testing2.set()
    except:
        await message.answer('Это должно быть чилсло')

@dp.message_handler(state=States_Zagotovka.feedback_testing2, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    try:
        FEEDBACK.post_answer_question2(message.chat.id,message.text)
        await message.answer('Насколько материалы модуля были понятны : ( Ответ 1-10 ):')
        await States_Zagotovka.feedback_testing3.set()
    except:
        await message.answer('Это должно быть чилсло')

@dp.message_handler(state=States_Zagotovka.feedback_testing3, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    try:
        FEEDBACK.post_answer_question3(message.chat.id,message.text)
        await message.answer('Каковы Ваши впечатления о модуле : ( Почему поставили именно такие оценки? Что понравилось, а что нет?):')
        await States_Zagotovka.feedback_testing4.set()
    except:
        await message.answer('Это должно быть чилсло')

@dp.message_handler(state=States_Zagotovka.feedback_testing4, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    FEEDBACK.post_answer_question4(message.chat.id,message.text)
    await message.answer(f'(Данное сообщение должно проходить в конце рабочей недели)\nПосмотрите какой Вы модлодец!\nЕще на одну неделю ближе к цели\nВаша цель : {FuncM.get_aim(message.chat.id)}')
    await States_Zagotovka.user_menu.set()
    print(FEEDBACK.get_question4(message.chat.id))
    print(message.chat.id)
    words = (' ').join(FEEDBACK.get_question4(message.chat.id)).split(' ')
    print(words)
    Cloud(message.chat.id, words)
    photo = open(f'utils/statistics/{message.chat.id}.png', 'rb')
    await message.answer_photo(photo)
    if os.path.isfile(f'utils/statistics/{message.chat.id}.png'):
        os.remove(f'utils/statistics/{message.chat.id}.png') 
        print("success") 
    else: 
        print("File doesn't exists!")
    scheduler.add_job(send_mood_msg, 'date', run_date=datetime.now()+timedelta(0,15), args=(dp,message.chat.id))


    
    await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
    


@dp.message_handler(state=States_Zagotovka.true_false_answer, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text in Test.get_all_answers():
        await message.answer('Правильно, ты большой молодец')
        await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
        await States_Zagotovka.user_menu.set()
        scheduler.add_job(send_feedback, 'date', run_date=datetime.now()+timedelta(0,15), args=(dp,message.chat.id))
    else:
        await message.answer('Ответ неверный!')
        await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
        await States_Zagotovka.user_menu.set()
        scheduler.add_job(send_feedback, 'date', run_date=datetime.now()+timedelta(0,15), args=(dp,message.chat.id))

@dp.message_handler(state=States_Zagotovka.feedback, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    FuncM.post_feedback(message.chat.id,message.text)
    await message.answer('Ваш отзыв обязательно дойдет до админимтратора')
    await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
    await States_Zagotovka.user_menu.set()


@dp.message_handler(state=States_Zagotovka.add_friend, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == friend_button[0]:
        await message.answer('Напишите нам username пользователя ( Например : Example123 )')
        await States_Zagotovka.add_friend1.set()
    elif message.text == friend_button[1]:
        await message.answer('Напишите нам username пользователя ( Например : Example123 )')
        friends =FuncM.get_friends(message.chat.id)
        msg = ''
        print(friends)
        if friends == ['']:
            await message.answer('Ваш список друзей пуст')
            await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
            await States_Zagotovka.user_menu.set()
        else:
            for i in range(len(friends)):
                print(FuncM.get_username_by_id1(int(friends[i])))
                msg = msg + f'`{FuncM.get_username_by_id1(friends[i])}`'+'\n'
            await message.answer(f'Список Ваших друзей:\n{msg}',parse_mode='MarkDown')
        await States_Zagotovka.delite_friend.set()

@dp.message_handler(state=States_Zagotovka.add_friend1, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    
    try:
        FuncM.Friends(message.chat.id,message.text)
        await message.answer('Друг добавлен')
    except:
        await message.answer('Данного пользователя не пользовался ботом, о нем нет данных')
    await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
    await States_Zagotovka.user_menu.set()




@dp.message_handler(state=States_Zagotovka.delite_friend, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    FuncM.delete_friends(message.chat.id,message.text)
    await message.answer('Друг удален')
    await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
    await States_Zagotovka.user_menu.set()

@dp.message_handler(state=States_Zagotovka.reminder_state, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == "Добавить напоминание":
        await States_Zagotovka.week_state.set()
        await message.answer('На какой день недели хотите поставить напоминание',reply_markup=add_button(week))
        await States_Zagotovka.time_state.set()
    if message.text == "Мое расписание":
        days={"mon":"понедельник",
        "tue":"вторник",
        "wed":"среда",
        "thu":"четверг",
        "fri":"пятница",
        "sat":"суббота",
        "sun":"воскресенье"
        }
        msg = ''
        x = PrettyTable()
        x.field_names = ["День недели", "Время"]
        # x.set_style(PLAIN_COLUMNS)
        try:
            for i in range(len(FuncM.Get_info(message.chat.id)[1])):
                msg = msg + f'{days[FuncM.Get_info(message.chat.id)[1][i]]} - '+f'{FuncM.Get_info(message.chat.id)[0][i]}\n'
                x.add_row([days[FuncM.Get_info(message.chat.id)[1][i]],FuncM.Get_info(message.chat.id)[0][i]])
            # await message.answer('Ваше расписание:\n'+msg)
            await message.answer(f'`{x.get_string(title="Ваше расписание")}`',parse_mode='MarkDown')
            await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
            await States_Zagotovka.user_menu.set()
        except:
            
            await message.answer(f"Ваше расписание пустое")
            await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
            await States_Zagotovka.user_menu.set()
    if message.text == 'Удалить напоминаие':
        await message.answer('Здесь выводится расписание напоминаний, но с возможностью удаления данного')
        days={"mon":"понедельник",
        "tue":"вторник",
        "wed":"среда",
        "thu":"четверг",
        "fri":"пятница",
        "sat":"суббота",
        "sun":"воскресенье"
        }
        msg = ''
        try:
            for i in range(len(FuncM.Get_info(message.chat.id)[1])):
                msg = msg + f'{days[FuncM.Get_info(message.chat.id)[1][i]]} - '+f'{FuncM.Get_info(message.chat.id)[0][i]} id: '+f'`{FuncM.Get_info(message.chat.id)[2][i]}`\n'
            await message.answer('Ваше расписание:\n'+msg+'Нажмите на id напоминания которое хотите удалить и отправьте)',parse_mode='MarkDown')
            await States_Zagotovka.delite_reminder.set()
        except:
            await message.answer(f'Ваше расписание пустое')
            await States_Zagotovka.user_menu.set()
            await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))

@dp.message_handler(state=States_Zagotovka.delite_reminder, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    scheduler.remove_job(message.text)
    FuncM.delete_id_reminder(message.chat.id,message.text)
    days={"mon":"понедельник",
        "tue":"вторник",
        "wed":"среда",
        "thu":"четверг",
        "fri":"пятница",
        "sat":"суббота",
        "sun":"воскресенье"
        }
    msg = ''
    try:
        for i in range(len(FuncM.Get_info(message.chat.id)[1])):
            msg = msg + f'{days[FuncM.Get_info(message.chat.id)[1][i]]} - '+f'{FuncM.Get_info(message.chat.id)[0][i]}\n'
        await message.answer('Готово!\nВаше расписание:\n'+msg)
        await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
        await States_Zagotovka.user_menu.set()
    except:
        await message.answer(f'Ваше расписание пустое')
        await States_Zagotovka.user_menu.set()
        await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
        



@dp.message_handler(state=States_Zagotovka.add_friend, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    
    await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
    await States_Zagotovka.user_menu.set()
    
@dp.message_handler(state=States_Zagotovka.game, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    await message.answer(f"Давай пройдем тест на какую-то тему c другом {message.text}\nЯ отправлю подтверждение на принятие вызова, как только он его примет, игра начнется, превый ответиший ВЕРНО на вопрос - побеждает\nВы можете отменить дуэль написав мне `Отмена`",parse_mode='MarkDown')
    msg = await message.answer("Ожидайте")
    msg
    a=0
    await States_Zagotovka.zero.set()
    states = await state.get_state()
    # print(states)
    id_friend = FuncM.get_username_by_id(message.text)
    if id_friend in FuncM.get_friends(message.chat.id):
    
        Dueling.add_players(message.chat.id,id_friend)
        while states == "States_Zagotovka:zero":
            states = await state.get_state()
            time.sleep(0.5)
            a=a+1
            point = '.'
            await msg.edit_text(f'Ожидайте'+f'{point*((a%3)+1)}')
            if a == 1:
                await dp.bot.send_message(id_friend, f'Вас приглашает на интеллектуальную дуэль {message.chat.first_name}',reply_markup=add_button(priglos))
                state1 = dp.current_state(chat=id_friend, user=id_friend)
                await state1.set_state(States_Zagotovka.priglos)
    else:
        await States_Zagotovka.user_menu.set()
        await message.answer('Данного пользователя у Вас нет в списке друзей')
        await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
    

@dp.message_handler(state=States_Zagotovka.zero, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
        await States_Zagotovka.user_menu.set()
        await dp.bot.send_message(1300419285, f"Меню админа:",reply_markup=add_button(admin_bat))
        state1 = dp.current_state(chat=1300419285, user=1300419285)
        await state1.set_state(States_Zagotovka.admin_menu)


@dp.message_handler(state=States_Zagotovka.feedback, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    # FEEDBACK(message.chat.id,message.text)
    await message.answer('Ваш отзыв/предложение отправлен администратору')
    await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
    await States_Zagotovka.user_menu.set()

@dp.message_handler(state=States_Zagotovka.time_state, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text in week:
        FuncM.Update_day_of_week(message.chat.id,message.text)
        await message.answer('На какое время хостите поставить напоминание\n( Например : 16:32 )')
        await States_Zagotovka.time_state1.set()
    
@dp.message_handler(state=States_Zagotovka.time_state1, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if re.fullmatch('^(([0,1][0-9])|(2[0-3])):[0-5][0-9]$', message.text):
        FuncM.Update_time(message.chat.id,message.text,f'{message.chat.id}_'+f'{str(random.randint(1, 10000))}')
        await message.answer('Уведомление установлено')
        await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
        await States_Zagotovka.user_menu.set()
    else:
        await message.answer('Некорректно указано время, попробуйте еще раз')
    

async def update_num_text(message: types.Message, new_value: time):
    await message.edit_text(
        f"Укажите время для напоминания: {new_value}",
        reply_markup=get_keyboard()
    )

user_data = {}




@dp.callback_query_handler(Text(startswith="num_"),state=States_Zagotovka.time_state)
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, '16:00')
    action = callback.data.split("_")[1]

    if action == "+1":
        split_data = user_value.split(':')
        if int(user_value.split(':')[0])+1 == 24:
            time = '00:'+split_data[1]
        else:
            time = str(int(user_value.split(':')[0])+1)+':'+split_data[1]
        user_data[callback.from_user.id] = time
        await update_num_text(callback.message, time)
    elif action == "-1":
        split_data = user_value.split(':')
        if int(user_value.split(':')[0])+1 == 1:
            time = '23:'+split_data[1]
        else:
            time = str(int(user_value.split(':')[0])-1)+':'+split_data[1]
        user_data[callback.from_user.id] = time
        await update_num_text(callback.message, time)
    elif action == "-15":
        split_data = user_value.split(':')
        if int(user_value.split(':')[1])-15 == -15:
            time = split_data[0]+':45'
        elif int(user_value.split(':')[1])-15 == 0:
            time = split_data[0]+':00'
        else:
            time = split_data[0]+':'+str(int(user_value.split(':')[1])-15)
        user_data[callback.from_user.id] = time
        await update_num_text(callback.message, time)
    elif action == "+15":
        split_data = user_value.split(':')
        if int(user_value.split(':')[1])+15 == 60:
            time = split_data[0]+':00'
        else:
            time = split_data[0]+':'+str(int(user_value.split(':')[1])+15)
        user_data[callback.from_user.id] = time
        await update_num_text(callback.message, time)
    elif action == "finish":
        await callback.message.edit_text(f"Итого: {user_value}")
        await States_Zagotovka.user_menu.set()
        await callback.message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))

    await callback.answer()
