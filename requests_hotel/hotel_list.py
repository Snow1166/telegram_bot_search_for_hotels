import requests
import re
import json
import config


def request_hotels(dest_id, checkIn, checkOut):
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": {dest_id}, "pageNumber": "1", "pageSize": "25", "checkIn": {checkIn},
                   "checkOut": {checkOut}, "adults1": "1", "sortOrder": "PRICE", "locale": "ru-RU", "currency": "RUB"}

    response = requests.get(url, headers=config.hotels_headers, params=querystring)
