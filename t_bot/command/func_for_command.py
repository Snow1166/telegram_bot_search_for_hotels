from t_bot.keyboard_markup.button_for_location import city_markup
from t_bot.t_bot import bot


def get_locations(message):
    button = city_markup(message.text)
    bot.send_message(message.from_user.id, 'Уточните, пожалуйста:',
                     reply_markup=button)


def find_location(message):
    bot.send_message(message.chat.id, 'В каком городе ищем?')
    bot.register_next_step_handler(message, get_locations)
