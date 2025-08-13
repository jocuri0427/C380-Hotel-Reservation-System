class HotelSystemError(Exception):
    # base class for all exceptions in the hotel reservation system
    pass


class UserNotFoundError(HotelSystemError):
    # is raised when a user ID is not found in the system
    pass


class RoomNotFoundError(HotelSystemError):
    # is raised when a room ID is not found in the system
    pass


class BookingNotFoundError(HotelSystemError):
    # is raised when a booking ID or confirmation number is not found
    pass


class InvalidDateRangeError(HotelSystemError):
    # is raised when the provided date range is invalid (e.g., end date is before start date)
    pass


class RoomUnavailableError(HotelSystemError):
    # is raised when a room is not available for the requested date range
    pass
