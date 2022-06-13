from tkinter.messagebox import QUESTION
from requests import delete
import sqlalchemy as db
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey,  distinct
import random
from utils.db_api.NLP_model import *
engine = db.create_engine(f'sqlite:///utils/db_api/DB.sqlite')
connection = engine.connect()
metadata = db.MetaData()

#Таблица Макса
Maks = db.Table('Maks', metadata,
                 autoload=True, autoload_with=engine)
#Таблица Коли
Kolya = db.Table('Kolya', metadata,
                 autoload=True, autoload_with=engine)
#Таблица соревнований
Competition = db.Table('Competition', metadata,
                 autoload=True, autoload_with=engine)
#ТАблица проверки знаний
Testing = db.Table('Testing', metadata,
                 autoload=True, autoload_with=engine)
#Таблица рассылки
Admin = db.Table('Admin', metadata,
                 autoload=True, autoload_with=engine)
#Таблица дуэли
Duel = db.Table('Duel', metadata, autoload=True, autoload_with=engine)
#Таблица обратной связи
Feedback = db.Table('Feedback', metadata,
                 autoload=True, autoload_with=engine)
#ТАблица вопросов в зависимости от наятроения
Mood = db.Table('Mood', metadata,
                 autoload=True, autoload_with=engine)
#Таблица вечерних ответов
Answer_mood=db.Table('Answer_mood', metadata,
                 autoload=True, autoload_with=engine)



#
class FuncM():
#Пример записи данных id и username в таблицу макса
    def POST(id1,username1):
        a=db.select([Maks.columns.id])
        list_id=[]
        for i in connection.execute(a).fetchall():
            list_id.append(i[0])
        if str(id1) in list_id:
            pass
        else:
            query = db.insert(Maks).values(id=id1,Username = username1,
                                       Aim='',Friends_id='',Day_for_reminder='',Time_for_reminder='',id_reminder='',feedback='' )
            ResultProxy = connection.execute(query)

#Пример чтения данных username по id из таблицы макса 
    def GET(id):
        a = db.select([Maks.columns.Username]).where(
        Maks.columns.id == id)
        list_username=[]
        for row in connection.execute(a).fetchall():
            list_username.append(row[0])
        return list_username

    def GET_ID():
        a = db.select([Maks.columns.id])
        list_id=[]
        for row in connection.execute(a).fetchall():
            list_id.append(row[0])
        return list_id

#Пример обновления данных в таблице макса
    def UPDATE(id,username):
        query = db.update(Maks).values(
        Username=username)
        query = query.where(Maks.columns.id == id)
        ResultProxy = connection.execute(query)
#Добваление дня напоминания
    def Update_day_of_week(id1,day):
        days={"понедельник":"mon",
        "вторник":"tue",
        "среда":"wed",
        "четверг":"thu",
        "пятница":"fri",
        "суббота":"sat",
        "воскресенье":"sun"
        }
        list_days=[]
        a=db.select([Maks.columns.Day_for_reminder]).where(
        Maks.columns.id ==id1)

        for row in connection.execute(a).fetchall():
            list_days.append(row[0])
        # print(list_days)
        if list_days[0]=='':
            query=db.update(Maks).values(
                Day_for_reminder=days[day.lower()]
            )
        else:
            query=db.update(Maks).values(
                Day_for_reminder=list_days[0]+','+days[day.lower()]
            )
        query=query.where(Maks.columns.id == id1)
        ResultProxy = connection.execute(query)
#Добавление времени и айди напоминаний
    def Update_time(id1,time,id_rim):
        list_time=''
        list_id_rim=''
        a=db.select([Maks.columns.Time_for_reminder]).where(
        Maks.columns.id ==id1)
        b=db.select([Maks.columns.id_reminder]).where(
        Maks.columns.id ==id1)

        for row in connection.execute(a).fetchall():
            list_time=row[0]

        for row in connection.execute(b).fetchall():
            list_id_rim=row[0]

        if (list_time=='')and(list_id_rim==''):
            query=db.update(Maks).values(
                Time_for_reminder = time,
                id_reminder = id_rim
            )
        else:
            query=db.update(Maks).values(
                Time_for_reminder = list_time+','+time,
                id_reminder = list_id_rim+','+id_rim
            )

        query=query.where(Maks.columns.id == id1)
        ResultProxy = connection.execute(query)

