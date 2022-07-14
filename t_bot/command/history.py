from config import bot
from loguru import logger
from database.users import User
from database.db_func import get_request_db
from t_bot.utilities import func
"""Команда /history
После ввода команды пользователю выводится история поиска отелей. Сама история
содержит:
1. Команду, которую вводил пользователь.
2. Дату и время ввода команды.
3. Отели, которые были найдены.
"""

@logger.catch()
@bot.message_handler(commands=['history'])
def send_history(message):
    history = get_request_db(message.chat.id)
    for i_hist in history:
        print(i_hist['data'])
        message_s = f"""
<b>Дата запроса:</b> {i_hist['data']}
<b>Команда:</b> {i_hist['command'][1:]}
<b>Запрашиваемый город:</b> {i_hist['city']}
<b>Список найденных отелей:</b>"""
        bot.send_message(message.chat.id, message_s)
        for hotel in i_hist['hotel_list']:
            print(hotel)


@logger.catch()
@bot.message_handler()
def unknown_command(message):
    bot.send_message(message.chat.id, """
Извините, я вас не понимаю.
Нажмите /help для получения списка команд""")