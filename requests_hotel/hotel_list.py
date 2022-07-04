import requests
import re
import json
import config

# querystring = {"destinationId": {dest_id}, "pageNumber": "1", "pageSize": "25", "checkIn": {checkIn},
#                "checkOut": {checkOut}, "adults1": "1", "sortOrder": "PRICE", "locale": "ru-RU", "currency": "RUB"}

def request_hotels(querystring):
    url = "https://hotels4.p.rapidapi.com/properties/list"

    answer = requests.get(url, headers=config.hotels_headers, params=querystring)
    if answer.status_code == requests.codes.ok:
        hotel_list = json.loads(answer.text)
        # with open('hotel_list.json', 'w', encoding='utf-8') as file:
        #     json.dump(hotel_list, file, ensure_ascii=False, indent=4)
        return hotel_list
    #
    # """ Сохранение запроса в json и дальнейшее его использование его вместо запроса для экономии вызовов"""
    #
    # with open('locations.json', 'r', encoding='utf-8') as file:
    #     locations = json.load(file)
    # return hotel_list