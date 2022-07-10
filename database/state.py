from telebot.handler_backends import State, StatesGroup


class StateUser(StatesGroup):
    command = State()
    destination_id = State()
    checkin = State()
    min_max_price = State()
    distance = State()
    total_hotel = State()
    bool_photo = State
    total_photos = State()

