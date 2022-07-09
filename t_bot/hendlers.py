from config import bot, user_dict
from database.state import StateUser
from t_bot.keyboard_markup.inline_keyboard import city_markup, photo_choice
from loguru import logger


@logger.catch()
@bot.message_handler(state=StateUser.destination_id)
def get_search_city(message):
    if message.text.lower() == 'лондон':
        bot.send_message(message.chat.id,
                         'В Лондоне? '
                         'https://www.youtube.com/watch?v=3-TMbwk7FvI')
    logger.info(f'User "{message.chat.id}" entered the city of "{message.text} "for the search')
    button = city_markup(message.text, message.chat.id)
    bot.set_state(message.from_user.id,
                  StateUser.destination_id,
                  message.chat.id)
    bot.send_message(message.from_user.id,
                     'Уточните, пожалуйста:',
                     reply_markup=button)


@logger.catch()
@bot.message_handler(state=StateUser.min_max_price)
def get_min_max_price(message):
    price_min, price_max = message.text.split()
    user_dict[message.chat.id].price_min = price_min
    user_dict[message.chat.id].price_max = price_max
    logger.info(f'User "{message.chat.id}" entered the min price "{price_min}" & max price "{price_max}"')
    bot.set_state(message.from_user.id,
                  StateUser.distance,
                  message.chat.id)
    bot.send_message(message.from_user.id,
                     'Укажите максимальное расстояние от центра в километрах.')


@logger.catch()
@bot.message_handler(state=StateUser.distance)
def get_max_distance(message):
    logger.info(f'User "{message.chat.id}" entered the maximum distance "{message.text}"')
    user_dict[message.chat.id].distance = message.text
    bot.set_state(message.from_user.id,
                  StateUser.total_photos,
                  message.chat.id)
    button = photo_choice(message.chat.id)
    bot.send_message(message.from_user.id,
                     'Вы хотите посмотреть фотографии отелей?',
                     reply_markup=button)

