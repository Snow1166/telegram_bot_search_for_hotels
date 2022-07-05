import requests
import json
import config
from requests_hotel.photo_hotel import get_url_photo

def request_hotels(querystring):
    url = "https://hotels4.p.rapidapi.com/properties/list"

    # answer = requests.get(url, headers=config.hotels_headers, params=querystring)
    # if answer.status_code == requests.codes.ok:
    #     hotel_list = json.loads(answer.text)
    #     with open('hotel_list.json', 'w', encoding='utf-8') as file:
    #         json.dump(hotel_list, file, ensure_ascii=False, indent=4)
    #     return hotel_list
    #
    # """ Сохранение запроса в json и дальнейшее его использование его вместо запроса для экономии вызовов"""
    #
    with open('hotel_list.json', 'r', encoding='utf-8') as file:
        hotel_list = json.load(file)
    return hotel_list


querystring = {"destinationId": "483449", "pageNumber": "1", "pageSize": "25", "checkIn": "2022-07-20",
               "checkOut": "2022-07-25", "adults1": "1", "sortOrder": "PRICE", "locale": "ru_RU", "currency": "RUB"}


# def get_locations_list(message):
#     """Парсим json файл поиска города и выдаем чистый словарь с локациями"""
#     json_loc = request_location(message)
#     locations = dict()
#     for item in json_loc['suggestions'][0]['entities']:
#         location_name = re.sub(config.CLEAN_NAME, '', item['caption'])
#         locations[location_name] = item['destinationId']
#     return locations


def get_hotels_list(message):
    """Парсим json файл поиска города и выдаем чистый словарь с локациями"""
    json_hotel_list = request_hotels(querystring)
    hotel_list = dict()
    for item in json_hotel_list['data']['body']['searchResults']['results']:
        if 'ratePlan' in item:
            id_hotel = item['id']
            hotel_list[id_hotel] = {"name hotel": item['name']}
            if 'streetAddress' in item['address']:
                hotel_list[id_hotel].update({"address": item['address']['streetAddress']})
            else:
                hotel_list[id_hotel].update({"address": item['address']['locality']})
            hotel_list[id_hotel].update({"starRating": '⭐' * int(item['starRating'])})
            hotel_list[id_hotel].update({"unformattedRating": item['guestReviews']['unformattedRating']})
            hotel_list[id_hotel].update({"landmarks": item['landmarks'][0]['distance']})
            hotel_list[id_hotel].update({"price": item['ratePlan']['price']['exactCurrent']})
            hotel_list[id_hotel].update({"site": f'https://www.hotels.com/ho{item["id"]}'})
            photo = get_url_photo(3, id_hotel)
            hotel_list[id_hotel].update({"photo": photo})

    # with open('hotel.json', 'w', encoding='utf-8') as file:
    #     json.dump(hotel_list, file, ensure_ascii=False, indent=4)
    return hotel_list


