from config import bot, user_dict
from database.state import StateUser
from t_bot.keyboard_markup.inline_keyboard import city_markup, photo_bool_choice, hotel_choice
from loguru import logger
from t_bot.utilities import func


@logger.catch()
@bot.message_handler(state=StateUser.destination_id)
def get_search_city(message):
    if message.text.lower() == 'лондон':
        bot.send_message(message.chat.id,
                         'В Лондоне? '
                         'https://www.youtube.com/watch?v=3-TMbwk7FvI')
    if func.city_correct(message.text):
        logger.info(f'User "{message.chat.id}" entered the city of "{message.text} "for the search')
        button = city_markup(message.text, message.chat.id)
        bot.send_message(message.from_user.id,
                         'Уточните, пожалуйста:',
                         reply_markup=button)
    else:
        logger.info(f'User "{message.chat.id}" incorrect city name input "{message.text}"')
        bot.send_message(message.from_user.id, """
Название города не может содержать цифры.
Пожалуйста, введите корректное название города.""")


@logger.catch()
@bot.message_handler(state=StateUser.min_max_price)
def get_min_max_price(message):
    if func.price_correct(message.text):
        price_min, price_max = message.text.split()
        user_dict[message.chat.id].price_min = price_min
        user_dict[message.chat.id].price_max = price_max
        logger.info(f'User "{message.chat.id}" entered the min price "{price_min}" & max price "{price_max}"')
        bot.set_state(message.from_user.id,
                      StateUser.distance,
                      message.chat.id)
        bot.send_message(message.from_user.id,
                         'Укажите максимальное расстояние от центра в километрах.')
    else:
        logger.info(f'User "{message.chat.id}" incorrect min_max_price input "{message.text}"')
        bot.send_message(message.from_user.id, """
Введите минимальную и максимальную цену стоимости отеля через пробел.
Максимальная цена не может быть меньше минимальной. Цены не могут быть отрицательные.""")


@logger.catch()
@bot.message_handler(state=StateUser.distance)
def get_max_distance(message):
    if func.distance_correct(message.text):
        logger.info(f'User "{message.chat.id}" entered the maximum distance "{message.text}"')
        user_dict[message.chat.id].distance = message.text
        button = hotel_choice(message.chat.id)
        bot.send_message(message.from_user.id,
                         'Сколько отелей вывести для просмотра?',
                         reply_markup=button)
    else:
        logger.info(f'User "{message.chat.id}" incorrect distance input "{message.text}"')
        bot.send_message(message.from_user.id, """
Введите максимальное расстояние от центра.
Число должно быть положительное.""")
