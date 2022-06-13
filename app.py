import asyncio
from loader import scheduler
from aiogram import Bot, executor
from aiogram import Dispatcher
from loader import dp
import middlewares, filters, handlers
from utils.db_api.DB_functions import FuncM
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

#В данном файле прописан код запуска бота
async def send_msg_by_remember(dp: Dispatcher,x):
    await dp.bot.send_message(int(x), 'Напоминание')

async def start_shedule(dp):
    for x in FuncM.GET_ID():
        for i in range(len(FuncM.Get_info(x)[1])):
            try:
                scheduler.add_job(send_msg_by_remember,\
                'cron', day_of_week=FuncM.Get_info(x)[1][i],\
                hour=int(FuncM.Get_info(x)[0][i].split(':')[0]),\
                minute=int(FuncM.Get_info(x)[0][i].split(':')[1]),\
                id=FuncM.Get_info(x)[2][i],args=(dp,x))
            except:
                pass

async def start_remember(dp):
    scheduler.add_job(start_shedule,'interval',seconds=15,args=(dp,))

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    asyncio.create_task(start_remember(dp))

    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await Bot.session.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
