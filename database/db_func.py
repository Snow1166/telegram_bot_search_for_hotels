from database.db_models import db, UserRequest
import json


def add_request_db(id_user: int, command: str, name_city: str, hotel_list: json) -> None:
    """
    Функция для добавления данный в базу данных.
    Args:
        :param id_user: принимает id пользователя
        :param command: принимает команду поиска пользователя
        :param name_city: принимает введённое название для поиска
        :param hotel_list: принимает JSON со списком отелей показанных пользователю при поиске
    :return: None
    """
    with db:
        UserRequest.create(id_user=id_user,
                           command=command,
                           name_city=name_city,
                           hotel_list=hotel_list
                           )


def get_request_db(user: int) -> list:
    """
    Функция возвращает из базы данных историю поиска пользователя.
    :param user: id пользователя
    :return: возвращает список со словарями истории запросов
    """
    with db:
        history_list = list()
        for data in UserRequest.select().where(UserRequest.id_user == user):
            request = ({'data': data.created_date,
                        'command': data.command,
                        'city': data.name_city,
                        'hotel_list': json.loads(data.hotel_list)})
            history_list.append(request)
    return history_list
