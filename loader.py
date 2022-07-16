from config import bot
from telebot.custom_filters import StateFilter
import t_bot


bot.add_custom_filter(StateFilter(bot))
