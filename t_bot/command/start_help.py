from config import bot, user_dict
from database.users import User


@bot.message_handler(commands=['start', 'help'])
def command_start(message):
    # bot.send_sticker(message.chat.id, 'CAADAgADsQADWQMDAAEJK1niI56hlhYE')
    user_dict[message.from_user.id] = User()
    welcome = open('images/logo.jpg', 'rb')
    bot.send_photo(message.chat.id, welcome, caption=(
        """
<b>Команды бота</b>
/lowprice- список недорогих отелей
/highprice - отели с высокими ценами
/bestdeal - лучшие предложения
/history - история запросов
/settings - настройки
        """))
