from config import bot, user_dict, command_list
from database.users import User
from loguru import logger


@logger.catch()
@bot.message_handler(commands=['start'])
def command_start(message):
    # bot.send_sticker(message.chat.id, 'CAADAgADsQADWQMDAAEJK1niI56hlhYE')
    user_dict[message.from_user.id] = User()
    logger.info(f'User "{message.chat.id}" create a user_dict')
    logger.info(f'User "{message.chat.id}" used command "/start"')
    welcome = open('images/logo.jpg', 'rb')
    bot.send_photo(message.chat.id, welcome, caption=command_list)


@logger.catch()
@bot.message_handler(commands=['help'])
def command_start(message):
    logger.info(f'User "{message.chat.id}" used command "/help"')
    welcome = open('images/logo.jpg', 'rb')
    bot.send_photo(message.chat.id, welcome, caption=command_list)
