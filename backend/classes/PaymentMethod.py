class PaymentMethod:
    def __init__(self, method_id, card_type, card_number, expiration_date):
        self.method_id = method_id
        self.card_type = card_type
        self.card_number = card_number
        self.expiration_date = expiration_date
