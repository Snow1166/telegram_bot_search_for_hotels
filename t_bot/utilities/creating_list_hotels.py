from t_bot.utilities import func
from requests_hotel.hotel_list import get_hotels_list
from requests_hotel.photo_hotel import add_photo
from telebot import types
from config import bot, user_dict


def get_final_hotel_list(querystring, total_hotels, total_photo, total_day):
    hotel_list = get_hotels_list(querystring)
    ready_list_hotels = dict()
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
        ready_list_hotels = add_photo(ready_list_hotels, total_photo)
    return ready_list_hotels


def send_hotels_list_for_user(user_id):
    querystring = user_dict[user_id].get_querystring()
    print(querystring)
    total_photo = user_dict[user_id].get_total_photo()
    total_hotels = user_dict[user_id].get_total_hotels()
    hotel_list = get_final_hotel_list(querystring, total_hotels, total_photo, user_dict[user_id].total_day)
    for hotel in hotel_list.values():
        bot.send_message(user_id,
                         f"""
<b>Название отеля:</b> {hotel['name']} {hotel['starRating']}        
<b>Адрес:</b> {hotel['address']}
<b>Рейтинг отеля:</b> {hotel['unformattedRating']}
<b>Страницу с отелем:</b> {hotel['site']}
<b>Расположение от центра:</b> {hotel['landmarks']}
<b>Цена за ночь:</b> {hotel['price']}
<b>Цена за {user_dict[user_id].total_day} (дня/дней):</b> {hotel['total_price']} 
      """,
                         disable_web_page_preview=True)
        if total_photo > 0:
            media_group = [types.InputMediaPhoto(media=url) for url in hotel['photo']]
            bot.send_media_group(user_id, media_group)
