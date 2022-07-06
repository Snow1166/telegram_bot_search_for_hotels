from config import bot, user_dict
from database.state import StateUser
from t_bot.keyboard_markup.inline_keyboard import hotel_choice, photo_choice
from t_bot.command import lowprice
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import date


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id='checkIn'))
def set_checkIn(call):
    result, key, step = DetailedTelegramCalendar(calendar_id='checkIn', min_date=date.today(), locale='ru').process(
        call.data)
    if not result and key:
        bot.edit_message_text("Выберите дату заезда:",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        calendar, step = DetailedTelegramCalendar(calendar_id='checkOut', min_date=date.today(), locale='ru').build()
        user_dict[call.from_user.id].checkIn = result
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите дату отъезда",
                              reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id='checkOut'))
def set_checkOut(call):
    result, key, step = DetailedTelegramCalendar(calendar_id='checkOut', min_date=date.today(), locale='ru').process(
        call.data)
    if not result and key:
        bot.edit_message_text("Выберите дату отъезда:",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        user_dict[call.from_user.id].checkOut = result

        if user_dict[call.from_user.id].command == '/bestdeal':
            bot.set_state(call.message.chat.id, StateUser.min_high_price)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите диапазон цен отелей, через пробел',
                                  reply_markup=None)
        else:
            bot.set_state(call.message.chat.id, StateUser.total_photos)
            button = photo_choice()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Вы хотите посмотреть фотографии отелей?',
                                  reply_markup=button)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswith('id_loc'):
        user_dict[call.from_user.id].destinationId = call.data
        bot.answer_callback_query(callback_query_id=call.id)
        bot.set_state(call.message.chat.id, StateUser.checkIn)
        calendar, step = DetailedTelegramCalendar(calendar_id='checkIn', min_date=date.today(), locale='ru').build()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите дату заезда",
                              reply_markup=calendar)


    elif call.data.startswith('photo'):
        answer = call.data.split()[1]
        user_dict[call.from_user.id].total_photos = answer
        bot.answer_callback_query(callback_query_id=call.id)
        bot.set_state(call.message.chat.id, StateUser.total_hotel)
        button = hotel_choice()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Сколько отелей загрузить?", reply_markup=button)

    elif call.data.startswith('hotel'):
        answer = call.data.split()[1]
        user_dict[call.from_user.id].total_hotel = answer
        bot.set_state(call.message.chat.id, StateUser.start)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Подождите, ищем походящие предложения...", reply_markup=None)
        if user_dict[call.from_user.id].command == '/lowprice':
            lowprice.get_lowprice_hotel(call.from_user.id)
        elif user_dict[call.from_user.id].command == '/highprice':
            pass
        elif user_dict[call.from_user.id].command == '/bestdeal':
            pass
