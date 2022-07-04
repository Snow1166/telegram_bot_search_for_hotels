from telebot.handler_backends import State, StatesGroup


class User(StatesGroup):
    command = State()
    destinationId = State()
    checkIn = State()
    checkOut = State()
    min_high_price = State()
    distance = State()
    photo_hotel = State()
    total_photos = State()