#Получить количество айди напоминаний 
    def Get_kol_id(id1):
        a = db.select([Maks.columns.id_reminder]).where(
        Maks.columns.id == id1)
        list_ids_reminder=[]
        try:
            for row in connection.execute(a).fetchall():
                list_ids_reminder=row[0].split(',')
            return len(list_ids_reminder)
        except:
            return 0

# Получение инфы по колонкам 
    def Get_info(id1):
        a = db.select([Maks.columns.Day_for_reminder, Maks.columns.Time_for_reminder, Maks.columns.id_reminder]).where(
        Maks.columns.id == id1)
        list_days=[]
        list_time=[]
        list_id=[]
        list_all = []
        for row in connection.execute(a).fetchone():
            list_all.append(row)
    
        list_days=list_all[0].split(',')
        list_time=list_all[1].split(',')
        list_id=list_all[2].split(',')
        return [list_time,list_days,list_id]

#Добавление друзей
    def Friends(id1,username):
        list_id=[]
        list_fr=[]
        #айди потенциального друга
        a=db.select([Maks.columns.id]).where(
        Maks.columns.Username==username)
        #список друзей
        b=db.select([Maks.columns.Friends_id]).where(
        Maks.columns.id ==id1)
        for row in connection.execute(a).fetchall():
            list_id.append(row[0])
        for row in connection.execute(b).fetchall():
            list_fr.append(row[0])
        if (list_fr[0]==''):
            query=db.update(Maks).values(
                Friends_id = list_id[0]
            )
        else:
            query=db.update(Maks).values(
                Friends_id = list_fr[0]+','+list_id[0]
            )

        query=query.where(Maks.columns.id == id1)
        ResultProxy = connection.execute(query)

#Удаление айди напоминаний
    def delete_id_reminder(id1,id_rem):
        list_id=[]
        list_time=[]
        list_day=[]
        a=db.select([Maks.columns.id_reminder]).where(
        Maks.columns.id==id1)
        b=db.select([Maks.columns.Day_for_reminder]).where(
        Maks.columns.id==id1)
        c=db.select([Maks.columns.Time_for_reminder]).where(
        Maks.columns.id==id1)
        for row in connection.execute(a).fetchone():
            list_id=row.split(',')
        for row in connection.execute(b).fetchone():
            list_day=row.split(',')
        for row in connection.execute(c).fetchone():
            list_time=row.split(',') 
        index = list_id.index(id_rem)   
        list_id.pop(index)
        list_time.pop(index)
        list_day.pop(index)
        str_id_rem=','.join(list_id)
        str_time=','.join(list_time)
        str_day=','.join(list_day)
        
        query=db.update(Maks).values(
                id_reminder = str_id_rem,
                Day_for_reminder = str_day,
                Time_for_reminder = str_time
            )
        query=query.where(Maks.columns.id == id1)
        ResultProxy = connection.execute(query)

#Удаление друзей
    def delete_friends(id1,username):
        list_id=[]
        a=db.select([Maks.columns.id]).where(
        Maks.columns.Username==username)
        for row in connection.execute(a).fetchall():
            list_id.append(row[0])
        list_id_fr=[]
        b=db.select([Maks.columns.Friends_id]).where(
        Maks.columns.id==id1)
        for row in connection.execute(b).fetchall():
            list_id_fr=row[0].split(',')
        list_id_fr.remove(list_id[0])
        str_id_fr=','.join(list_id_fr)
        query=db.update(Maks).values(
                Friends_id = str_id_fr
            )
        query=query.where(Maks.columns.id == id1)
        ResultProxy = connection.execute(query)
#Обновление цели
    def update_aim(id1,aim):
        query=db.update(Maks).values(
                    Aim = aim
                )
        query=query.where(Maks.columns.id == id1)
        ResultProxy = connection.execute(query)
#Добавление отзыва
    def post_feedback(id1,text):
        list_feedback=[]
        a=db.select([Maks.columns.feedback]).where(
        Maks.columns.id ==id1)

        for row in connection.execute(a).fetchall():
            list_feedback.append(row[0])
        # print(list_days)
        try:
            query=db.update(Maks).values(
                feedback=list_feedback[0]+'&'+text
            )
        except:
            query=db.update(Maks).values(
                feedback=text
            )
        
        query=query.where(Maks.columns.id == id1)
        ResultProxy = connection.execute(query)
#Запрос друзей
    def get_friends(id1):
        list_id=[]
        a=db.select([Maks.columns.Friends_id]).where(
        Maks.columns.id==id1)
        for row in connection.execute(a).fetchall():
            list_id=row[0].split(',')
        return list_id
