import requests
import json
import config
import loguru


@loguru.logger.catch()
def request_hotels(querystring):
    try:
        url = "https://hotels4.p.rapidapi.com/properties/list"
        answer = requests.get(url, headers=config.hotels_headers, params=querystring, timeout=15)
        if answer.status_code == requests.codes.ok:
            hotel_list = json.loads(answer.text)
            return hotel_list
    except TimeoutError:
        return None


def get_hotels_list(querystring):
    json_hotel_list = request_hotels(querystring)
    hotel_list = dict()
    for hotel in json_hotel_list['data']['body']['searchResults']['results']:
        id_hotel = hotel['id']
        hotel_list[id_hotel] = hotel
    return hotel_list

# querystring = {"destinationId": 332483, "pageNumber": "1", "pageSize": "25",
#                "checkIn": '2022-08-04', "checkOut": '2022-08-06', "adults1": "1",
#                "priceMin": 3000, "priceMax": 2000,
#                "sortOrder":"DISTANCE_FROM_LANDMARK", "distancMin": 1,"distancMax": 2,
#                "locale": "ru-RU", "currency": "RUB"}
#
# request_hotels(querystring)