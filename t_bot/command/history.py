from config import bot, user_dict
from loguru import logger

"""Команда /history
После ввода команды пользователю выводится история поиска отелей. Сама история
содержит:
1. Команду, которую вводил пользователь.
2. Дату и время ввода команды.
3. Отели, которые были найдены.
"""
@logger.catch()
@bot.message_handler()
def unknown_command(message):
    bot.send_message(message.chat.id, """
Извините, я вас не понимаю.
Нажмите /help для получения списка команд""")