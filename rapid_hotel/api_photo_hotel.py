import requests
import json
import config
from loguru import logger


@logger.catch()
def request_photo(id_hotel: int, user_id: int) -> dict:
    """
    Получает id отедя и запрашивает у api словарь с url фотографий
    :param id_hotel: id отелей
    :param user_id: id пользователя
    :return: словарь с url фотографий
    """
    if not config.DEBUG:
        try:
            answer = requests.get(config.url_get_hotel_photos, headers=config.hotels_headers,
                                  params={"id": f"{id_hotel}"})
            logger.info(f'User "{user_id}" requests list photos for a hotel with id "{id_hotel}"')
            if answer.status_code == requests.codes.ok:
                photo_list = json.loads(answer.text)
                return photo_list
            raise ConnectionError(f'Connection Error {answer.status_code}')
        except (requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError,
                ConnectionError) as ex:
            logger.error(f'User "{user_id}" request_photos: {ex}')
    else:
        with open('photo_list.json', 'r', encoding='utf-8') as file:
            photo_list = json.load(file)
        return photo_list


@logger.catch()
def get_url_photo(id_hotel: int, total_photo: int, user_id: int) -> list:
    """
    Получает id отеля и количество фотографий,
    вызывает функцию api, получает словарь с url фотографий,
    парсит и возвращает список с введенным количеством фотографий.
    :param id_hotel: id отеля
    :param total_photo: количество фотографий
    :param user_id: id пользователя
    :return: список фотографий
    """
    photo_list = request_photo(id_hotel, user_id)
    photo_list_url = list()
    if photo_list:
        logger.info(f'User "{user_id}" creating a list of photo links for a hotel "{id_hotel}"')
        for i in range(total_photo):
            photo_list_url.append(photo_list['hotelImages'][i]['baseUrl'].replace("{size}", "b"))
        return photo_list_url
    logger.info(f'User "{user_id}" server error, the list of photos was not received "{id_hotel}"')


@logger.catch()
def add_photo(hotel_list: dict, total_photo: int, user_id: int) -> dict:
    """
    Добавляет в словарь отелей фотографии
    :param hotel_list: словарь отелей
    :param total_photo: количество фотографий
    :param user_id: id пользователя
    :return: словарь отелей с фотографиями
    """
    logger.info(f'User "{user_id}" adding a list of photos to a list of hotels')
    for id_hotel in hotel_list:
        photo = get_url_photo(id_hotel, total_photo, user_id)
        if photo:
            hotel_list[id_hotel].update({"photo": photo})
        else:
            hotel_list[id_hotel].update({"photo": False})
    return hotel_list
