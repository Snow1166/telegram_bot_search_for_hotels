from t_bot.utilities.func import *
from requests_hotel.hotel_list import get_hotels_list
from requests_hotel.photo_hotel import add_photo


def get_final_hotel_list(querystring, total_hotels, total_photo):
    hotel_list = get_hotels_list(querystring)
    ready_list_hotels = dict()
    for hotel in hotel_list.values():
        total_hotels -= 1
        id_hotel = hotel['id']
        ready_list_hotels[id_hotel] = get_name(hotel)
        ready_list_hotels[id_hotel].update(get_address(hotel))
        ready_list_hotels[id_hotel].update(get_star_rating(hotel))
        ready_list_hotels[id_hotel].update(get_unformatted_rating(hotel))
        ready_list_hotels[id_hotel].update(get_landmarks(hotel))
        ready_list_hotels[id_hotel].update(get_price(hotel))
        ready_list_hotels[id_hotel].update(get_site(hotel))
        if total_hotels == 0:
            break
    ready_list_hotels = add_photo(ready_list_hotels, total_photo)
    return ready_list_hotels
