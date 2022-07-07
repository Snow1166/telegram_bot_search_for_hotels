from telebot import types
from config import bot, user_dict
from t_bot.utilities.creating_list_hotels import get_final_hotel_list


def get_lowprice_hotel(user_id):
    querystring = user_dict[user_id].get_querystring_lowprice()
    total_photo = user_dict[user_id].get_total_photo()
    total_hotels = user_dict[user_id].get_total_hotels()

    hotel_list = get_final_hotel_list(querystring, total_hotels, total_photo, )
    for hotel in hotel_list.values():
        bot.send_message(user_id,
                         f"""
        <b>Название отеля:</b> {hotel['name hotel']} {hotel['starRating']}        
        <b>Адрес:</b> {hotel['address']}
        <b>Рейтинг отеля:</b> {hotel['unformattedRating']}"
        <b>Страницу с отелем:</b> {hotel['site']}"
        <b>Расположение от центра:</b> {hotel['landmarks']}
        <b>Цена за ночь:</b> {hotel['price']}. Суммарная стоимость: пока нет
        <b>Цена за {user_dict[user_id].total_day} дня:</b> {hotel['price']}. 
      """)
        media_group = [types.InputMediaPhoto(media=url) for url in hotel['photo']]
        bot.send_media_group(user_id, media_group)
