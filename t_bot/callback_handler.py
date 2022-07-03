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