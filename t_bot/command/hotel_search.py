from config import bot
from database.users import User
from t_bot.keyboard_markup.inline_keyboard import button_cancel_ready
from database.state import StateUser
from loguru import logger


@logger.catch()
@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def hotel_search(message):
    user = User.get_user(message.chat.id)
    bot.set_state(message.from_user.id,
                  StateUser.destination_id,
                  message.chat.id)
    logger.info(f'User "{message.chat.id}" used the search command "{message.text}"')
    user.command = message.text
    user.last_message_bot = bot.send_message(message.from_user.id,
                                             'В каком городе ищем гостиницу?',
                                             reply_markup=button_cancel_ready())
