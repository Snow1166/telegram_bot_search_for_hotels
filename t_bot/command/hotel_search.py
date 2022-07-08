from config import bot, user_dict
from database.state import StateUser


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def hotel_search(message):
    user_dict[message.chat.id].command = message.text
    bot.set_state(message.from_user.id,
                  StateUser.destination_id,
                  message.chat.id)
    bot.send_message(message.from_user.id,
                     'В каком городе ищем гостиницу? ')