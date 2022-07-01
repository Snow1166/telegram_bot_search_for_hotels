from config import bot
from t_bot.command.func_for_command import find_location


@bot.message_handler(commands=['bestdeal'])
def command_bestdeal(message):
    find_location(message)
