"""Location Request Module"""
import re
import json
from typing import Any

import requests

from loguru import logger

import config


@logger.catch()
def request_location(message: str, user_id: str) -> Any | None:
    """
    Gets the name of the city and requests a list of locations from the api.
    :param message: name of the city
    :param user_id: user id for logging
    :return: returns a dictionary of locations.
    """
    try:
        querystring = {"query": {message}, "locale": "ru_RU", "currency": "rub"}
        logger.info(f'User "{user_id}" requests locations with parameters "{querystring}"')
        answer = requests.get(config.URL_SEARCH_LOCATIONS,
                              headers=config.hotels_headers,
                              params=querystring,
                              timeout=15)
        logger.info(f'User "{user_id}" requests status code: {answer.status_code}')
        if answer.status_code == 200:
            locations = json.loads(answer.text)
            return locations
        raise ConnectionError(f'Connection Error {answer.status_code}')
    except (requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            ConnectionError) as ex:
        logger.error(f'User "{user_id}" request_location: {ex}')
    return None


@logger.catch()
def get_locations_list(message: str, user_id: str) -> dict | None:
    """
    Gets the name of the city, calls the location api request function,
    gets a dictionary of locations, parses the dictionary, then returns it.
    :param message: the name of the city.
    :param user_id: user id.
    :return: dictionary of locations
    """
    json_loc = request_location(message, user_id)
    if json_loc:
        logger.info(f'User "{user_id}" parsing list location hotels')
        locations = {}
        for item in json_loc['suggestions'][0]['entities']:
            location_name = re.sub(config.PATTERN_DELETE_SPANS, '', item['caption'])
            locations[location_name] = item['destinationId']
        return locations
    return None
