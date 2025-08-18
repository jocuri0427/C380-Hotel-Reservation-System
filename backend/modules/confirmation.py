import string
import random


class Confirmation:
    def __init__(self, confirmation_number, booking_details):
        self.confirmation_number = confirmation_number
        self.booking_details = booking_details

    def get_summary(self):
        return self.confirmation_number + "\n" + self.booking_details

    @staticmethod  # generate a confirmation num
    def gen_confirmation_number():
        return "CON-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
