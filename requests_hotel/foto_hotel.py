import requests
import re
import json
from telebot import types
import config

hotels_headers = {
    "X-RapidAPI-Key": config.RapidAPI_Key,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}