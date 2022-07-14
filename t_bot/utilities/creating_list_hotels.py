from t_bot.utilities import func
from rapid_hotel.api_hotel_list import api_get_hotels_list
from rapid_hotel.api_photo_hotel import add_photo
from telebot import types
from loader import bot
from loguru import logger
from t_bot.keyboard_markup.inline_keyboard import after_search
from database.users import User


@logger.catch()
def get_final_hotel_list(querystring, total_hotels, total_photo, total_day, user_id):
    hotel_list = api_get_hotels_list(querystring, user_id)
    ready_list_hotels = dict()
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
def send_hotels_list_for_user(user_id):
    user = User.get_user(user_id)
    querystring = user.get_querystring()
    total_photo = user.get_total_photo()
    total_hotels = user.get_total_hotels()
    total_day = user.total_day
    hotel_list = get_final_hotel_list(querystring, total_hotels, total_photo, total_day, user_id)
    answer_button = after_search()
    if hotel_list:
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

