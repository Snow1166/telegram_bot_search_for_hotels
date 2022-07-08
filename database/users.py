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
        self.total_photos = None
        self.locale = "ru_RU"
        self.currency = "RUB"

    def get_querystring(self):
        if self.command == '/lowprice':
            querystring = {"destinationId": self.destination_id, "pageNumber": "1", "pageSize": "25",
                           "checkIn": self.checkin, "checkOut": self.checkout, "adults1": "1",
                           "sortOrder": "PRICE", "locale": self.locale, "currency": self.currency}
            return querystring

        elif self.command == '/highprice':
            querystring = {"destinationId": self.destination_id, "pageNumber": "1", "pageSize": "25",
                           "checkIn": self.checkin, "checkOut": self.checkout, "adults1": "1",
                           "sortOrder": "PRICE_HIGHEST_FIRST", "locale": self.locale, "currency": self.currency}
            return querystring

        elif self.command == '/bestdeal':
            querystring = {"destinationId": self.destination_id, "pageNumber": "1", "pageSize": "25",
                           "checkIn": self.checkin, "checkOut": self.checkout, "adults1": "1",
                           "priceMin": self.price_min, "priceMax": self.price_max,
                           "sortOrder": "DISTANCE_FROM_LANDMARK", "landmarkIds": "Центр города",
                           "locale": self.locale, "currency": self.currency}
            return querystring

    def get_total_photo(self):
        return int(self.total_photos)

    def get_total_hotels(self):
        return int(self.total_hotel)

    def get_command(self):
        return self.command
