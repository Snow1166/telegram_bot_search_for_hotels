from config import alphabet
from database.users import User


def get_name(hotel):
    return {'name': hotel.get('name', 'Название отеля не указано')}


def get_address(hotel):
    return {'address': hotel.get('address', {}).get('streetAddress', 'Адрес не указан')}


def get_star_rating(hotel):
    try:
        return {"starRating": '⭐' * int(hotel['starRating'])}
    except KeyError:
        return {"starRating": " "}


def get_unformatted_rating(hotel):
    return {"unformattedRating": hotel.get('guestReviews', {}).get('unformattedRating', 'Рейтинг не указан.')}


def get_landmarks(hotel):
    return {"landmarks": hotel.get('landmarks', {})[0].get('distance', 'Дистанция до центра не указана.')}


def get_price(hotel):
    try:
        return {"price": f"{int(hotel['ratePlan']['price']['exactCurrent']):,} руб."}
    except KeyError:
        return {"price": "Уточняйте цену на сайте."}


def get_total_price(hotel, total_day):
    try:
        return {"total_price": f"{int(hotel['ratePlan']['price']['exactCurrent'] * total_day):,} руб."}
    except KeyError:
        return {"total_price": "Уточняйте цену на сайте."}


def get_site(hotel):
    return {"site": f'https://www.hotels.com/ho{hotel["id"]}/'}


def format_message_for_user(hotel, total_day):
    message = f"""
🏨 <a href="{hotel['site']}/">{hotel['name']}</a> {hotel['starRating']}        
🗺 <b>Адрес:</b> {hotel['address']}
📈 <b>Рейтинг отеля:</b> {hotel['unformattedRating']}
🧭 <b>Расположение от центра:</b> {hotel['landmarks']}
💲 <b>Цена за ночь:</b> {hotel['price']}
💲 <b>Цена за {total_day} (дня/дней):</b> {hotel['total_price']} 
      """
    return message


def format_message_for_user_history(hotel):
    message = f"""
🏨 <a href="{hotel['site']}/">{hotel['name']}</a> {hotel['starRating']}        
🗺 <b>Адрес:</b> {hotel['address']}
💲 <b>Цена за ночь:</b> {hotel['price']}
      """
    return message


def city_correct(name_city):
    return all(sym in alphabet for sym in name_city.lower())


def price_correct(min_max_price):
    price_list = min_max_price.split()
    if len(price_list) == 2 and price_list[0].isdigit() and price_list[1].isdigit() and \
            -1 < int(price_list[0]) < int(price_list[1]):
        return True
    return False


def distance_correct(distance):
    return distance.isdigit() and int(distance) >= 0


def check_distance(user_id, hotel):
    user = User.get_user(user_id)
    if user.command != '/bestdeal':
        return True
    dist = hotel.get('landmarks', [{}])[0].get('distance')
    if float(user.distance) >= float(dist.replace(',', '.').split()[0]):
        return True
