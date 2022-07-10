import requests
import json
import config
from loguru import logger


@logger.catch()
def request_hotels(querystring, user_id):
    try:
        logger.info(f'User "{user_id}" request a list of hotels with parameters {querystring}')
        answer = requests.get(config.url_properties_list, headers=config.hotels_headers, params=querystring, timeout=15)
        logger.info(f'User "{user_id}" requests status code: {answer.status_code}')
        if answer.status_code == requests.codes.ok:
            hotel_list = json.loads(answer.text)
            with open('hotel_list.json', 'w', encoding='utf-8') as file:
                json.dump(hotel_list, file, ensure_ascii=False, indent=4)
            return hotel_list
    except TimeoutError:
        return None


@logger.catch()
def get_hotels_list(querystring, user_id):
    json_hotel_list = request_hotels(querystring, user_id)
    logger.info(f'User "{user_id}" parsing list of hotels')
    hotel_list = dict()
    for hotel in json_hotel_list['data']['body']['searchResults']['results']:
        id_hotel = hotel['id']
        hotel_list[id_hotel] = hotel
    return hotel_list
