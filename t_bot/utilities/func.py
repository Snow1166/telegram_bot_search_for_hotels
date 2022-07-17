"""Functional tools module"""
from config import ALPHABET
from database.users import User


def get_name(hotel: dict) -> dict:
    """
    Gets the name of the hotel from the dictionary
    :param hotel: dict
    :return: dict
    """
    return {'name': hotel.get('name', 'Название отеля не указано')}


def get_address(hotel: dict) -> dict:
    """
    Gets the street name from the dictionary
    :param hotel: dict
    :return: dict
    """
    return {'address': hotel.get('address', {}).get('streetAddress', 'Адрес не указан')}


def get_star_rating(hotel: dict) -> dict:
    """
    Gets a star rating from the dictionary
    :param hotel: dict
    :return: dict
    """
    try:
        return {"starRating": '⭐' * int(hotel['starRating'])}
    except KeyError:
        return {"starRating": " "}


def get_unformatted_rating(hotel: dict) -> dict:
    """
    Gets a rating from the dictionary
    :param hotel: dict
    :return: dict
    """
    return {"unformattedRating":
                hotel.get('guestReviews', {}).get('unformattedRating', 'Рейтинг не указан.')}


def get_landmarks(hotel: dict) -> dict:
    """
    Gets the distance from the center from the dictionary
    :param hotel: dict
    :return: dict
    """
    return {"landmarks":
                hotel.get('landmarks', {})[0].get('distance', 'Дистанция до центра не указана.')}


def get_price(hotel: dict) -> dict:
    """
    Gets the price from the dictionary
    :param hotel: dict
    :return: dict
    """
    try:
        return {"price": f"{int(hotel['ratePlan']['price']['exactCurrent']):,} руб."}
    except KeyError:
        return {"price": "Уточняйте цену на сайте."}


def get_total_price(hotel: dict, total_day: int) -> dict:
    """
    Gets the final price from the dictionary
    :param hotel: dict
    :param total_day: int
    :return: dict
    """
    try:
        return {"total_price":
                    f"{int(hotel['ratePlan']['price']['exactCurrent'] * total_day):,} руб."}
    except KeyError:
        return {"total_price": "Уточняйте цену на сайте."}


def get_site(hotel: dict) -> dict:
    """
    Gets a link to the hotel page from the dictionary
    :param hotel: dict
    :return: dict
    """
    return {"site": f'https://www.hotels.com/ho{hotel["id"]}/'}


def format_message_for_user(hotel: dict, total_day: int) -> str:
    """
    Generates a string with the data of the found hotel to send to the user
    :param hotel: dict
    :param total_day: int
    :return: str
    """
    message = f"""
🏨 <a href="{hotel['site']}/">{hotel['name']}</a> {hotel['starRating']}        
🗺 <b>Адрес:</b> {hotel['address']}
📈 <b>Рейтинг отеля:</b> {hotel['unformattedRating']}
🧭 <b>Расположение от центра:</b> {hotel['landmarks']}
💲 <b>Цена за ночь:</b> {hotel['price']}
💲 <b>Цена за {total_day} (дня/дней):</b> {hotel['total_price']} 
      """
    return message


def format_message_for_user_history(hotel: dict) -> str:
    """
    Generates a string with hotel data from the db to send to the user
    :param hotel: dict
    :return: str
    """
    message = f"""
🏨 <a href="{hotel['site']}/">{hotel['name']}</a> {hotel['starRating']}        
🗺 <b>Адрес:</b> {hotel['address']}
💲 <b>Цена за ночь:</b> {hotel['price']}
      """
    return message


def city_correct(name_city: str) -> bool:
    """
    Checking directional input of the city name
    :param name_city: str
    :return: bool
    """
    return all(sym in ALPHABET for sym in name_city.lower())


def price_correct(min_max_price: str) -> bool:
    """
    Checking for the correct entry of the minimum and maximum prices
    :param min_max_price: str
    :return: bool
    """
    price_list = min_max_price.split()
    if len(price_list) == 2 and price_list[0].isdigit() and price_list[1].isdigit() and \
            -1 < int(price_list[0]) < int(price_list[1]):
        return True
    return False


def distance_correct(distance: str) -> bool:
    """
    Checking the distance for correct input
    :param distance: str
    :return: bool
    """
    return distance.isdigit() and int(distance) >= 0


def check_distance(user_id: str, hotel: dict) -> bool:
    """
    Checking the distance of the hotel from the center
    :param user_id: str
    :param hotel: dict
    :return: bool
    """
    user = User.get_user(user_id)
    if user.command != '/bestdeal':
        return True
    dist = hotel.get('landmarks', [{}])[0].get('distance')
    if float(user.distance) >= float(dist.replace(',', '.').split()[0]):
        return True
    return False
