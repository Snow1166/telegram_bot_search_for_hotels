from database.db_models import db, UserRequest
import json


def add_request_db(id_user: str, command: str, name_city: str, hotel_list: json) -> None:
    """
    Function for adding data to the database.
    Args:
        :param id_user: accepts user id
        :param command: accepts the user's search command
        :param name_city: accepts the entered name for the search
        :param hotel_list: accepts JSON with a list of hotels shown to the user during the search
    :return: None
    """
    with db:
        UserRequest.create(id_user=id_user,
                           command=command,
                           name_city=name_city,
                           hotel_list=hotel_list
                           )


def get_request_db(user: str) -> list:
    """
    The function returns the user's search history from the database.
    :param user: accepts user id
    :return: returns a list with query history dictionaries
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
