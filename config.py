from dotenv import find_dotenv, load_dotenv
from loguru import logger
import telebot
import os
if not find_dotenv():
    print('не найден')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')

RapidAPI_Key = os.getenv('Rapid_API_Key')
hotels_headers = {
    "X-RapidAPI-Key": RapidAPI_Key,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

logger.add('error.json', level='DEBUG', format="{time} {level} {message}", rotation='00:00', compression='zip',
           serialize=True)

CLEAN_NAME = '<([^<>]*)>'

user_dict = dict()