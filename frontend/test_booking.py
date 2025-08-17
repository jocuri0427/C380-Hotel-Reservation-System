import sys
from unittest.mock import patch, MagicMock

import pytest
from PyQt5.QtCore import Qt, QDate, QPoint
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

# keeping a global instance to avoid garbage collection
app = None


@pytest.fixture(scope="session")
def test_app():
    global app
    if QApplication.instance() is None:
        app = QApplication(sys.argv)
    return QApplication.instance()


@pytest.fixture
def mock_app():
    class MockApp:
        current_user = {  # Mock user
            'id': 1,
            'name': 'Test Samar',
            'email': 'samar@test.com'
        }

    return MockApp()


@pytest.fixture
def room_data():  # Mock room data
    return {
        'id': 101,
        'room_type': 'Deluxe',
        'price': '200.00',
        'status': 'available'
    }


@pytest.fixture
def booking_page(test_app, mock_app, room_data):
    # Patch QDesktopWidget to avoid needing a real screen
    with patch('PyQt5.QtWidgets.QDesktopWidget') as mock_desktop:
        mock_screen = MagicMock()
        mock_screen.geometry.return_value.center.return_value = QPoint(100, 100)
        mock_desktop.screen.return_value = mock_screen
        mock_desktop.screenGeometry.return_value.center.return_value = QPoint(100, 100)

        from frontend.bookingPage import BookingPage
        page = BookingPage(mock_app, mock_app.current_user, room_data)
        yield page
        page.close()


class TestBookingPage:
    # Testing update_total_price method with different date ranges
    def test_update_total_price(self, booking_page):
        # Set check-in to today
        today = QDate.currentDate()
        booking_page.check_in.setDate(today)

        # Test 1 night stay
        tomorrow = today.addDays(1)
        booking_page.check_out.setDate(tomorrow)
        assert "$200.00 (1 nights)" in booking_page.total_price.text()

        # Test 3 night stay
        three_days = today.addDays(3)
        booking_page.check_out.setDate(three_days)
        assert "$600.00 (3 nights)" in booking_page.total_price.text()

    # Testing validation on submit booking
    def test_submit_booking_validation(self, booking_page):
        # Test invalid date range (check-out before check-in)
        today = QDate.currentDate()
        yesterday = today.addDays(-1)
        booking_page.check_in.setDate(today)
        booking_page.check_out.setDate(yesterday)

        with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning:
            QTest.mouseClick(booking_page.submitButton, Qt.LeftButton)
            mock_warning.assert_called_once()
            args, _ = mock_warning.call_args
            assert args[1] == "Error"
            assert "Check-out date must be after check-in date" in args[2]

        # Test missing payment info
        booking_page.check_out.setDate(today.addDays(1))  # Fix date range
        with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning:
            QTest.mouseClick(booking_page.submitButton, Qt.LeftButton)
            mock_warning.assert_called_once()
            args, _ = mock_warning.call_args
            assert args[1] == "Error"
            assert "Please fill in all payment details" in args[2]

    # Testing successful booking
    def test_successful_booking(self, booking_page):
        # Set valid dates
        today = QDate.currentDate()
        tomorrow = today.addDays(1)
        booking_page.check_in.setDate(today)
        booking_page.check_out.setDate(tomorrow)

        # Fill in payment info
        booking_page.card_number.setText("1234123412341234")
        booking_page.expiration_date.setText("12/25")
        booking_page.cvv.setText("123")
        booking_page.card_type.setCurrentText("Visa")

        # Mock the API response
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {
            'id': 1001,
            'status': 'confirmed',
            'total_price': '200.00',
            'check_in': today.toString(Qt.ISODate),
            'check_out': tomorrow.toString(Qt.ISODate)
        }

        with patch('requests.post', return_value=mock_response) as mock_post, \
                patch('frontend.confirmationPlaceholder.ConfirmationPlaceHolder') as mock_confirm:
            # Click the submit button
            QTest.mouseClick(booking_page.submitButton, Qt.LeftButton)

            # Verify the API was called with correct data
            mock_post.assert_called_once()
            _, kwargs = mock_post.call_args
            request_data = kwargs['json']
            assert request_data['user_id'] == 1
            assert request_data['room_id'] == 101
            assert request_data['payment']['card_type'] == 'Visa'

            # Verify confirmation page was shown
            mock_confirm.assert_called_once()

    # Testing API errors when booking
    def test_booking_api_error(self, booking_page):
        # Set up valid form data
        today = QDate.currentDate()
        booking_page.check_in.setDate(today)
        booking_page.check_out.setDate(today.addDays(1))
        booking_page.card_number.setText("1234123412341234")
        booking_page.expiration_date.setText("12/25")
        booking_page.cvv.setText("123")

        # Mock API error response
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.json.return_value = {'error': 'Room not available'}

        with patch('requests.post', return_value=mock_response), \
                patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning:
            QTest.mouseClick(booking_page.submitButton, Qt.LeftButton)

            # Verify error message was shown
            mock_warning.assert_called_once()
            args, _ = mock_warning.call_args
            assert "Failed to create booking" in args[2]
            assert "Room not available" in args[2]
