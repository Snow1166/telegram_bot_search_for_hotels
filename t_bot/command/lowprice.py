import config
from telebot import types
from config import bot, user_dict
from config import bot
from requests_hotel.hotel_list import get_hotels_list


def get_lowprice_hotel(user_id):
    hotel_list = get_hotels_list(user_dict[user_id].get_querystring_lowprice())
    for hotel in hotel_list.values():
        bot.send_message(user_id, f"""
        <b>Название отеля:</b> {hotel['name hotel']} {hotel['starRating']}        
        <b>Адрес:</b> {hotel['address']}
        <b>Рейтинг отеля:</b> {hotel['unformattedRating']}"
        <b>Страницу с отелем:</b> {hotel['site']}"
        <b>Расположение от центра:</b> {hotel['landmarks']}
        <b>Цена за ночь:</b> {hotel['price']}. Суммарная стоимость: пока нет
      """)
        media_group = [types.InputMediaPhoto(media=url) for url in hotel['photo']]
        bot.send_media_group(user_id, media_group)
