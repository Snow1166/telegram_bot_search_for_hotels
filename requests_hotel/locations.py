import requests
import re
import json
from telebot import types
import config

hotels_headers = {
    "X-RapidAPI-Key": config.RapidAPI_Key,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}


def request_location(message):
    """Запрос локаций по названию городу"""
    # url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    # querystring = {"query": {message}, "locale": "ru_RU", "currency": "rub"}
    # answer = requests.request("GET", url, headers=hotels_headers, params=querystring, timeout=15)
    # if answer.status_code == requests.codes.ok:
    #     locations = json.loads(answer.text)
    #     with open('locations.json', 'w', encoding='utf-8') as file:
    #         json.dump(locations, file, ensure_ascii=False, indent=4)
    #     return locations

    """ Сохранение запроса в json и дальнейшее его использование его вместо запроса для экономии вызовов"""

    with open('locations.json', 'r', encoding='utf-8') as file:
        locations = json.load(file)
    return locations


def get_locations_list(message):
    """Парсим json файл поиска города и выдаем чистый словарь с локациями"""
    json_loc = request_location(message)
    locations = dict()
    for item in json_loc['suggestions'][0]['entities']:
        location_name = re.sub('<([^<>]*)>', '', item['caption'])
        locations[location_name] = item['destinationId']
    return locations


def city_markup(message):
    """Создаем и возвращаем кнопки для точного определения города"""
    cities = get_locations_list(message)
    destinations = types.InlineKeyboardMarkup()
    for city in cities:
        destinations.add(types.InlineKeyboardButton(text=city, callback_data='id_loc' + cities[city]))
    return destinations
