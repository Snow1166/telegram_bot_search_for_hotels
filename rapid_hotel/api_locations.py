import re
import json

import requests
import config
from loguru import logger


@logger.catch()
def request_location(message: str, user_id: str) -> dict:
    """
    Получает название города и запрашивает список локаций у api.
    :param message: название города
    :param user_id: id пользователя для логирования
    :return: возвращает словарь локаций.
    """
    try:
        querystring = {"query": {message}, "locale": "ru_RU", "currency": "rub"}
        logger.info(f'User "{user_id}" requests locations with parameters "{querystring}"')
        answer = requests.get(config.url_search_locations, headers=config.hotels_headers, params=querystring,
                              timeout=15)
        logger.info(f'User "{user_id}" requests status code: {answer.status_code}')
        if answer.status_code == requests.codes.ok:
            locations = json.loads(answer.text)
            return locations
        raise ConnectionError(f'Connection Error {answer.status_code}')
    except (requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            ConnectionError) as ex:
        logger.error(f'User "{user_id}" request_location: {ex}')


@logger.catch()
def get_locations_list(message: str, user_id: str) -> dict:
    """
    Получает название города, вызывает функцию запроса api локаций,
    получает словарь локаций, парсит словарь, затем его возвращает.
    :param message: название города.
    :param user_id: id пользователя.
    :return: словарь локаций
    """
    json_loc = request_location(message, user_id)
    if json_loc:
        logger.info(f'User "{user_id}" parsing list location hotels')
        locations = dict()
        for item in json_loc['suggestions'][0]['entities']:
            location_name = re.sub(config.pattern_delete_spans, '', item['caption'])
            locations[location_name] = item['destinationId']
        return locations

