from config import bot


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswith('id_loc'):
        bot.answer_callback_query(callback_query_id=call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="город выбран",
                              reply_markup=None)

    elif call.data.startswith('checkIn'):
        pass
    elif call.data.startswith('checkOut'):
        pass