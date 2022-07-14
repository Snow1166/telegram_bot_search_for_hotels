from config import bot
from database.state import StateUser
from t_bot.keyboard_markup.inline_keyboard import city_markup, hotel_choice, button_cancel_ready
from loguru import logger
from t_bot.utilities import func
from database.users import User


@logger.catch()
@bot.message_handler(state=StateUser.destination_id)
def get_search_city(message):
    user = User.get_user(message.chat.id)
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=user.last_message_bot.message_id,
                          text=user.last_message_bot.text,
                          reply_markup=None)
    if message.text.lower() == 'лондон':
        bot.send_message(message.chat.id,
                         'В Лондоне? '
                         'https://www.youtube.com/watch?v=3-TMbwk7FvI')
    if func.city_correct(message.text):
        button = city_markup(message.text, message.chat.id)
        if button:
            bot.set_state(message.from_user.id,
                          StateUser.checkin,
                          message.chat.id)
            logger.info(f'User "{message.chat.id}" entered the city of "{message.text} "for the search')
            bot.send_message(message.from_user.id,
                             'Пожалуйста, уточните местонахождение:',
                             reply_markup=button)
        else:
            if button is None:
                user.last_message_bot = bot.send_message(
                    message.from_user.id, """
Ошибка сервера, попробуйте еще раз
В каком городе ищем гостиницу?""",
                    reply_markup=button_cancel_ready())
            else:
                user.last_message_bot = bot.send_message(
                    message.from_user.id, """
По вашему запросу ничего не найдено
Введите другой город для поиска""",
                    reply_markup=button_cancel_ready())

    else:
        logger.info(f'User "{message.chat.id}" incorrect city name input "{message.text}"')
        user.last_message_bot = bot.send_message(
            message.from_user.id, """
Пожалуйста, повторите название города.
Название города может состоять только из русских букв.
""",
            reply_markup=button_cancel_ready())


@logger.catch()
@bot.message_handler(state=StateUser.min_max_price)
def get_min_max_price(message):
    user = User.get_user(message.chat.id)
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=user.last_message_bot.message_id,
                          text=user.last_message_bot.text,
                          reply_markup=None)
    if func.price_correct(message.text):
        price_min, price_max = message.text.split()
        user.price_min = price_min
        user.price_max = price_max
        logger.info(f'User "{message.chat.id}" entered the min price "{price_min}" & max price "{price_max}"')
        bot.set_state(message.from_user.id,
                      StateUser.distance,
                      message.chat.id)
        user.last_message_bot = bot.send_message(
            message.from_user.id,
            'Укажите максимальное расстояние от центра в километрах.',
            reply_markup=button_cancel_ready())
    else:
        logger.info(f'User "{message.chat.id}" incorrect min_max_price input "{message.text}"')
        user.last_message_bot = bot.send_message(
            message.from_user.id, """
Введите минимальную и максимальную цену стоимости отеля через пробел.
Максимальная цена не может быть меньше минимальной. Цены не могут быть отрицательные.""",
            reply_markup=button_cancel_ready())


@logger.catch()
@bot.message_handler(state=StateUser.distance)
def get_max_distance(message):
    user = User.get_user(message.chat.id)
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=user.last_message_bot.message_id,
                          text=user.last_message_bot.text,
                          reply_markup=None)
    if func.distance_correct(message.text):
        bot.set_state(message.from_user.id,
                      StateUser.total_hotel,
                      message.chat.id)
        logger.info(f'User "{message.chat.id}" entered the maximum distance "{message.text}"')
        user.distance = message.text
        button = hotel_choice(message.chat.id)
        bot.send_message(message.from_user.id,
                         'Сколько отелей вывести для просмотра?',
                         reply_markup=button)
    else:
        logger.info(f'User "{message.chat.id}" incorrect distance input "{message.text}"')
        user.last_message_bot = bot.send_message(
            message.from_user.id, """
Введите максимальное расстояние от центра.
Число должно быть положительное.""",
            reply_markup=button_cancel_ready())
