import PaymentMethod


class User:
    # user details
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.payment_methods = []

    # getter method to call
    def get_user_details(self):
        user_details = {
            "user.id": self.user_id,
            "name": self.name,
            "email": self.email
        }
        return user_details

    # add new payment method to list of payment methods
    def add_payment_method(self, method_id, card_type, card_number, expiration_date):
        new_method = PaymentMethod.PaymentMethod(
            method_id, card_type, card_number, expiration_date)
        self.payment_methods.append(new_method)

    # remove new payment method to list of payment methods: search and match payment info to remove
    def remove_payment_method(self, method_id):
        for method in self.payment_methods:
            if method_id == method.method_id:
                self.payment_methods.remove(method)
            break
