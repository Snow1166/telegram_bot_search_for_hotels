from requests_hotel.locations import get_locations_list
from telebot import types
from loguru import logger


@logger.catch()
def city_markup(message, user_id):
    """Создаем и возвращаем кнопки для точного определения города"""
    cities = get_locations_list(message, user_id)
    destinations = types.InlineKeyboardMarkup()
    logger.info(f'User "{user_id} "creating buttons to accurately select the city of "{message}"')
    for city in cities:
        destinations.add(types.InlineKeyboardButton(text=city,
                                                    callback_data=f'id_loc {cities[city]}'))
    return destinations


@logger.catch()
def photo_choice(user_id):
    logger.info(f'User "{user_id}" creating buttons to select the number of photos')
    button_photo_choice = types.InlineKeyboardMarkup(row_width=5)
    button = [(types.InlineKeyboardButton(text=i,
                                          callback_data=f'photo {i}')) for i in range(1, 6)]
    button_photo_choice.add(*button)
    button_photo_choice.add(types.InlineKeyboardButton(text='Без фото',
                                                       callback_data='photo 0'))
    return button_photo_choice


@logger.catch()
def hotel_choice(user_id):
    logger.info(f'User "{user_id}" creating buttons to select the number of hotels')
    button_hotel_choice = types.InlineKeyboardMarkup(row_width=2)
    button = [(types.InlineKeyboardButton(text=i,
                                          callback_data=f'hotel {i}')) for i in [1, 3, 5, 7, 10]]
    button_hotel_choice.add(*button)

    return button_hotel_choice
