from peewee import *
import datetime


db = SqliteDatabase('users.db')


class BaseModel(Model):
    class Meta:
        database = db
        order_by = 'created_date'


class UserRequest(BaseModel):
    id_user = IntegerField()
    command = CharField()
    name_city = CharField()
    hotel_list = CharField()
    created_date = DateTimeField(default=datetime.datetime.now())


