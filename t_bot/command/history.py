from config import bot
from loguru import logger
from database.users import User
from database.db_func import get_request_db
from t_bot.utilities import func


@logger.catch()
@bot.message_handler(commands=['history'])
def send_history(message):
    history = get_request_db(message.chat.id)
    for i_hist in history:
        message_s = f"""
<b>дата запроса:</b>  {i_hist['data'].strftime("%Y.%m.%d <b>время:</b>  %H:%M")}
<b>Команда:</b> {i_hist['command'][1:]}
<b>Запрашиваемый город:</b> {i_hist['city']}
<b>Список найденных отелей:</b>"""
        bot.send_message(message.chat.id, message_s)
        for hotel in i_hist['hotel_list'].values():
            bot.send_message(message.chat.id, func.format_message_for_user_history(hotel), disable_web_page_preview=True)


@logger.catch()
@bot.message_handler()
def unknown_command(message):
    bot.send_message(message.chat.id, """
Извините, я вас не понимаю.
Нажмите /help для получения списка команд""")