import config
from telebot import types
from config import bot, user_dict
from config import bot
from requests_hotel.hotel_list import get_hotels_list

"""Команда /lowprice
После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3. Необходимость загрузки и вывода фотографий для каждого отеля («Да/Нет»):
a. При положительном ответе пользователь также вводит количество
необходимых фотографий (не больше заранее определённого
максимума).

Для команд lowprice, highprice и bestdeal сообщение с результатом команды должно
содержать краткую информацию по каждому отелю. В эту информацию как минимум
входит:
● название отеля,
● адрес,
● ссылка на страницу с отелем.
● как далеко расположен от центра,
● цена за ночь и суммарную стоимость.
● N фотографий отеля (если пользователь счёл необходимым их вывод).
"""

def get_lowprice_hotel(user_id):
    hotel_list = get_hotels_list(user_dict[user_id].get_querystring_lowprice())
    for hotel in hotel_list.values():
        bot.send_message(user_id, f"""
        <b>Название отеля:</b> {hotel['name hotel']}        
        <b>Адрес:</b> {hotel['address']}
        <b>Звёздность отеля:</b> {hotel['starRating']}
        <b>Рейтинг отеля:</b> {hotel['unformattedRating']}"
        <b>Страницу с отелем:</b> {hotel['site']}"
        <b>Расположение от центра:</b> {hotel['landmarks']}
        <b>Цена за ночь:</b> {hotel['price']}. Суммарная стоимость: пока нет
      """)
        media_group = [types.InputMediaPhoto(media=url) for url in hotel['photo']]
        bot.send_media_group(user_id, media_group)



# bot.send_media_group(message.chat.id, media_group)
# bot = telegram.Bot(token = TOKEN)
# media_group = []
# text = 'some caption for album'
# for num in range(3):
#     media_group.append(InputMediaPhoto(open('img%d.png' % num, 'rb'),
#                                        caption = text if num == 0 else ''))
# bot.send_media_group(chat_id = CHANNEL_ID, media = media_group)