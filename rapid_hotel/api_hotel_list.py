import requests
import json
import config
from loguru import logger
from t_bot.utilities import func


@logger.catch()
def api_request_hotels(querystring: dict, user_id: int) -> dict:
    """
    Получает строку запроса и запрашивает у api json отелей
    :param querystring: строка запроса для api
    :param user_id: id ползователя для логирования
    :return: json отелей
    """
    try:
        logger.info(f'User "{user_id}" request a list of hotels with parameters {querystring}')
        answer = requests.get(config.url_properties_list, headers=config.hotels_headers, params=querystring, timeout=15)
        logger.info(f'User "{user_id}" requests status code: {answer.status_code}')
        if answer.status_code == requests.codes.ok:
            hotel_list = json.loads(answer.text)
            return hotel_list
        raise ConnectionError(f'Connection Error {answer.status_code}')
    except (requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            ConnectionError) as ex:
        logger.error(f'User "{user_id}" request_hotels: {ex}')


@logger.catch()
def api_get_hotels_list(querystring: dict, user_id: int) -> dict:
    """
    Получает строку запроса и id пользователя, запрашивает список отелей,
    парсит и возвращает словарь со списком отелей
    :param querystring: строка запроса
    :param user_id: id пользователя
    :return: словарь отелей
    """
    json_hotel_list = api_request_hotels(querystring, user_id)
    if json_hotel_list:
        logger.info(f'User "{user_id}" parsing list of hotels')
        hotel_list = dict()
        for hotel in json_hotel_list['data']['body']['searchResults']['results']:
            if func.check_distance(user_id, hotel):
                id_hotel = hotel['id']
                hotel_list[id_hotel] = hotel
        return hotel_list
