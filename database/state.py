from telebot.handler_backends import State, StatesGroup


class StateUser(StatesGroup):
    start = State()
    command = State()
    destination_id = State()
    checkin = State()
    checkout = State()
    min_max_price = State()
    distance = State()
    total_photos = State()
    total_hotel = State()