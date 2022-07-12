class User:
    def __init__(self):
        self.command = None
        self.destination_id = None
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
        self.last_message = None

    def get_querystring(self):
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
