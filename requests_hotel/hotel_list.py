import requests
import json
import config


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
