from config import bot
from t_bot.command.func_for_command import find_location


@bot.message_handler(commands=['lowprice'])
def command_lowprice(message):
    find_location(message)

