"""Если руки дойдут, попытаться сделать 2 языка"""
language = {
    'ru':
        {'help': (
            '<b>Команды бота</b>\n'
            '/help - список всех команд\n'
            '/lowprice- получить список дешевых отелей\n'
            '/highprice - отели с высокими ценами\n'
            '/bestdeal - лучшие предложения\n'
            '/history - история запросов\n'
            '/settings - настройки\n'),
            'select language': 'выберите язык'},
    'en': {
        'help': (
            '<b>Bot commands</b>\n'
            '/help - List of all commands\n'
            '/lowprice- get a list of cheap hotels\n'
            '/highprice - hotels with high prices\n'
            '/bestdeal- the best offers\n'
            '/history - request history\n'
            '/settings - settings\n'),
        'select language': 'select a language'}}






"""======================settings+++++++++++++++++++++++++"""
# @bot.message_handler(commands=['settings'])
# def settings(message):
#
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item1 = types.InlineKeyboardButton("ru", callback_data='ru')
#     item2 = types.InlineKeyboardButton("en", callback_data='en')
#     markup.add(item1, item2)
#     bot.send_message(message.chat.id, default_language['select language'], reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     try:
#         print(call.message.call)
#         logger.info(f'Изменен язык на {call.message["callback_data"]}')
#         if call.message:
#             set_language(default_language, call.data)
#             bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
#                                       text=f'Язык по умолчанию: {call.data}.')
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text="Выберете язык'",
#                                   reply_markup=None)
#         bot.send_message(call.message.chat.id, default_language['help'], parse_mode='html')
#     except Exception as ex:
#         print(repr(ex))
