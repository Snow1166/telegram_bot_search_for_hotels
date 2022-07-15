from typing import Dict, List
from database.db_models import db, UserRequest
import json


def add_request_db(id_user: int, command: str, name_city: str, hotel_list: dict) -> None:
    """
    Функция для добавления данный в базу данных.
    Args:
        id_user

    """
    with db:
        UserRequest.create(id_user=id_user,
                           command=command,
                           name_city=name_city,
                           hotel_list=hotel_list
                           )


def get_request_db(user: int) -> list:
    with db:
        history_list = list()
        for data in UserRequest.select().where(UserRequest.id_user == user):
            request = ({'data': data.created_date,
                        'command': data.command,
                        'city': data.name_city,
                        'hotel_list': json.loads(data.hotel_list)})
            history_list.append(request)
    return history_list
