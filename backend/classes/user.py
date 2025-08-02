import PaymentMethod


class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.payment_methods = []

    def get_user_details(self):
        user_details = {
            "user.id": self.user_id,
            "name": self.name,
            "email": self.email
        }
        return user_details

    def add_payment_method(self, method):
        self.payment_methods.append(method)

    def remove_payment_method(self, method_id):
        for method in self.payment_methods:
            if method_id == method.method_id:
                self.payment_methods.remove(method)
            break
