"""The module for requesting a list of hotels"""
import json

import requests
from loguru import logger

import config
from t_bot.utilities import func


@logger.catch()
def api_request_hotels(querystring: dict, user_id: str) -> dict | None:
    """
    Gets the request string and requests from the hotels json api
    :param querystring: api request string
    :param user_id: user id for logging
    :return: json hotels
    """
    if config.DEBUG:
        with open('hotel_list.json', 'r', encoding='utf-8') as file:
            hotel_list = json.load(file)
        return hotel_list
    try:
        logger.info(f'User "{user_id}" request a list of hotels with parameters {querystring}')
        answer = requests.get(config.URL_PROPERTIES_LIST,
                              headers=config.hotels_headers,
                              params=querystring,
                              timeout=config.TIMEOUT_RAPID)
        logger.info(f'User "{user_id}" requests status code: {answer.status_code}')
        if func.check_status_code(answer.status_code):
            hotel_list = json.loads(answer.text)
            if config.DEBUG_SAVE_REQUESTS:
                with open('hotel_list.json', 'w', encoding='utf-8') as file:
                    json.dump(hotel_list, file, ensure_ascii=False, indent=4)
            return hotel_list
        raise ConnectionError(f'Connection Error {answer.status_code}')
    except (requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            ConnectionError) as ex:
        logger.error(f'User "{user_id}" request_hotels: {ex}')
    return None


@logger.catch()
def api_get_hotels_list(querystring: dict, user_id: str) -> dict | None:
    """
    Gets the query string and user id, requests a list of hotels,
    parses and returns a dictionary with a list of hotels
    :param querystring: query string
    :param user_id: user id
    :return: dictionary of hotels
    """
    json_hotel_list = api_request_hotels(querystring, user_id)
    if json_hotel_list:
        logger.info(f'User "{user_id}" parsing list of hotels')
        hotel_list = {}
        for hotel in json_hotel_list['data']['body']['searchResults']['results']:
            if func.check_distance(user_id, hotel):
                id_hotel = hotel['id']
                hotel_list[id_hotel] = hotel
        return hotel_list
    return None
