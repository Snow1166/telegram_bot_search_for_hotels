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
        return {"price": f"{(hotel['ratePlan']['price']['exactCurrent'])} руб."}
    except KeyError:
        return {"price": "Уточняйте цену на сайте."}


def get_total_price(hotel, total_day):
    try:
        return {"total_price": f"{int(hotel['ratePlan']['price']['exactCurrent'] * total_day)} руб."}
    except KeyError:
        return {"total_price": "Уточняйте цену на сайте."}


def get_site(hotel):
    try:
        return {"site": f'https://www.hotels.com/ho{hotel["id"]}'}
    except KeyError:
        return {"price": "Страница не указана"}
