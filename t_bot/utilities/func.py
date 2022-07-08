def get_name(hotel):
    if 'name' in hotel:
        return {"name hotel": f"{hotel['name']}"}
    else:
        return {"name hotel": "Название отеля не указано"}


def get_address(hotel):
    try:
        return {"address": f"{hotel['address']['streetAddress']}"}
    except KeyError:
        return {"address": "Адрес не указан."}


def get_star_rating(hotel):
    try:
        return {"starRating": '⭐' * int(hotel['starRating'])}
    except KeyError:
        return {"starRating": "Рейтинг не указан."}


def get_unformatted_rating(hotel):
    try:
        return {"unformattedRating": hotel['guestReviews']['unformattedRating']}
    except KeyError:
        return {"unformattedRating": "Рейтинг не указан."}


def get_landmarks(hotel):
    try:
        return {"landmarks": hotel['landmarks'][0]['distance']}
    except KeyError:
        return {"landmarks": "Дистанция до центра не указана."}


def get_price(hotel):
    try:
        return {"price": hotel['ratePlan']['price']['exactCurrent']}
    except KeyError:
        return {"price": "Уточняйте цену на сайте."}


def get_site(hotel):
    try:
        return {"site": f'https://www.hotels.com/ho{hotel["id"]}'}
    except KeyError:
        return {"price": "Страница не указана"}
