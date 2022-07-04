from config import bot
from database.user import User


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswith('id_loc'):
        User.destinationId = call.data
        bot.answer_callback_query(callback_query_id=call.id)
        bot.set_state(call.message.chat.id, User.checkIn)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите дату заезда", reply_markup=None)
    elif call.data.startswith('photo'):
        answer = call.data.split()[1]
        print(answer)
        bot.answer_callback_query(callback_query_id=call.id)
        if answer == 'yes':
            User.photo_hotel = answer
            bot.set_state(call.message.chat.id, User.total_photos)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Сколько фотографий выы хотите посмотреть?", reply_markup=None)
        else:
            User.photo_hotel = answer
            bot.set_state(call.message.chat.id, User.command)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Вы выбрали без просмотра фотографий", reply_markup=None)