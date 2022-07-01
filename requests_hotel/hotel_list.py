import requests
import re
import json
from telebot import types
import config

hotels_headers = {
    "X-RapidAPI-Key": config.RapidAPI_Key,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}


def request_hotels(dest_id, checkIn, checkOut):
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": {dest_id}, "pageNumber": "1", "pageSize": "25", "checkIn": {checkIn},
                   "checkOut": {checkOut}, "adults1": "1", "sortOrder": "PRICE", "locale": "ru-RU", "currency": "RUB"}

    headers = {
        "X-RapidAPI-Key": config.RapidAPI_Key,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

    response = requests.request("GET", url, headers=headers, params=querystring)

