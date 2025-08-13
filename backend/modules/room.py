from datetime import date


class Room:
    # room details-- room number, type, price
    def __init__(self, room_number, room_type, price_per_night):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.bookings = []

    # getter method to call
    def get_room_details(self):
        details = {
            "room_number": self.room_number,
            "room_type": self.room_type,
            "price_per_night": self.price_per_night
        }

        return details

    def add_booking(self, booking):
        self.bookings.append(booking)

    # loop to see if date is available
    def is_available(self, start_date: date, end_date: date):
        for booking in self.bookings:
            if start_date < booking.end_date and end_date > booking.start_date:
                return False
        return True
