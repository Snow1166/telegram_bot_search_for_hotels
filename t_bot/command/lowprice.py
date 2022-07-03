from config import bot
from database.user import User
from t_bot.keyboard_markup.button_for_location import city_markup


@bot.message_handler(commands=['lowprice'])
def command_lowprice(message):
    bot.set_state(message.from_user.id, User.destinationId, message.chat.id)
    bot.send_message(message.from_user.id, 'В каком городе ищем гостиницу? ')


@bot.message_handler(state=User.destinationId)
def get_search_city(message):
    bot.set_state(message.from_user.id, User.destinationId, message.chat.id)
    button = city_markup(message.text)
    bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=button)


@bot.message_handler(state=User.checkIn)
def get_checkIn(message):
    bot.set_state(message.from_user.id, User.checkOut, message.chat.id)
    bot.send_message(message.from_user.id, 'Выберите дату отъезда')
    User.checkIn = message.text


@bot.message_handler(state=User.checkOut)
def get_checkOut(message):
    bot.set_state(message.from_user.id, User.checkIn, message.chat.id)
    bot.send_message(message.from_user.id, 'собранная информация для поиска')
    User.checkOut = message.text
    bot.send_message(message.from_user.id, (f'{User.destinationId}, {User.checkIn}, {User.checkOut}'))
