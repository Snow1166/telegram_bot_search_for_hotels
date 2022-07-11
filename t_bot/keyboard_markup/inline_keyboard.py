from requests_hotel.locations import get_locations_list
from database.state import StateUser
from telebot import types
from loguru import logger


@logger.catch()
def city_markup(message, user_id):
    """Создаем и возвращаем кнопки для точного определения города"""
    cities = get_locations_list(message, user_id)
    destinations = types.InlineKeyboardMarkup()
    print(cities)
    if cities:
        logger.info(f'User "{user_id}" creating buttons to accurately select the city of "{message}"')
        for city in cities:
            destinations.add(types.InlineKeyboardButton(text=city,
                                                        callback_data=f'id_loc {cities[city]}'))
        destinations.add(button_cancel())
        return destinations
    elif cities == False: #как бы тут ловить 3 сотояния? словарь, пустой словарь и False?
        button = types.InlineKeyboardButton(text='Сервер не отвечает.'
                                                 'Возврат в главное меню',
                                            callback_data='cancel')
        return destinations.add(button)
    elif len(cities) == 0:
        button = types.InlineKeyboardButton(text='По данному городу ничего не найдено.'
                                                 'Возврат в главное меню',
                                            callback_data='cancel')
        return destinations.add(button)


@logger.catch()
def photo_bool_choice(user_id):
    logger.info(f'User "{user_id}" creating buttons for asking about the need for photos')
    button_photo_choice = types.InlineKeyboardMarkup(row_width=2)
    button_1 = types.InlineKeyboardButton(text='Да', callback_data='bool_photo yes')
    button_2 = types.InlineKeyboardButton(text='Нет', callback_data='bool_photo no')
    button_photo_choice.add(button_1, button_2)
    button_photo_choice.add(button_cancel())
    return button_photo_choice


@logger.catch()
def photo_choice(user_id):
    logger.info(f'User "{user_id}" creating buttons to select the number of photos')
    button_photo_choice = types.InlineKeyboardMarkup(row_width=5)
    button = [(types.InlineKeyboardButton(text=i,
                                          callback_data=f'photo {i}')) for i in range(1, 6)]
    button_photo_choice.add(*button)
    button_photo_choice.add(button_cancel())
    return button_photo_choice


@logger.catch()
def hotel_choice(user_id):
    logger.info(f'User "{user_id}" creating buttons to select the number of hotels')
    button_hotel_choice = types.InlineKeyboardMarkup(row_width=2)
    button = [(types.InlineKeyboardButton(text=i,
                                          callback_data=f'hotel {i}')) for i in [1, 3, 5, 7, 10]]
    button_hotel_choice.add(*button)
    button_hotel_choice.add(button_cancel())
    return button_hotel_choice


def button_cancel():
    button = types.InlineKeyboardButton(text='Возврат в главное меню', callback_data='cancel')
    return button


def button_cancel_ready():
    button = types.InlineKeyboardMarkup()
    button.add(button_cancel())
    return button
