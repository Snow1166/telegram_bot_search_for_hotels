from config import bot


@bot.message_handler(commands=['start', 'help'])
def command_start(message):
    welcome = open('images/logo.jpg', 'rb')
    bot.send_photo(message.chat.id, welcome, caption=(
        """<b>Команды бота</b>
                /lowprice- список недорогих отелей
                /highprice - отели с высокими ценами
                /bestdeal - лучшие предложения
                /history - история запросов
                /settings - настройки
        """))
