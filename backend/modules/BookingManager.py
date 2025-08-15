from datetime import date
from booking import Booking
from exceptions import InvalidDateRangeError, UserNotFoundError, RoomNotFoundError, RoomUnavailableError, BookingNotFoundError


class BookingManager:
    def __init__(self):
        self.rooms = []
        self.users = []
        self.bookings = []

    # validates dates if they don't overlap with each other
    def validate_input(self, start_date: date, end_date: date):
        today = date.today()
        if start_date >= end_date:
            raise InvalidDateRangeError("Start date must be before end date.")
        elif start_date < today:
            raise InvalidDateRangeError("Start date cannot be in the past.")
        else:
            return True

    # create the booking: loops to look for user and room, and if dates are valid, and room is available, creates a booking
    def create_booking(self, user_id: int, room_id: int, start_date: date, end_date: date):
        found_user = next(
            (user for user in self.users if user.user_id == user_id), None)
        if found_user is None:
            raise UserNotFoundError(f"User ID {user_id} not found.")

        found_room = next(
            (room for room in self.rooms if room.room_number == room_id), None)
        if found_room is None:
            raise RoomNotFoundError(f"Room ID {room_id} not found.")

        if not self.validate_input(start_date, end_date):
            return False

        if not found_room.is_available(start_date, end_date):
            raise RoomUnavailableError(
                "Room is not available for the selected dates.")

        number_of_nights = (end_date - start_date).days
        total_price = number_of_nights * found_room.price_per_night

        booking_id = len(self.bookings) + 1
        status = "Confirmed"

        new_booking = Booking(booking_id, found_user, found_room,
                              start_date, end_date, total_price, status)
        self.bookings.append(new_booking)
        found_room.add_booking(new_booking)

        return True

    # cancel the booking: loops to find booking and cancels it
    def cancel_booking(self, booking_id):
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                booking.cancel()
                return True
        raise BookingNotFoundError(f"Booking ID {booking_id} not found.")
