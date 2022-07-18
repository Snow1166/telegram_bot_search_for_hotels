"""Project configuration"""
import os

from dotenv import find_dotenv, load_dotenv
from loguru import logger
import telebot

from database.db_models import db, UserRequest


if not find_dotenv():
    logger.error('find_dotenv not found ')
else:
    load_dotenv()

DEBUG = False
DEBUG_SAVE_REQUESTS = False

URL_PROPERTIES_LIST = "https://hotels4.p.rapidapi.com/properties/list"
URL_SEARCH_LOCATIONS = "https://hotels4.p.rapidapi.com/locations/v2/search"
URL_GET_HOTEL_PHOTOS = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
TIMEOUT_RAPID = 15


BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')

RapidAPI_Key = os.getenv('RAPID_API_KEY')
hotels_headers = {
    "X-RapidAPI-Key": RapidAPI_Key,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

logger.add('log.log',
           level='DEBUG',
           format="{time} {level} {message}",
           rotation='00:00', compression='zip',
           serialize=True)

PATTERN_DELETE_SPANS = '<([^<>]*)>'

ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя-"

STICKER_WAIT = 'CAACAgIAAxkBAAEWAqhi0TfnjiiCWkPDOtdwHmizZrHPLgACgBgAAsC2UEmimzNNrlDPPCkE'

db.create_tables([UserRequest])

COMMAND_LIST = """
<b>Команды бота</b>
/lowprice - поиск недорогих отелей
/highprice - отели с высокими ценами
/bestdeal - лучшие предложения
/history - история запросов
/help - помощь по командам бота"""
