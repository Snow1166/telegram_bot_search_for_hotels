from config import bot, user_dict
from database.state import StateUser
from t_bot.keyboard_markup.button_for_photo import total_photo


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
        bot.answer_callback_query(callback_query_id=call.id)
        if answer == 'yes':
            user_dict[call.from_user.id].photo_hotel = answer
            bot.set_state(call.message.chat.id, StateUser.total_photos)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Сколько фотографий выы хотите посмотреть?", reply_markup=total_photo())
        else:
            user_dict[call.from_user.id].photo_hotel = answer
            bot.set_state(call.message.chat.id, StateUser.command)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Вы выбрали без просмотра фотографий", reply_markup=None)

    elif call.data.startswith('total_photo'):
        answer = call.data.split()[1]
        bot.answer_callback_query(callback_query_id=call.id)
        answer = call.data.split()[1]
        user_dict[call.from_user.id].total_photos = answer
        bot.set_state(call.message.chat.id, StateUser.start)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Подождите, ищем походящие предложения...", reply_markup=None)
