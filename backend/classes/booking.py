from datetime import date
import Room
import User


class Booking:
    def __init__(self, booking_id, user: User, room: Room, start_date: date, end_date: date, total_cost, status):
        self.booking_id = booking_id
        self.user = user
        self.room = room
        self.start_date = start_date
        self.end_date = end_date
        self.total_cost = total_cost
        self.status = status

    def calculate_total_cost(self):
        number_of_nights = (self.end_date - self.start_date).days
        price = self.room.price_per_night * number_of_nights
        return price

    def cancel(self):
        self.status = "Cancelled"
