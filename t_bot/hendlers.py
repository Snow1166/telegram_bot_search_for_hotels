from config import bot, user_dict
from database.state import StateUser
from t_bot.keyboard_markup.inline_keyboard import city_markup, photo_choice


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def command_lowprice(message):
    user_dict[message.chat.id].command = message.text
    bot.set_state(message.from_user.id,
                  StateUser.destination_id,
                  message.chat.id)
    bot.send_message(message.from_user.id,
                     'В каком городе ищем гостиницу? ')


@bot.message_handler(state=StateUser.destination_id)
def get_search_city(message):
    button = city_markup(message.text)
    bot.set_state(message.from_user.id,
                  StateUser.destination_id,
                  message.chat.id)
    bot.send_message(message.from_user.id,
                     'Уточните, пожалуйста:',
                     reply_markup=button)


@bot.message_handler(state=StateUser.min_max_price)
def get_checkout(message):
    price_min, price_max = message.text.split()
    user_dict[message.chat.id].price_min = price_min
    user_dict[message.chat.id].price_max = price_max
    bot.set_state(message.from_user.id,
                  StateUser.distance,
                  message.chat.id)
    bot.send_message(message.from_user.id,
                     'Укажите максимальное расстояние от центра.')


@bot.message_handler(state=StateUser.distance)
def get_checkout(message):
    user_dict[message.chat.id].distance = message.text
    bot.set_state(message.from_user.id,
                  StateUser.total_photos,
                  message.chat.id)
    button = photo_choice()
    bot.send_message(message.from_user.id,
                     'Вы хотите посмотреть фотографии отелей?',
                     reply_markup=button)
