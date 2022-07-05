from telebot.handler_backends import State, StatesGroup


class StateUser(StatesGroup):
    start = State()
    command = State()
    destinationId = State()
    checkIn = State()
    checkOut = State()
    min_high_price = State()
    distance = State()
    total_photos = State()
    total_hotel = State()