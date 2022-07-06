from config import bot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date

@bot.message_handler(commands=['settings'])
def start(m):
    calendar, step = DetailedTelegramCalendar(min_date=date.today(), locale="ru", calendar_id='checkIn').build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar().func(calendar_id='checkIn'))
def cal(c):
    result, key, step = DetailedTelegramCalendar(min_date=date.today(), calendar_id='checkIn').process(c.data)
    print(result)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)