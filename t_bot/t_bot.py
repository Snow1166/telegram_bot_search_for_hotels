from config import bot
from t_bot import handlers
from t_bot.command import start_help, hotel_search, history
from telebot.custom_filters import StateFilter
from t_bot import callback_handler

bot.add_custom_filter(StateFilter(bot))



