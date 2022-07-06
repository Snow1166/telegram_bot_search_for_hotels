from requests_hotel.locations import get_locations_list
from telebot import types


def city_markup(message):
    """Создаем и возвращаем кнопки для точного определения города"""
    cities = get_locations_list(message)
    destinations = types.InlineKeyboardMarkup()
    for city in cities:
        destinations.add(types.InlineKeyboardButton(text=city, callback_data=f'id_loc {cities[city]}'))
    return destinations

def photo_choice():
    button_photo_choice = types.InlineKeyboardMarkup(row_width=5)
    button_0 = types.InlineKeyboardButton(text='Без фото', callback_data='photo 0')
    button_1 = types.InlineKeyboardButton(text='1', callback_data='photo 1')
    button_2 = types.InlineKeyboardButton(text='2', callback_data='photo 2')
    button_3 = types.InlineKeyboardButton(text='3', callback_data='photo 3')
    button_4 = types.InlineKeyboardButton(text='4', callback_data='photo 4')
    button_5 = types.InlineKeyboardButton(text='5', callback_data='photo 5')
    button_photo_choice.add(button_1, button_2, button_3, button_4, button_5)
    button_photo_choice.add(button_0)
    return button_photo_choice

def hotel_choice():
    button_hotel_choice = types.InlineKeyboardMarkup(row_width=2)
    button_0 = types.InlineKeyboardButton(text='1', callback_data='hotel 1')
    button_1 = types.InlineKeyboardButton(text='3', callback_data='hotel 3')
    button_2 = types.InlineKeyboardButton(text='5', callback_data='hotel 5')
    button_3 = types.InlineKeyboardButton(text='7', callback_data='hotel 7')
    button_4 = types.InlineKeyboardButton(text='10', callback_data='hotel 10')
    button_hotel_choice.add(button_0, button_1, button_2, button_3, button_4)
    return button_hotel_choice