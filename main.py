import telebot
from loguru import logger
import config
from requests_hotel import locations


bot = telebot.TeleBot(config.BOT_TOKEN, parse_mode='html')


def get_locations(message):
    button = locations.city_markup(message.text)
    bot.send_message(message.from_user.id, 'Уточните, пожалуйста:',
                     reply_markup=button)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    welcome = open('images/logo.jpg', 'rb')
    bot.send_photo(message.chat.id, welcome, caption=(
        '<b>Команды бота</b>\n'
        '/lowprice- список недорогих отелей\n'
        '/highprice - отели с высокими ценами\n'
        '/bestdeal - лучшие предложения\n'
        '/history - история запросов\n'
        '/settings - настройки\n'))


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def go_find(message):
    bot.send_message(message.chat.id, 'В каком городе ищем?')
    bot.register_next_step_handler(message, get_locations)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswith('id_loc'):
        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="город выбран",
                              reply_markup=None)

    elif call.data.startswith('checkIn'):
        pass
    elif call.data.startswith('checkOut'):
        pass


bot.polling(none_stop=True)
