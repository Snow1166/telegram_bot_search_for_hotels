from config import bot, user_dict
from database.state import StateUser
from database.users import User
from t_bot.keyboard_markup.inline_keyboard import city_markup, photo_choice, hotel_choice


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def command_lowprice(message):
    user_dict[message.chat.id].command = message.text
    bot.set_state(message.from_user.id, StateUser.destinationId, message.chat.id)
    bot.send_message(message.from_user.id, 'В каком городе ищем гостиницу? ')


@bot.message_handler(state=StateUser.destinationId)
def get_search_city(message):
    button = city_markup(message.text)
    bot.set_state(message.from_user.id, StateUser.destinationId, message.chat.id)
    bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=button)



@bot.message_handler(state=StateUser.checkIn)
def get_checkIn(message):
    user_dict[message.chat.id].checkIn = message.text
    bot.set_state(message.from_user.id, StateUser.checkOut, message.chat.id)
    bot.send_message(message.from_user.id, 'Выберите дату отъезда')





@bot.message_handler(state=StateUser.min_high_price)
def get_checkOut(message):
    user_dict[message.chat.id].min_high_price = message.text.split()
    bot.set_state(message.from_user.id, StateUser.distance, message.chat.id)
    bot.send_message(message.from_user.id, 'Укажите максимальное расстояние от центра.')


@bot.message_handler(state=StateUser.distance)
def get_checkOut(message):
    user_dict[message.chat.id].distance = message.text
    bot.set_state(message.from_user.id, StateUser.total_photos, message.chat.id)
    button = photo_choice()
    bot.send_message(message.from_user.id, 'Вы хотите посмотреть фотографии отелей?', reply_markup=button)
