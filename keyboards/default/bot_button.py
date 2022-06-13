from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#Набор кнопок
admin_bat = ['📨 Массовая расcылка информации 📨','📚 Добавить задачу 📚','🔍 Просмотреть отзывы 🔎','❔ Добавить вопросы интеллектуальной рефлексии ❔']
user_bat = ['📅 Добавить напоминание/\nМое расписание/Удалить напоминаие 📅','📈 Статистика 📈','🏆 Соревноваться с друзьями 🏆','👥 Добавить в друзья/Удалить из друзей 👥','🎓 Проверить мои знания 🎓','ℹ️ Оставить отзыв / предложение о боте ℹ️','🎯 Поменять цель 🎯']
week = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
reminder_menu = ['Добавить напоминание','Мое расписание','Удалить напоминаие']
friend_button = ['Добавить в друзья','Удалить из друзей']
yes_no = ['Да','Нет']
priglos = ['✅ Принять ✅','❌ Отклонить ❌']
test_vopros = ["<class 'bool'>","<class 'tuple'>","<class 'str'>"]
category = ['Для соревнований','Для проверки зананий']
mood_bat = ['positive','negative','neutral']

def add_button(mass):
    buttons = ReplyKeyboardMarkup(True,True,True)
    for i in range(len(mass)):
        keyboad = KeyboardButton(mass[i])
        buttons.add(keyboad)
    return buttons