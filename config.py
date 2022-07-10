from dotenv import find_dotenv, load_dotenv
from loguru import logger
import telebot
import os

if not find_dotenv():
    print('не найден')
else:
    load_dotenv()

url_properties_list = "https://hotels4.p.rapidapi.com/properties/list"
url_search_locations = "https://hotels4.p.rapidapi.com/locations/v2/search"
url_get_hotel_photos = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')

RapidAPI_Key = os.getenv('Rapid_API_Key')
hotels_headers = {
    "X-RapidAPI-Key": RapidAPI_Key,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

logger.add('log.log', level='DEBUG', format="{time} {level} {message}", rotation='00:00', compression='zip',
           serialize=True)

delete_spans = '<([^<>]*)>'
alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
            "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я", "-"]
user_dict = dict()

command_list = """
<b>Команды бота</b>
/lowprice- список недорогих отелей
/highprice - отели с высокими ценами
/bestdeal - лучшие предложения
/history - история запросов"""
