"""Hotel search team"""
import json

from loguru import logger
from telebot import types
from telebot.types import Message

from config import bot
from t_bot.utilities import func
from t_bot.keyboard_markup.inline_keyboard import button_cancel_ready
from t_bot.keyboard_markup.inline_keyboard import after_search
from rapid_hotel.api_hotel_list import api_get_hotels_list
from rapid_hotel.api_photo_hotel import add_photo
from database.state import StateUser
from database.users import User
from database.db_func import add_request_db


@logger.catch()
@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def hotel_search(message: Message) -> None:
    """
    Catches the search commands 'lowprice', 'highprice', 'best deal',
    requests the desired city from the user,
    changes the user's state to destination_id
    :param message: user's message with the name of the city
    :return:
    """
    user = User.get_user(message.chat.id)
    bot.set_state(message.from_user.id,
                  StateUser.destination_id,
                  message.chat.id)
    logger.info(f'User "{message.chat.id}" used the search command "{message.text}"')
    user.command = message.text
    user.last_message_bot = bot.send_message(message.from_user.id,
                                             'В каком городе ищем гостиницу?',
                                             reply_markup=button_cancel_ready())


@logger.catch()
def get_final_hotel_list(querystring: dict,
                         total_hotels: int,
                         total_photo: int,
                         total_day: int,
                         user_id: str) -> dict:
    """
    Calls a function with a request from the dictionary api with hotels,
generates a final list of hotels for the user and adds photos.
    :param querystring: query string
    :param total_hotels: number of hotels
    :param total_photo: number of photos
    :param total_day: number of days
    :param user_id: user id
    """
    hotel_list = api_get_hotels_list(querystring, user_id)
    ready_list_hotels = {}
    logger.info(f'User "{user_id}" creating a final list of hotels')
    if hotel_list:
        for hotel in hotel_list.values():
            total_hotels -= 1
            id_hotel = hotel['id']
            ready_list_hotels[id_hotel] = func.get_name(hotel)
            ready_list_hotels[id_hotel].update(func.get_address(hotel))
            ready_list_hotels[id_hotel].update(func.get_star_rating(hotel))
            ready_list_hotels[id_hotel].update(func.get_unformatted_rating(hotel))
            ready_list_hotels[id_hotel].update(func.get_landmarks(hotel))
            ready_list_hotels[id_hotel].update(func.get_price(hotel))
            ready_list_hotels[id_hotel].update(func.get_total_price(hotel, total_day))
            ready_list_hotels[id_hotel].update(func.get_site(hotel))
            if total_hotels == 0:
                break
        if total_photo > 0:
            logger.info(f'User "{user_id}" adding photos to the final list of hotels')
            ready_list_hotels = add_photo(ready_list_hotels, total_photo, user_id)
        return ready_list_hotels
    return hotel_list


@logger.catch()
def send_hotels_list_for_user(user_id) -> None:
    """
    Generates a query string,
    calls functions to generate a list of hotels
    and sends them to the chat to the user.
    :rtype: object
    :param user_id: str
    """
    user = User.get_user(user_id)
    querystring = user.get_querystring()
    total_photo = user.get_total_photo()
    total_hotels = user.get_total_hotels()
    total_day = user.total_day
    hotel_list = get_final_hotel_list(querystring, total_hotels, total_photo, total_day, user_id)
    answer_button = after_search()
    bot.delete_message(user_id, user.last_message_bot.message_id)
    if hotel_list:
        logger.info(f'User "{user_id}" Adding a list of hotels to the database')
        add_request_db(user_id, user.command, user.city_search, json.dumps(hotel_list))
        logger.info(f'User "{user_id}" sending a list of hotels to the user')
        for hotel in hotel_list.values():
            bot.send_message(user_id, func.format_message_for_user(hotel, total_day),
                             disable_web_page_preview=True)
            if total_photo > 0:
                if hotel['photo']:
                    media_group = [types.InputMediaPhoto(media=url) for url in hotel['photo']]
                    bot.send_media_group(user_id, media_group)
                else:
                    bot.send_message(user_id, 'Фотографии не найдены.')
        bot.send_message(user_id, 'Начать новый поиск?',
                         reply_markup=answer_button)
    else:
        if hotel_list is None:
            bot.send_message(user_id, 'Сервер не отвечает, попробуйте повторить запрос позже.',
                             reply_markup=answer_button)
        else:
            logger.info(f'User "{user_id}" no hotels found')
            bot.send_message(user_id, 'Ничего не найдено, попробуйте изменить параметры поиска.',
                             reply_markup=answer_button)
