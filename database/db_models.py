from peewee import *
import datetime

db = SqliteDatabase('users.db')


class BaseModel(Model):
    """
    Создание базовой модели
    """

    class Meta:
        database = db
        order_by = 'created_date'


class UserRequest(BaseModel):
    """
    Создание формы таблицы базы данных
    """
    id_user = IntegerField()
    command = CharField()
    name_city = CharField()
    hotel_list = CharField()
    created_date = DateTimeField(default=datetime.datetime.now())
