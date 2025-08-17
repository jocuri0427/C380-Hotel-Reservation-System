import unittest
from datetime import date, timedelta
from unittest.mock import MagicMock, PropertyMock

# Assuming BookingManager is in a file named BookingManager.py
from BookingManager import BookingManager, InvalidDateRangeError, UserNotFoundError, RoomNotFoundError, RoomUnavailableError, BookingNotFoundError

# --- Mock Objects ---
# Since we don't have the actual User, Room, and Booking classes,
# we'll create simple mock classes for testing purposes.


class MockUser:
    def __init__(self, user_id):
        self.user_id = user_id


class MockRoom:
    def __init__(self, room_number, price_per_night):
        self.room_number = room_number
        self.price_per_night = price_per_night
        self.bookings = []

    def is_available(self, start_date, end_date):
        # Simple availability check for testing
        for booking in self.bookings:
            if not (end_date <= booking.start_date or start_date >= booking.end_date):
                return False
        return True

    def add_booking(self, booking):
        self.bookings.append(booking)

    def remove_booking(self, booking):
        self.bookings.remove(booking)


class MockBooking:
    def __init__(self, booking_id, user, room, start_date, end_date, total_price, status="Confirmed"):
        self.booking_id = booking_id
        self.user = user
        self.room = room
        self.start_date = start_date
        self.end_date = end_date
        self.total_cost = total_price
        self.status = status

    def cancel(self):
        self.status = "Cancelled"


class TestBookingManager(unittest.TestCase):

    def setUp(self):
        """Set up a new BookingManager and mock data for each test."""
        self.manager = BookingManager()

        # Mock dependencies that are not part of BookingManager
        # This makes our tests focused only on BookingManager's logic
        self.user1 = MockUser(user_id=1)
        self.room1 = MockRoom(room_number=101, price_per_night=150)
        self.room2 = MockRoom(room_number=102, price_per_night=200)

        self.manager.users = [self.user1]
        self.manager.rooms = [self.room1, self.room2]

        # Replace the real Booking class with our mock for consistent testing
        self.manager.bookings.append = lambda b: super(type(self.manager.bookings), self.manager.bookings).append(
            MockBooking(b.booking_id, b.user, b.room, b.start_date,
                        b.end_date, b.total_cost, b.status)
        )

    def test_create_booking_success(self):
        """Test successful creation of a booking."""
        start = date.today() + timedelta(days=10)
        end = date.today() + timedelta(days=15)

        result = self.manager.create_booking(1, 101, start, end)

        self.assertTrue(result)
        self.assertEqual(len(self.manager.bookings), 1)
        self.assertEqual(self.manager.bookings[0].room.room_number, 101)
        self.assertEqual(self.manager.bookings[0].user.user_id, 1)
        # 5 nights * 150 per night
        self.assertEqual(self.manager.bookings[0].total_cost, 5 * 150)

    def test_create_booking_user_not_found(self):
        """Test booking creation fails if user ID does not exist."""
        start = date.today() + timedelta(days=10)
        end = date.today() + timedelta(days=15)

        with self.assertRaises(UserNotFoundError):
            self.manager.create_booking(99, 101, start, end)

    def test_create_booking_room_not_found(self):
        """Test booking creation fails if room ID does not exist."""
        start = date.today() + timedelta(days=10)
        end = date.today() + timedelta(days=15)

        with self.assertRaises(RoomNotFoundError):
            self.manager.create_booking(1, 999, start, end)

    def test_create_booking_invalid_date_range(self):
        """Test booking creation fails if start date is after end date."""
        start = date.today() + timedelta(days=15)
        end = date.today() + timedelta(days=10)

        with self.assertRaises(InvalidDateRangeError):
            self.manager.create_booking(1, 101, start, end)

    def test_create_booking_past_date(self):
        """Test booking creation fails if start date is in the past."""
        start = date.today() - timedelta(days=1)
        end = date.today() + timedelta(days=5)

        with self.assertRaises(InvalidDateRangeError):
            self.manager.create_booking(1, 101, start, end)

    def test_create_booking_room_unavailable(self):
        """Test booking creation fails if the room is already booked for the dates."""
        start1 = date.today() + timedelta(days=20)
        end1 = date.today() + timedelta(days=25)

        # First booking should succeed
        self.manager.create_booking(1, 101, start1, end1)

        # Second booking attempt for overlapping dates should fail
        start2 = date.today() + timedelta(days=22)
        end2 = date.today() + timedelta(days=27)

        with self.assertRaises(RoomUnavailableError):
            self.manager.create_booking(1, 101, start2, end2)

    def test_cancel_booking_success(self):
        """Test successful cancellation of an existing booking."""
        start = date.today() + timedelta(days=30)
        end = date.today() + timedelta(days=35)
        self.manager.create_booking(1, 101, start, end)

        booking_id = self.manager.bookings[0].booking_id
        result = self.manager.cancel_booking(booking_id)

        self.assertTrue(result)
        self.assertEqual(self.manager.bookings[0].status, "Cancelled")

    def test_cancel_booking_not_found(self):
        """Test cancelling a booking that does not exist."""
        with self.assertRaises(BookingNotFoundError):
            self.manager.cancel_booking(999)

    def test_modify_booking_success(self):
        """Test successful modification of a booking."""
        # Create an initial booking
        start1 = date.today() + timedelta(days=40)
        end1 = date.today() + timedelta(days=45)
        self.manager.create_booking(1, 101, start1, end1)
        booking_to_modify = self.manager.bookings[0]

        # New details for modification
        new_room_id = 102
        new_start = date.today() + timedelta(days=50)
        new_end = date.today() + timedelta(days=52)

        result = self.manager.modify_booking(
            booking_to_modify.booking_id, new_room_id, new_start, new_end)

        self.assertTrue(result)
        # Check that the booking details were updated
        self.assertEqual(booking_to_modify.room.room_number, new_room_id)
        self.assertEqual(booking_to_modify.start_date, new_start)
        self.assertEqual(booking_to_modify.end_date, new_end)
        self.assertEqual(booking_to_modify.total_cost, 2 *
                         200)  # 2 nights * 200 per night
        # Check that the booking was moved from the old room to the new one
        self.assertNotIn(booking_to_modify, self.room1.bookings)
        self.assertIn(booking_to_modify, self.room2.bookings)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
