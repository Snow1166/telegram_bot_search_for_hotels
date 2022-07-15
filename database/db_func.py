from database.db_models import db, UserRequest
import json


def add_request_db(id_user, command, name_city, hotel_list):
    with db:
        UserRequest.create(id_user=id_user,
                           command=command,
                           name_city=name_city,
                           hotel_list=hotel_list
                           )


def get_request_db(user):
    with db:
        history_list = list()
        for data in UserRequest.select().where(UserRequest.id_user == user):
            request = ({'data': data.created_date,
                        'command': data.command,
                        'city': data.name_city,
                        'hotel_list': json.loads(data.hotel_list)})
            history_list.append(request)
    return history_list