#Запрос имени по id
    def get_username_by_id(username):
        str_id=''
        a=db.select([Maks.columns.id]).where(
        Maks.columns.Username==username)
        for row in connection.execute(a).fetchall():
            str_id=row[0]
        return str_id
    def get_username_by_id1(id1):
        str_id=''
        a=db.select([Maks.columns.Username]).where(
        Maks.columns.id==id1)
        for row in connection.execute(a).fetchall():
            str_id=row[0]
        return str_id
    def get_aim(id1):
        str_id=''
        a=db.select([Maks.columns.Aim]).where(
        Maks.columns.id==id1)
        for row in connection.execute(a).fetchall():
            str_id=row[0]
        return str_id
    def get_feedback(id1):
        a = db.select(Maks.columns.feedback).where(Maks.columns.id == id1)
        list_feedback=[]
        for row in connection.execute(a).fetchall():
            list_feedback = row[0].split('&')
        return list_feedback
#Таблица для соревнований
class Competitions():

#Добваление вопроса для соревнования
    def post_question(id1,question):
        query = db.insert(Competition).values(id=id1, Question=question,
                                    Answer='', Words='', Weight='')
        ResultProxy = connection.execute(query)

#Добавление правильного ответа на вопрос
    def post_answer(answer):
        query = db.update(Competition).values(Answer=answer)
        query = query.where(Competition.columns.Answer == '')
        ResultProxy = connection.execute(query)

#Добавление прочих вариантов ответов 
    def post_words(text):
        query = db.update(Competition).values(Words=text)
        query = query.where(Competition.columns.Words == '')
        ResultProxy = connection.execute(query)

#Добавление веса ответа
    def post_weight(weight):
        query = db.update(Competition).values(Weight=weight)
        query = query.where(Competition.columns.Weight == '')
        ResultProxy = connection.execute(query)

#Запрос на все имеющиеся вопросы
    def get_questions():
        list_all=[]
        a = db.select(Competition)
        for row in connection.execute(a).fetchall():
            list_all.append(list(row))
        return list_all #Возвращает список списков со строчками таблицы(пример:[['12', 'Кто я?', 'Сергей', 'человек, животное', 10], ['12', 'Кто я?', 'Сергей', 'человек, животное', 10]])

#Таблица для тестирования
class Test():

#Добавление вопроса
    def post_test_question(id1,question):
        query = db.insert(Testing).values(id=id1, Question=question, Modul='',
                                    Answer='', Words='', Weight='')
        ResultProxy = connection.execute(query)

#Добавление модуля вопроса
    def post_modul(modul):
        query = db.update(Testing).values(Modul=modul)
        query = query.where(Testing.columns.Modul == '')
        ResultProxy = connection.execute(query)

#Добваление ответа на вопрос
    def post_test_answer(answer):
        query = db.update(Testing).values(Answer=answer)
        query = query.where(Testing.columns.Answer == '')
        ResultProxy = connection.execute(query)

#Добавление прочих ответов на вопрос
    def post_test_words(text):
        query = db.update(Testing).values(Words=text)
        query = query.where(Testing.columns.Words == '')
        ResultProxy = connection.execute(query)

#Добваление веса ответа на вопрос
    def post_test_weight(weight):
        query = db.update(Testing).values(Weight=weight)
        query = query.where(Testing.columns.Weight == '')
        ResultProxy = connection.execute(query)

#Достать случайный вопрос по теме
    def  get_random_question(modul):
        list_q=[]
        a=db.select(Testing).where(
        Testing.columns.Modul==modul)
        for row in connection.execute(a).fetchall():
            list_q.append(list(row))
        return list_q[random.randint(0,len(list_q)-1)]

#Получить всё
    def get_questions():
        list_all=[]
        a = db.select(Testing)
        for row in connection.execute(a).fetchall():
            list_all.append(list(row))
        return list_all
#Извлечение всех правильных ответов
    def get_all_answers():
        a = db.select(Testing.columns.Answer)
        list_all=[]
        for row in connection.execute(a).fetchall():
            list_all.append(list(row)[0])
        return list_all


class mailing_list():
#Добавление текста 
    def post_text(text):
        query = db.insert(Admin).values(image=text, text='')
        ResultProxy = connection.execute(query)
#Добавление фото  
    def post_image(img):
        query = db.update(Admin).values(text=img)
        query = query.where(Admin.columns.text == '')
        ResultProxy = connection.execute(query)
