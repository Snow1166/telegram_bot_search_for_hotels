from config import bot, command_list
from telebot.types import Message
from loguru import logger


@logger.catch()
@bot.message_handler(commands=['start'])
def command_start(message: Message) -> None:
    """
    Catches the start command,
    sends the user a welcome message and a list of commands.
    :param message: user's message
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
    Catches the help command and sends the user a list of bot commands.
    :param message: user's message
    """
    sticker_help = 'CAACAgIAAxkBAAEWA9li0UwRePc9fF3eBRMIXAb7qIH5TAACwxMAAm3oEEqGY8B94dy6NCkE'
    logger.info(f'User "{message.chat.id}" used command "/help"')
    bot.send_sticker(message.chat.id, sticker_help)
    bot.send_message(message.chat.id, command_list)

