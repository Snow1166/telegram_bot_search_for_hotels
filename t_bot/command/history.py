"""Team history"""
from loguru import logger
from telebot.types import Message

from config import bot
from database.db_func import get_request_db
from t_bot.utilities import func
from t_bot.keyboard_markup.inline_keyboard import after_search


@logger.catch()
@bot.message_handler(commands=['history'])
def send_history(message: Message) -> None:
    """
    Catches the history command
    and sends the user a history of his requests.
    :param message: user's message
    """
    history = get_request_db(message.chat.id)
    answer_button = after_search()
    if history:
        for i_hist in history:
            message_s = f"""
<b>дата запроса:</b>  {i_hist['data'].strftime("%Y.%m.%d <b>время:</b>  %H:%M")}
<b>Команда:</b> {i_hist['command'][1:]}
<b>Запрашиваемый город:</b> {i_hist['city']}
<b>Список найденных отелей:</b>"""
            bot.send_message(message.chat.id, message_s)
            for hotel in i_hist['hotel_list'].values():
                bot.send_message(message.chat.id,
                                 func.format_message_for_user_history(hotel),
                                 disable_web_page_preview=True)
        bot.send_message(message.chat.id, 'Начать новый поиск?',
                         reply_markup=answer_button)
    else:
        bot.send_message(message.chat.id, 'Ваша история запросов пуста', reply_markup=answer_button)


@logger.catch()
@bot.message_handler()
def unknown_command(message: Message) -> None:
    """
    Catches unrecognized messages
    and sends the relevant information to the user.
    :param message: user's message
    """
    sticker = 'CAACAgIAAxkBAAEWAqpi0TgZuLaB1AXOqHLVwkKlGB106QACYhgAAjx6UEnKFDnPOcbwvykE'
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, """
Извините, я вас не понимаю.
Нажмите /help для получения списка команд""")
