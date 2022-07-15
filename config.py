from dotenv import find_dotenv, load_dotenv
from loguru import logger
import telebot
import os
from database.db_models import db, UserRequest
if not find_dotenv():
    logger.error('find_dotenv not found ')
else:
    load_dotenv()

DEBUG = True
DEBUG_save_requests = False

url_properties_list = "https://hotels4.p.rapidapi.com/properties/list"
url_search_locations = "https://hotels4.p.rapidapi.com/locations/v2/search"
url_get_hotel_photos = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
timeout_api_hotels = 3


BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')

RapidAPI_Key = os.getenv('RAPID_API_KEY')
hotels_headers = {
    "X-RapidAPI-Key": RapidAPI_Key,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

logger.add('log.log', level='DEBUG', format="{time} {level} {message}", rotation='00:00', compression='zip',
           serialize=True)

pattern_delete_spans = '<([^<>]*)>'

alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя-"

sticker = 'CAACAgIAAxkBAAEWAqhi0TfnjiiCWkPDOtdwHmizZrHPLgACgBgAAsC2UEmimzNNrlDPPCkE'

user_dict = dict()
db.create_tables([UserRequest])

command_list = """
<b>Команды бота</b>
/lowprice - поиск недорогих отелей
/highprice - отели с высокими ценами
/bestdeal - лучшие предложения
/history - история запросов"""
