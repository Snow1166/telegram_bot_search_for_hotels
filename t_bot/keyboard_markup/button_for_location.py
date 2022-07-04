from requests_hotel.locations import get_locations_list
from telebot import types


def city_markup(message):
    """Создаем и возвращаем кнопки для точного определения города"""
    cities = get_locations_list(message)
    destinations = types.InlineKeyboardMarkup()
    for city in cities:
        destinations.add(types.InlineKeyboardButton(text=city, callback_data=f'id_loc{cities[city]}'))
    return destinations