#Очистка таблицы
    def clear_table():
        query = db.delete(
        Admin)
        results = connection.execute(query)
#Получить все значения таблицы
    def get_all():
        list_all=[]
        a = db.select(Admin)
        for row in connection.execute(a).fetchall():
            list_all.append(list(row))
        return list_all[0]

class FEEDBACK():
#Заносим модуль вопроса
    def post_answer_question0(id1,modul):
        list_a=[]
        a=db.select([Feedback.columns.Modul]).where(
        Feedback.columns.id ==id1)
        for row in connection.execute(a).fetchall():
            list_a.append(row[0])
        if len(list_a)==0:
            query = db.insert(Feedback).values(id=id1,Modul=modul, Question1='null', Question2='null', Question3='null', Boad_question='', mood='')
        else:
            query = db.update(Feedback).values(Modul=list_a[0]+'|'+modul)
            query = query.where(Feedback.columns.id == id1)
        ResultProxy = connection.execute(query)

#Заносим ответ на первый вопрос
    def post_answer_question1(id1,ans):
        list_a=[]
        a=db.select([Feedback.columns.Question1]).where(
        Feedback.columns.id ==id1)
        for row in connection.execute(a).fetchall():
            list_a.append(row[0])
        if list_a[0]=='null':
            query = db.update(Feedback).values(Question1=ans)
            query = query.where(Feedback.columns.Question2 == 'null')
        else:
            query = db.update(Feedback).values(Question1=str(list_a[0])+'|'+ans)
            query = query.where(Feedback.columns.id == id1)
        ResultProxy = connection.execute(query)
#Заносим ответ на второй вопрос
    def post_answer_question2(id1,ans):
        list_a=[]
        a=db.select([Feedback.columns.Question2]).where(
        Feedback.columns.id ==id1)
        for row in connection.execute(a).fetchall():
            list_a.append(row[0])
        if list_a[0]=='null':
            query = db.update(Feedback).values(Question2=ans)
            query = query.where(Feedback.columns.Question2 == 'null')
        else:
            query = db.update(Feedback).values(Question2=str(list_a[0])+'|'+ans)
            query = query.where(Feedback.columns.id == id1)
        ResultProxy = connection.execute(query)
#Заносим ответ на третий вопрос
    def post_answer_question3(id1,ans):
        list_a=[]
        a=db.select([Feedback.columns.Question3]).where(
        Feedback.columns.id ==id1)
        for row in connection.execute(a).fetchall():
            list_a.append(row[0])
        if list_a[0]=='null':
            query = db.update(Feedback).values(Question3=ans)
            query = query.where(Feedback.columns.Question3 == 'null')
        else:
            query = db.update(Feedback).values(Question3=str(list_a[0])+'|'+ans)
            query = query.where(Feedback.columns.id == id1)
        ResultProxy = connection.execute(query)
#Развёрнутый ответ
    def post_answer_question4(id1,ans):
        list_a=''
        a=db.select([Feedback.columns.Boad_question]).where(
        Feedback.columns.id ==id1)
        for row in connection.execute(a).fetchall():
            list_a=row[0]
        if list_a=='':
            query = db.update(Feedback).values(Boad_question=ans)
            query = query.where(Feedback.columns.Boad_question == '')
        else:
            query = db.update(Feedback).values(Boad_question=list_a+'|'+ans)
            query = query.where(Feedback.columns.id == id1)
        ResultProxy = connection.execute(query)

        list_b=''
        b=db.select([Feedback.columns.mood]).where(
        Feedback.columns.id ==id1)
        for row in connection.execute(b).fetchall():
            list_b=row[0]
        an=func(ans)
        if list_b=='':
            query = db.update(Feedback).values(mood=an)
            query = query.where(Feedback.columns.mood == '')
        else:
            query = db.update(Feedback).values(mood=list_b+'|'+an)
            query = query.where(Feedback.columns.id == id1)
        ResultProxy = connection.execute(query)

#Получить ответы фидбэка
    def get_question4(id1):
        a = db.select(Feedback.columns.Boad_question).where(Feedback.columns.id == id1)
        list_mood=[]
        for row in connection.execute(a).fetchall():
            list_mood = row[0].split('|')
        return list_mood


