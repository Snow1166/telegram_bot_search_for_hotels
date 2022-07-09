from config import bot, user_dict
from database.state import StateUser
from loguru import logger


@logger.catch()
@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def hotel_search(message):
    logger.info(f'User "{message.chat.id}" used the search command "{message.text}"')
    user_dict[message.chat.id].command = message.text
    bot.set_state(message.from_user.id,
                  StateUser.destination_id,
                  message.chat.id)
    bot.send_message(message.from_user.id,
                     'В каком городе ищем гостиницу? ')