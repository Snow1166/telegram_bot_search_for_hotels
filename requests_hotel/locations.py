import requests
import re
import json
import config


def request_location(message):
    """Запрос локаций по названию городу"""
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": {message}, "locale": "ru_RU", "currency": "rub"}
    answer = requests.get(url, headers=config.hotels_headers, params=querystring, timeout=15)
    if answer.status_code == requests.codes.ok:
        locations = json.loads(answer.text)
        return locations


def get_locations_list(message):
    """Парсим json файл поиска города и выдаем чистый словарь с локациями"""
    json_loc = request_location(message)
    locations = dict()
    for item in json_loc['suggestions'][0]['entities']:
        location_name = re.sub(config.CLEAN_NAME, '', item['caption'])
        locations[location_name] = item['destinationId']
    return locations
