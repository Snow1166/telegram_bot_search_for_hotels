import requests
import json
import config


def request_photo(id_hotel):
    # url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    # answer = requests.get(url, headers=config.hotels_headers, params={"id": f"{id_hotel}"})
    # if answer.status_code == requests.codes.ok:
    #     photo_list = json.loads(answer.text)
    #     with open('photo_list.json', 'w', encoding='utf-8') as file:
    #         json.dump(photo_list, file, ensure_ascii=False, indent=4)
    #     return photo_list

    """ Сохранение запроса в json и дальнейшее его использование его вместо запроса для экономии вызовов"""

    with open('photo_list.json', 'r', encoding='utf-8') as file:
        photo_list = json.load(file)
    return photo_list


def get_url_photo(quantity, id_hotel):
    photo_list = request_photo(id_hotel)
    photo_list_url = list()
    for i in range(quantity):
        photo_list_url.append(photo_list['hotelImages'][i]['baseUrl'].replace("{size}", "b"))
    return photo_list_url