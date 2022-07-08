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
            with open('hotel_list.json', 'w', encoding='utf-8') as file:
                json.dump(hotel_list, file, ensure_ascii=False, indent=4)
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
