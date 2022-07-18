"""Loader"""
from telebot.custom_filters import StateFilter
import t_bot
from config import bot


bot.add_custom_filter(StateFilter(bot))
