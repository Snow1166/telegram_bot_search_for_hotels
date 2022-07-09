from config import bot, user_dict
from t_bot.utilities import func
from database.state import StateUser
from loguru import logger


@logger.catch()
@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def hotel_search(message):
    print(bot.get_state(message.chat.id))
    if func.check_user_state(bot.get_state(message.chat.id)):
        bot.set_state(message.from_user.id,
                      StateUser.destination_id,
                      message.chat.id)
        logger.info(f'User "{message.chat.id}" used the search command "{message.text}"')
        user_dict[message.chat.id].command = message.text
        bot.send_message(message.from_user.id,
                         'В каком городе ищем гостиницу?')
