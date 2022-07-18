"""Callback Module"""
from datetime import date, timedelta

from loguru import logger
from telegram_bot_calendar import DetailedTelegramCalendar
from telebot.types import CallbackQuery

from config import bot, COMMAND_LIST, STICKER_WAIT
from database.users import User
from database.state import StateUser
from t_bot.keyboard_markup.inline_keyboard import hotel_choice, photo_choice
from t_bot.keyboard_markup.inline_keyboard import photo_bool_choice, button_cancel_ready
from t_bot.command.hotel_search import send_hotels_list_for_user


@logger.catch()
@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id='checkin'))
def set_checkin(call: CallbackQuery) -> None:
    """
    Creates calendar buttons and asks the user for the check-in date.
    :param call:
    """
    user = User.get_user(call.from_user.id)
    logger.info(f'User "{call.message.chat.id}" selects the arrival date {call.data}')
    result, key, step = DetailedTelegramCalendar(calendar_id='checkin',
                                                 min_date=date.today(),
                                                 locale='ru').process(call.data)
    if not result and key:
        bot.edit_message_text("Выберите дату заезда:",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        user.checkin = result
        calendar, step = DetailedTelegramCalendar(calendar_id='checkout',
                                                  min_date=user.checkin + timedelta(days=1),
                                                  locale='ru').build()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Выберите дату отъезда",
                              reply_markup=calendar)


@logger.catch()
@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id='checkout'))
def set_checkout(call: CallbackQuery) -> None:
    """
    Receives and records the user's check-in and check-out data.
    If the best deal command is selected, it asks the user for a range of hotel prices.
    Otherwise, it asks the user how many hotels to show.
    :param call:
    """
    user = User.get_user(call.from_user.id)
    logger.info(f'User "{call.message.chat.id}" selects the departure date {call.data}')
    result, key, step = DetailedTelegramCalendar(calendar_id='checkout',
                                                 min_date=user.checkin + timedelta(days=1),
                                                 locale='ru').process(
        call.data)
    if not result and key:
        bot.edit_message_text("Выберите дату отъезда:",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        user.total_day = int((result - user.checkin).days)
        user.checkout = result.strftime("%Y-%m-%d")
        user.checkin = user.checkin.strftime("%Y-%m-%d")
        if user.command == '/bestdeal':
            bot.set_state(call.message.chat.id, StateUser.min_max_price)
            user.last_message_bot = bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='Введите диапазон цен отелей, через пробел в рублях.',
                reply_markup=button_cancel_ready())
        else:
            button = hotel_choice(call.from_user.id)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Сколько отелей вывести для просмотра?",
                                  reply_markup=button)


@logger.catch()
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: CallbackQuery) -> None:
    """
    Receives all callback calls, determines the type of received data
    at the beginning of the line. Records data. Requests additional data from the user.
    If all the data is received, it calls the function
    to send the search and send the result to the user.
    :param call:
    """
    user = User.get_user(call.from_user.id)
    if call.data.startswith('id_loc'):
        destination_id = call.data.split()[1]
        logger.info(f'User "{call.from_user.id}" choose destination_id "{destination_id}"')
        user.destination_id = destination_id
        bot.answer_callback_query(callback_query_id=call.id)
        calendar, step = DetailedTelegramCalendar(calendar_id='checkin',
                                                  min_date=date.today(),
                                                  locale='ru').build()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Выберите дату заезда",
                              reply_markup=calendar)

    elif call.data.startswith('hotel'):
        total_hotel = call.data.split()[1]
        logger.info(f'User "{call.from_user.id}" choose total_hotel "{total_hotel}"')
        user.total_hotel = total_hotel
        button = photo_bool_choice(call.from_user.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Вы хотите посмотреть фотографии отелей?',
                              reply_markup=button)

    elif call.data.startswith('bool_photo'):
        photos_bool = call.data.split()[1]
        logger.info(f'User "{call.from_user.id}" send photos? "{photos_bool}"')
        user.bool_photo = photos_bool
        bot.answer_callback_query(callback_query_id=call.id)
        if photos_bool == 'no':
            user.total_photos = 0
            bot.set_state(call.message.chat.id, StateUser.command)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Подождите, ищем подходящие предложения...",
                                  reply_markup=None)
            user.last_message_bot = bot.send_sticker(call.message.chat.id, STICKER_WAIT)
            send_hotels_list_for_user(call.from_user.id)
        elif photos_bool == 'yes':
            button = photo_choice(call.from_user.id)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Сколько фотографий отелей показать?',
                                  reply_markup=button)

    elif call.data.startswith('photo'):
        bot.set_state(call.message.chat.id, StateUser.command)
        total_photos = call.data.split()[1]
        logger.info(f'User "{call.from_user.id}" choose total_photos "{total_photos}"')
        user.total_photos = total_photos
        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Подождите, ищем походящие предложения...",
                              reply_markup=None)
        user.last_message_bot = bot.send_sticker(call.message.chat.id, STICKER_WAIT)
        send_hotels_list_for_user(call.from_user.id)

    elif call.data.startswith('cancel'):
        bot.set_state(call.message.chat.id, StateUser.command)
        logger.info(f'User "{call.from_user.id}" cancel, return to the main menu"')
        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=COMMAND_LIST,
                              reply_markup=None)

    elif call.data.startswith('end'):
        bot.set_state(call.message.chat.id, StateUser.command)
        logger.info(f'User "{call.from_user.id}" search completed')
        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Спасибо, что воспользовались ботом по поиску отелей.',
                              reply_markup=None)
        sticker_end = 'CAACAgIAAxkBAAEWBKhi0VFcFp1tiTKLJ_q4PYEQhMLVrQACChUAAl_zwUl2NIzsRPf4fykE'
        bot.send_sticker(call.message.chat.id, sticker_end)
