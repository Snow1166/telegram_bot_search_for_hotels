class User:
    """
    Создание класса пользователя для сбора данных опроса
    и возвращения строки запроса дла api отелей
    """
    all_users = dict()

    def __init__(self, user_id: int) -> None:
        self.command = None
        self.destination_id = None
        self.city_search = None
        self.checkin = None
        self.checkout = None
        self.total_day = None
        self.price_min = None
        self.price_max = None
        self.distance = None
        self.total_hotel = None
        self.bool_photo = None
        self.total_photos = None
        self.locale = "ru_RU"
        self.currency = "RUB"
        self.last_message_bot = None
        User.add_user(user_id, self)

    @staticmethod
    def get_user(user_id):
        """
        Принимает id пользователя и проверяет наличия значения в словаре
        В случае отсутствия id пользователя, добавляет его в словарь.
        :param user_id:
        :return: возвращает id пользователя из словаря
        """
        if User.all_users.get(user_id) is None:
            new_user = User(user_id)
            return new_user
        return User.all_users.get(user_id)

    @classmethod
    def add_user(cls, user_id, user):
        """ Создает пользователя в словаре"""
        cls.all_users[user_id] = user

    def get_querystring(self) -> dict:
        """Создание и возвращение строки запроса и
        корректирование его в зависимости от введенной команды пользователя"""
        querystring = {"destinationId": self.destination_id, "pageNumber": "1", "pageSize": "25",
                       "checkIn": self.checkin, "checkOut": self.checkout, "adults1": "1",
                       "sortOrder": "PRICE", "locale": self.locale, "currency": self.currency}

        if self.command == '/lowprice':
            return querystring

        elif self.command == '/highprice':
            querystring['sortOrder'] = "PRICE_HIGHEST_FIRST"
            return querystring

        elif self.command == '/bestdeal':
            querystring['sortOrder'] = 'DISTANCE_FROM_LANDMARK'
            querystring['landmarkIds'] = 'Центр города'
            querystring['priceMin'] = self.price_min
            querystring['priceMax'] = self.price_max
            return querystring

    def get_total_photo(self):
        return int(self.total_photos)

    def get_total_hotels(self):
        return int(self.total_hotel)

    def get_command(self):
        return self.command
