from dotenv import find_dotenv, load_dotenv
from loguru import logger
import telebot
import os
if not find_dotenv():
    print('не найден')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RapidAPI_Key = os.getenv('RapidAPI_Key')
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')
logger.add('error.json', level='DEBUG', format="{time} {level} {message}", rotation='00:00', compression='zip',
           serialize=True)
