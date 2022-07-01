from config import bot


@bot.message_handler(commands=['start', 'help'])
def command_start(message):
    welcome = open('images/logo.jpg', 'rb')
    bot.send_photo(message.chat.id, welcome, caption=(
        '<b>Команды бота</b>\n'
        '/lowprice- список недорогих отелей\n'
        '/highprice - отели с высокими ценами\n'
        '/bestdeal - лучшие предложения\n'
        '/history - история запросов\n'
        '/settings - настройки\n'))