from datetime import date
from Booking import Booking


class BookingManager:
    def __init__(self):
        self.rooms = []
        self.users = []
        self.bookings = []

    def validate_input(self, start_date: date, end_date: date):
        today = date.today()
        if start_date >= end_date:
            return False
        elif start_date < today:
            return False
        else:
            return True

    def create_booking(self, user_id: int, room_id: int, start_date: date, end_date: date):
        found_user = next(
            (user for user in self.users if user.user_id == user_id), None)
        if found_user is None:
            return False

        found_room = next(
            (room for room in self.rooms if room.room_number == room_id), None)
        if found_room is None:
            return False

        if not self.validate_input(start_date, end_date):
            return False

        if not found_room.is_available(start_date, end_date):
            return False

        number_of_nights = (end_date - start_date).days
        total_price = number_of_nights * found_room.price_per_night

        booking_id = len(self.bookings) + 1
        status = "Confirmed"

        new_booking = Booking(booking_id, found_user, found_room,
                              start_date, end_date, total_price, status)
        self.bookings.append(new_booking)
        found_room.add_booking(new_booking)

        return True

    def cancel_booking(self, booking_id):
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                booking.cancel()
                return True
        return False
