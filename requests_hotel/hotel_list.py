import requests
import json
import config
from loguru import logger
from t_bot.utilities import func


@logger.catch()
def request_hotels(querystring, user_id):
    try:
        logger.info(f'User "{user_id}" request a list of hotels with parameters {querystring}')
        answer = requests.get(config.url_properties_list, headers=config.hotels_headers, params=querystring, timeout=15)
        logger.info(f'User "{user_id}" requests status code: {answer.status_code}')
        if answer.status_code == requests.codes.ok:
            hotel_list = json.loads(answer.text)
            return hotel_list
        raise ConnectionError
    except TimeoutError:
        logger.error(f'User "{user_id}" request_location: {TimeoutError}')
        return None
    except ConnectionError:
        logger.error(f'User "{user_id}" request_location: {ConnectionError}')
        return None


@logger.catch()
def get_hotels_list(querystring, user_id):
    json_hotel_list = request_hotels(querystring, user_id)
    if json_hotel_list:
        logger.info(f'User "{user_id}" parsing list of hotels')
        hotel_list = dict()
        for hotel in json_hotel_list['data']['body']['searchResults']['results']:
            if func.check_distance(user_id, hotel):
                id_hotel = hotel['id']
                hotel_list[id_hotel] = hotel
        print(hotel_list)
        return hotel_list
    return False
