from requests_hotel.locations import get_locations_list
from telebot import types


def photo_choice():
    button_photo_choice = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text='Да', callback_data='photo yes')
    button_2 = types.InlineKeyboardButton(text='Нет', callback_data='photo no')
    return button_photo_choice.add(button_1, button_2)


def total_photo():
    button_total_photo = types.InlineKeyboardMarkup(row_width=5)
    button_1 = types.InlineKeyboardButton(text='1', callback_data='total_photo 1')
    button_2 = types.InlineKeyboardButton(text='2', callback_data='total_photo 2')
    button_3 = types.InlineKeyboardButton(text='3', callback_data='total_photo 3')
    button_4 = types.InlineKeyboardButton(text='4', callback_data='total_photo 4')
    button_5 = types.InlineKeyboardButton(text='5', callback_data='total_photo 5')
    return button_total_photo.add(button_1, button_2, button_3, button_4, button_5)
