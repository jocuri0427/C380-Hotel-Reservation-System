from datetime import date
from room import Room
from user import User


class Booking:
    # constructor for booking details
    def __init__(self, booking_id, user: User, room: Room, start_date: date, end_date: date, total_cost, status):
        self.booking_id = booking_id
        self.user = user
        self.room = room
        self.start_date = start_date
        self.end_date = end_date
        self.total_cost = total_cost
        self.status = status

    # calculate booking cost: calculates total cost based on room price and number of nights
    def calculate_total_cost(self):
        number_of_nights = (self.end_date - self.start_date).days
        price = self.room.price_per_night * number_of_nights
        return price

    # change status to cancelled
    def cancel(self):
        self.status = "Cancelled"
