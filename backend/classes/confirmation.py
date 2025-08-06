class Confirmation:
    def __init__(self, confirmation_number, booking_details):
        self.confirmation_number = confirmation_number
        self.booking_details = booking_details

    def get_summary(self):
        return self.confirmation_number + "\n" + self.booking_details
