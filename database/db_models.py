from peewee import *
import datetime

db = SqliteDatabase('users.db')


class BaseModel(Model):
    """
    Creating a basic model
    """

    class Meta:
        database = db
        order_by = 'created_date'


class UserRequest(BaseModel):
    """
    Creating a database table form
    """
    id_user = CharField()
    command = CharField()
    name_city = CharField()
    hotel_list = CharField()
    created_date = DateTimeField(default=datetime.datetime.now())
