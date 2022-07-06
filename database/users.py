class User:
    def __init__(self):
        self.command = None
        self.destinationId = None
        self.checkIn = None
        self.checkOut = None
        self.price_min = None
        self.price_high = None
        self.distance = None
        self.total_hotel = None
        self.total_photos = None
        self.locale = "ru-RU"
        self.currency = "RUB"

    def get_querystring_lowprice(self):
        querystring = {"destinationId": {self.destinationId}, "pageNumber": "1", "pageSize": "25",
                       "checkIn": {self.checkIn}, "checkOut": {self.checkOut}, "adults1": "1",
                       "sortOrder": "PRICE", "locale": {self.locale}, "currency": {self.currency}}
        return querystring

    def get_querystring_highprice(self):
        querystring = {"destinationId": {self.destinationId}, "pageNumber": "1", "pageSize": "25",
                       "checkIn": {self.checkIn}, "checkOut": {self.checkOut}, "adults1": "1",
                       "sortOrder": "PRICE_HIGHEST_FIRST", "locale": {self.locale}, "currency": {self.currency}}
        return querystring

    def get_querystring_bestdeal(self):
        querystring = {"destinationId": {self.destinationId}, "pageNumber": "1", "pageSize": "25",
                       "checkIn": {self.checkIn}, "checkOut": {self.checkOut}, "adults1": "1",
                       "priceMin": {self.price_min}, "priceMax": {self.price_high},
                       "sortOrder": "PRICE", "locale": {self.locale}, "currency": {self.currency}}
        return querystring

    def get_total_photo(self):
        return int(self.total_photos)

    def get_total_hotels(self):
        return int(self.total_hotel)
