from config import bot
from t_bot import hendlers
from t_bot.command import start_help, lowprice, highprice, bestdeal, settings
from telebot.custom_filters import StateFilter
from t_bot import callback_handler

bot.add_custom_filter(StateFilter(bot))



