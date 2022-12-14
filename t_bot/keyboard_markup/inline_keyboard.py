"""The module for creating inline keyboards"""
from loguru import logger
from telebot import types
from telebot.types import InlineKeyboardMarkup

from rapid_hotel.api_locations import get_locations_list


@logger.catch()
def city_markup(message: str, user_id) -> InlineKeyboardMarkup | dict:
    """
    Создаем и возвращаем кнопки для точного определения города.
    :param message: название города.
    :param user_id: id пользователя.
    :return: возвращает клавиатуру или словарь
    """
    cities = get_locations_list(message, user_id)
    destinations = types.InlineKeyboardMarkup()
    if cities:
        logger.info(f'''
            User "{user_id}" creating buttons to accurately select the city of "{message}"''')
        for city in cities:
            destinations.add(types.InlineKeyboardButton(text=city,
                                                        callback_data=f'id_loc {cities[city]}'))
        destinations.add(button_cancel())
        return destinations
    return cities


@logger.catch()
def photo_bool_choice(user_id) -> InlineKeyboardMarkup:
    """
    Создает InlineKeyboardMarkup для выбора необходимости фотографий
    :param user_id: id пользователя.
    :return: InlineKeyboardMarkup
    """
    logger.info(f'User "{user_id}" creating buttons for asking about the need for photos')
    button_photo_choice = types.InlineKeyboardMarkup(row_width=2)
    button_1 = types.InlineKeyboardButton(text='Да', callback_data='bool_photo yes')
    button_2 = types.InlineKeyboardButton(text='Нет', callback_data='bool_photo no')
    button_photo_choice.add(button_1, button_2)
    button_photo_choice.add(button_cancel())
    return button_photo_choice


@logger.catch()
def photo_choice(user_id ) -> InlineKeyboardMarkup:
    """
    Создает InlineKeyboardMarkup для выбора количества фотографий
    :param user_id: id пользователя.
    :return: InlineKeyboardMarkup
    """
    logger.info(f'User "{user_id}" creating buttons to select the number of photos')
    button_photo_choice = types.InlineKeyboardMarkup(row_width=5)
    button = [(types.InlineKeyboardButton(text=i,
                                          callback_data=f'photo {i}')) for i in range(1, 6)]
    button_photo_choice.add(*button)
    button_photo_choice.add(button_cancel())
    return button_photo_choice


@logger.catch()
def hotel_choice(user_id) -> InlineKeyboardMarkup:
    """
    Создает InlineKeyboardMarkup для выбора количества отелей
    :param user_id: id пользователя.
    :return: InlineKeyboardMarkup
    """
    logger.info(f'User "{user_id}" creating buttons to select the number of hotels')
    button_hotel_choice = types.InlineKeyboardMarkup(row_width=2)
    button = [(types.InlineKeyboardButton(text=i,
                                          callback_data=f'hotel {i}')) for i in [1, 3, 5, 7, 10]]
    button_hotel_choice.add(*button)
    button_hotel_choice.add(button_cancel())
    return button_hotel_choice


def button_cancel() -> types.InlineKeyboardButton:
    """
    Создаёт кнопку возврата к выбору поиска команд.
    :return: InlineKeyboardMarkup
    """
    button = types.InlineKeyboardButton(text='Вернуться к выбору команд', callback_data='cancel')
    return button


def button_cancel_ready() -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру возврата к выбору поиска команд.
    :return: InlineKeyboardMarkup
    """
    button = types.InlineKeyboardMarkup()
    button.add(button_cancel())
    return button


def after_search() -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру c новым поиском и завершением.
    :return: InlineKeyboardMarkup
    """
    button = types.InlineKeyboardMarkup(row_width=1)
    button_1 = types.InlineKeyboardButton(text='Новый поиск', callback_data='cancel')
    button_2 = types.InlineKeyboardButton(text='Завершить', callback_data='end')
    button.add(button_1, button_2)
    return button
