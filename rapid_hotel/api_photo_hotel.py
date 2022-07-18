"""Photo Request Module"""
import json

import requests
from loguru import logger

import config
from t_bot.utilities import func


@logger.catch()
def request_photo(id_hotel: int, user_id: str) -> dict | None:
    """
    Gets the id from the user and requests a dictionary from the api with the url of the photos
    :param id_hotel: id of hotels
    :param user_id: user id
    :return: dictionary with photo urls
    """
    if config.DEBUG:
        with open('photo_list.json', 'r', encoding='utf-8') as file:
            photo_list = json.load(file)
        return photo_list
    try:
        answer = requests.get(config.URL_GET_HOTEL_PHOTOS,
                              headers=config.hotels_headers,
                              params={"id": f"{id_hotel}"},
                              timeout=config.TIMEOUT_RAPID)
        logger.info(f'User "{user_id}" requests list photos for a hotel with id "{id_hotel}"')
        if func.check_status_code(answer.status_code):
            photo_list = json.loads(answer.text)
            return photo_list
        raise ConnectionError(f'Connection Error {answer.status_code}')
    except (requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            ConnectionError) as ex:
        logger.error(f'User "{user_id}" request_photos: {ex}')
    return None


@logger.catch()
def get_url_photo(id_hotel: int, total_photo: int, user_id: str) -> list | None:
    """
    Gets the hotel id and the number of photos,
    calls the api function, gets a dictionary with the url of photos,
    parses and returns a list with the entered number of photos.
    :param id_hotel: hotel id
    :param total_photo: number of photos
    :param user_id: user id
    :return: list of photos
    """
    photo_list = request_photo(id_hotel, user_id)
    photo_list_url = []
    if photo_list:
        logger.info(f'User "{user_id}" creating a list of photo links for a hotel "{id_hotel}"')
        for i in range(total_photo):
            photo_list_url.append(photo_list['hotelImages'][i]['baseUrl'].replace("{size}", "b"))
        return photo_list_url
    logger.info(f'User "{user_id}" server error, the list of photos was not received "{id_hotel}"')
    return None


@logger.catch()
def add_photo(hotel_list: dict, total_photo: int, user_id: str) -> dict:
    """
    Adds photos to the hotel dictionary
    :param hotel_list: dictionary of hotels
    :param total_photo: number of photos
    :param user_id: user id
    :return: dictionary of hotels with photos
    """
    logger.info(f'User "{user_id}" adding a list of photos to a list of hotels')
    for id_hotel in hotel_list:
        photo = get_url_photo(id_hotel, total_photo, user_id)
        if photo:
            hotel_list[id_hotel].update({"photo": photo})
        else:
            hotel_list[id_hotel].update({"photo": False})
    return hotel_list
