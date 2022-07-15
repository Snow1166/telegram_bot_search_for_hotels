from config import bot, command_list
from telebot.types import Message
from loguru import logger


@logger.catch()
@bot.message_handler(commands=['start'])
def command_start(message: Message) -> None:
    """
    Отлавливает команду start,
    отправляет пользователю приветственное сообщение и список команд.
    :param message: сообщение пользователя
    """
    sticker_hello = 'CAACAgIAAxkBAAEWA7hi0UsBZWQDmcBFYA25gZnWohcWbQAChxUAAj0PUEnem2b91sejvykE'
    logger.info(f'User "{message.chat.id}" used command "/start"')
    bot.send_sticker(message.chat.id, sticker_hello)
    bot.send_message(message.chat.id, """
Привет, я бот по поиску отелей
Выбери необходимую команду.  """)
    bot.send_message(message.chat.id, command_list)


@logger.catch()
@bot.message_handler(commands=['help'])
def command_start(message: Message) -> None:
    """
    Отлавливает команду help и отправляет пользователю список команд бота.
    :param message: сообщение пользователя
    """
    sticker_help = 'CAACAgIAAxkBAAEWA9li0UwRePc9fF3eBRMIXAb7qIH5TAACwxMAAm3oEEqGY8B94dy6NCkE'
    logger.info(f'User "{message.chat.id}" used command "/help"')
    bot.send_sticker(message.chat.id, sticker_help)
    bot.send_message(message.chat.id, command_list)

