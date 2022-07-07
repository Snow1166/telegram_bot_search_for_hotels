import requests
import json
import config
from requests_hotel.photo_hotel import get_url_photo, add_photo


def request_hotels(querystring):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    # querystring = {"destinationId": "549499", "pageNumber": "1", "pageSize": "25", "checkIn": "2022-07-20",
    #                "checkOut": "2022-07-25", "adults1": "1", "sortOrder": "PRICE", "locale": "ru_RU", "currency": "RUB"}

    answer = requests.get(url, headers=config.hotels_headers, params=querystring)
    if answer.status_code == requests.codes.ok:
        hotel_list = json.loads(answer.text)
    #     with open('hotel_list.json', 'w', encoding='utf-8') as file:
    #         json.dump(hotel_list, file, ensure_ascii=False, indent=4)
        return hotel_list
    #
    # """ Сохранение запроса в json и дальнейшее его использование его вместо запроса для экономии вызовов"""
    #
    # with open('hotel_list.json', 'r', encoding='utf-8') as file:
    #     hotel_list = json.load(file)
    # return hotel_list


def get_hotels_list(querystring, total_hotels, total_photo):
    print(total_hotels)
    print(total_photo)
    print(querystring)
    json_hotel_list = request_hotels(querystring)
    hotel_list = dict()
    for item in json_hotel_list['data']['body']['searchResults']['results']:
        total_hotels -= 1
        if 'ratePlan' in item:
            id_hotel = item['id']
            hotel_list[id_hotel] = {"name hotel": item['name']}
            if 'streetAddress' in item['address']:
                hotel_list[id_hotel].update({"address": f"{item['address']['streetAddress']}, "
                                                        f"{item['address']['locality']}"})
            else:
                hotel_list[id_hotel].update({"address": item['address']['locality']})
            hotel_list[id_hotel].update({"starRating": '⭐' * int(item['starRating'])})
            hotel_list[id_hotel].update({"unformattedRating": item['guestReviews']['unformattedRating']})
            hotel_list[id_hotel].update({"landmarks": item['landmarks'][0]['distance']})
            hotel_list[id_hotel].update({"price": item['ratePlan']['price']['exactCurrent']})
            hotel_list[id_hotel].update({"site": f'https://www.hotels.com/ho{item["id"]}'})
            photo = get_url_photo(id_hotel, total_photo)
            hotel_list[id_hotel].update({"photo": photo})
            if total_hotels == 0:
                break
    # hotel_list = add_photo(hotel_list, total_photo)
    # with open('hotel.json', 'w', encoding='utf-8') as file:
    #     json.dump(hotel_list, file, ensure_ascii=False, indent=4)
    return hotel_list

# def get_sorted_hotel_list(querystring, total_photo, total_hotels):
#     sorted_list_hotels = get_hotels_list(querystring, total_hotels)
#
#     sorted_list_hotels = add_photo(sorted_list_hotels, total_photo)
#     return sorted_list_hotels
# get_hotels_list(55,2,5)