#Функция для персональной статистики(Для Коли)
    def get_all_answers(id1):
        answers_list=[]
        a = db.select([Feedback.columns.Question1,Feedback.columns.Question2,Feedback.columns.Question3]).where(Feedback.columns.id == id1)
        for row in connection.execute(a).fetchall():
            for i in list(row):
                answers_list.append(list(map(int, i.split('|'))))
        return answers_list
#Функция для персональной статистики настроения(Для Коли)
    def get_all_mood(id1):
        answers_list=[]
        a = db.select(Feedback.columns.mood).where(Feedback.columns.id == id1)
        for row in connection.execute(a).fetchall():
            for i in list(row):
                answers_list=row[0].split('|')
        return answers_list
    def get_feedback(id1):
        a = db.select(Feedback.columns.feedback).where(Feedback.columns.id == id1)
        list_mood=[]
        for row in connection.execute(a).fetchall():
            list_mood = row[0].split('&')
        return list_mood

class Dueling():

    def add_players(id11,id12):
        query = db.insert(Duel).values(id1=id11, id2=id12)
        ResultProxy = connection.execute(query)

    def get_id(id):
        list_id=''
        a=db.select([Duel.columns.id2]).where(Duel.columns.id1==id)
        for row in connection.execute(a).fetchall():
            list_id=row[0]
        if list_id=='':
            a=db.select([Duel.columns.id1]).where(Duel.columns.id2==id)
            for row in connection.execute(a).fetchall():
                list_id=row[0]
        return list_id
        
    def get_ids(id):
        list_id=[]
        a=db.select([Duel.columns.id1,Duel.columns.id2]).where(Duel.columns.id1==id)
        for row in connection.execute(a).fetchall():
            list_id=list(row)
        if len(list_id)==0:
            a=db.select([Duel.columns.id1,Duel.columns.id2]).where(Duel.columns.id2==id)
            for row in connection.execute(a).fetchall():
                list_id=list(row)
        return list_id

    def delete(id):
        try:
            query = db.delete(Duel)
            query = query.where(Duel.columns.id1 == id)
        except:
            query = db.delete(Duel)
            query = query.where(Duel.columns.id2 == id)
        results = connection.execute(query)

class mood():
#Извлечение рандомного вопроса по настроению
    def get_question(id1):
        mood_list=[]
        b=db.select([Feedback.columns.mood]).where(
        Feedback.columns.id ==id1)
        for row in connection.execute(b).fetchall():
            mood_list=row[0].split('|')
        list_q=[]
        a=db.select([Mood.columns.Question]).where(
        Mood.columns.Mood==mood_list[len(mood_list)-1])
        for row in connection.execute(a).fetchall():
            list_q.append(list(row))
        return list_q[random.randint(0,len(list_q)-1)]
#Добавление вопроса по настроению
    def post_question_mood(mood):
        query = db.insert(Mood).values(Mood=mood, Question='')
        ResultProxy = connection.execute(query)
    def post_question(question):
        query = db.update(Mood).values(Question=question)
        query = query.where(Mood.columns.Question == '')
        ResultProxy = connection.execute(query)
        print('Вопрос добавлен')


class answer_mood():
#ЗАпись ответа на вопрос и определение настроения
    def post_answer_mood(id1,ans):
        list_a=[]
        a=db.select([Answer_mood.columns.Answer]).where(
        Answer_mood.columns.id ==id1)
        for row in connection.execute(a).fetchall():
            list_a.append(row[0])
        if len(list_a)==0:
            query = db.insert(Answer_mood).values(id=id1,Answer=ans,mood='')
        else:
            query = db.update(Answer_mood).values(Answer=list_a[0]+'|'+ans)
            query = query.where(Answer_mood.columns.id == id1)
        ResultProxy = connection.execute(query)

        list_b=''
        b=db.select([Answer_mood.columns.mood]).where(
        Answer_mood.columns.id ==id1)
        for row in connection.execute(b).fetchall():
            list_b=row[0]
        an=func(ans)
        if list_b=='':
            query = db.update(Answer_mood).values(mood=an)
            query = query.where(Answer_mood.columns.mood == '')
        else:
            query = db.update(Answer_mood).values(mood=list_b+'|'+an)
            query = query.where(Answer_mood.columns.id == id1)
        ResultProxy = connection.execute(query)

#Функция для персональной статистики настроения(Для Коли)
    def get_mood(id1):
        answers_list=[]
        a = db.select(Answer_mood.columns.mood).where(Answer_mood.columns.id == id1)
        for row in connection.execute(a).fetchall():
            for i in list(row):
                answers_list=row[0].split('|')
        return answers_list


