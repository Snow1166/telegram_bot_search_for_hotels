from config import bot
from database.user import User
from t_bot.keyboard_markup.button_for_location import city_markup, photo_choice


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def command_lowprice(message):
    User.command = message.text
    bot.set_state(message.from_user.id, User.destinationId, message.chat.id)
    bot.send_message(message.from_user.id, 'В каком городе ищем гостиницу? ')


@bot.message_handler(state=User.destinationId)
def get_search_city(message):
    button = city_markup(message.text)
    bot.set_state(message.from_user.id, User.destinationId, message.chat.id)
    bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=button)


@bot.message_handler(state=User.checkIn)
def get_checkIn(message):
    User.checkIn = message.text
    bot.set_state(message.from_user.id, User.checkOut, message.chat.id)
    bot.send_message(message.from_user.id, 'Выберите дату отъезда')


@bot.message_handler(state=User.checkOut)
def get_checkOut(message):
    User.checkOut = message.text
    if User.command == '/bestdeal':
        bot.set_state(message.from_user.id, User.min_high_price, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите диапазон цен отелей, через пробел')
    else:
        bot.set_state(message.from_user.id, User.photo_hotel, message.chat.id)
        button = photo_choice()
        bot.send_message(message.from_user.id, 'Вы хотите посмотреть фотографии отелей?', reply_markup=button)


@bot.message_handler(state=User.min_high_price)
def get_checkOut(message):
    User.min_high_price = message.text.split()
    bot.set_state(message.from_user.id, User.distance, message.chat.id)
    bot.send_message(message.from_user.id, 'Укажите максимальное расстояние от центра.')


@bot.message_handler(state=User.distance)
def get_checkOut(message):
    User.distance = message.text
    bot.set_state(message.from_user.id, User.photo_hotel, message.chat.id)
    button = photo_choice()
    bot.send_message(message.from_user.id, 'Вы хотите посмотреть фотографии отелей?', reply_markup=button)


@bot.message_handler(state=User.total_photos)
def get_checkOut(message):
    User.distance = message.text
    bot.set_state(message.from_user.id, User.command, message.chat.id)
