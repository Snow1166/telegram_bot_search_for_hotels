from config import bot, user_dict
from database.state import StateUser
from t_bot.keyboard_markup.inline_keyboard import hotel_choice
from t_bot.command import lowprice

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswith('id_loc'):
        user_dict[call.from_user.id].destinationId = call.data
        bot.answer_callback_query(callback_query_id=call.id)
        bot.set_state(call.message.chat.id, StateUser.checkIn)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите дату заезда", reply_markup=None)

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