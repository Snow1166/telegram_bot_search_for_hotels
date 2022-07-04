from requests_hotel.locations import get_locations_list
from telebot import types


def city_markup(message):
    """Создаем и возвращаем кнопки для точного определения города"""
    cities = get_locations_list(message)
    destinations = types.InlineKeyboardMarkup()
    for city in cities:
        destinations.add(types.InlineKeyboardButton(text=city, callback_data=f'id_loc{cities[city]}'))
    return destinations


def photo_choice():
    button_photo_choice = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text='Да', callback_data='photo yes')
    button_2 = types.InlineKeyboardButton(text='Нет', callback_data='photo no')
    return button_photo_choice.add(button_1, button_2)
