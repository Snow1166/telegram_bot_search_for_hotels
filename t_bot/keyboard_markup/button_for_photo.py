from requests_hotel.locations import get_locations_list
from telebot import types


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
