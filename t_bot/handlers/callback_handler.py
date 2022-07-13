from config import bot, user_dict, command_list
from database.state import StateUser
from t_bot.keyboard_markup.inline_keyboard import hotel_choice, photo_choice, photo_bool_choice, button_cancel_ready
from t_bot.utilities.creating_list_hotels import send_hotels_list_for_user
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import date, timedelta
from loguru import logger


@logger.catch()
@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id='checkin'))
def set_checkin(call):
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
        user_dict[call.from_user.id].checkin = result
        calendar, step = DetailedTelegramCalendar(calendar_id='checkout',
                                                  min_date=user_dict[call.from_user.id].checkin + timedelta(days=1),
                                                  locale='ru').build()
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Выберите дату отъезда",
                              reply_markup=calendar)


@logger.catch()
@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id='checkout'))
def set_checkout(call):
    logger.info(f'User "{call.message.chat.id}" selects the departure date {call.data}')
    result, key, step = DetailedTelegramCalendar(calendar_id='checkout',
                                                 min_date=user_dict[call.from_user.id].checkin + timedelta(days=1),
                                                 locale='ru').process(
        call.data)
    if not result and key:
        bot.edit_message_text("Выберите дату отъезда:",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        user_dict[call.from_user.id].total_day = int((result - user_dict[call.from_user.id].checkin).days)
        user_dict[call.from_user.id].checkout = result.strftime("%Y-%m-%d")
        user_dict[call.from_user.id].checkin = user_dict[call.from_user.id].checkin.strftime("%Y-%m-%d")
        if user_dict[call.from_user.id].command == '/bestdeal':
            bot.set_state(call.message.chat.id, StateUser.min_max_price)
            user_dict[call.message.chat.id].last_message_bot = bot.edit_message_text(
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
def callback_inline(call):
    if call.data.startswith('id_loc'):
        destination_id = call.data.split()[1]
        logger.info(f'User "{call.from_user.id}" choose destination_id "{destination_id}"')
        user_dict[call.from_user.id].destination_id = destination_id
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
        user_dict[call.from_user.id].total_hotel = total_hotel
        button = photo_bool_choice(call.from_user.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Вы хотите посмотреть фотографии отелей?',
                              reply_markup=button)

    elif call.data.startswith('bool_photo'):
        photos_bool = call.data.split()[1]
        logger.info(f'User "{call.from_user.id}" send photos? "{photos_bool}"')
        user_dict[call.from_user.id].bool_photo = photos_bool
        bot.answer_callback_query(callback_query_id=call.id)
        if photos_bool == 'no':
            user_dict[call.from_user.id].total_photos = 0
            bot.set_state(call.message.chat.id, StateUser.command)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Подождите, ищем подходящие предложения...",
                                  reply_markup=None)
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
        user_dict[call.from_user.id].total_photos = total_photos
        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Подождите, ищем походящие предложения...",
                              reply_markup=None)
        send_hotels_list_for_user(call.from_user.id)

    elif call.data.startswith('cancel'):
        bot.set_state(call.message.chat.id, StateUser.command)
        logger.info(f'User "{call.from_user.id}" cancel, return to the main menu"')
        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=command_list,
                              reply_markup=None)

    elif call.data.startswith('end'):
        bot.set_state(call.message.chat.id, StateUser.command)
        logger.info(f'User "{call.from_user.id}" search completed')
        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Спасибо, что воспользовались ботом по поиску отелей.',
                              reply_markup=None)
