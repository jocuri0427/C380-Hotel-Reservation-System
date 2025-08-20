import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QGridLayout, QDateEdit, QMessageBox
)
from PyQt5.QtCore import QDate, Qt


class BookingPage(QWidget):
    def __init__(self, app, user_data, room_data, parent=None):
        super().__init__(parent)
        self.app = app
        self.user_data = user_data
        self.room_data = room_data

        # setting up the window properties
        self.setWindowTitle("Create Booking")
        self.setGeometry(200, 100, 500, 650)
        self.center()
        self.create_ui()

    def center(self):
        # center the window on the screen
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    # UI
    def create_ui(self):
        layout = QVBoxLayout()
        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("Name:"), 0, 0)
        self.name = QLineEdit(self.user_data.get('name', ''))
        self.name.setReadOnly(True)
        form_layout.addWidget(self.name, 0, 1)

        form_layout.addWidget(QLabel("Email:"), 1, 0)
        self.email = QLineEdit(self.user_data.get('email', ''))
        self.email.setReadOnly(True)
        form_layout.addWidget(self.email, 1, 1)

        # Room info (pre-filled from room data)
        form_layout.addWidget(QLabel("Room Type:"), 2, 0)
        self.room_type = QLineEdit(self.room_data.get('room_type', 'Standard'))
        self.room_type.setReadOnly(True)
        form_layout.addWidget(self.room_type, 2, 1)

        form_layout.addWidget(QLabel("Room Number:"), 3, 0)
        self.room_number = QLineEdit(
            str(self.room_data.get('room_number', '')))
        self.room_number.setReadOnly(True)
        form_layout.addWidget(self.room_number, 3, 1)

        form_layout.addWidget(QLabel("Price per Night:"), 4, 0)
        self.price = QLineEdit(f"${self.room_data.get('price', '0')}")
        self.price.setReadOnly(True)
        form_layout.addWidget(self.price, 4, 1)

        # Dates
        form_layout.addWidget(QLabel("Check-in Date:"), 5, 0)

        self.check_in = QDateEdit()

        self.check_in.setCalendarPopup(True)

        self.check_in.setDate(QDate.currentDate())

        form_layout.addWidget(self.check_in, 5, 1)

        form_layout.addWidget(QLabel("Check-out Date:"), 6, 0)

        self.check_out = QDateEdit()

        self.check_out.setCalendarPopup(True)

        self.check_out.setDate(QDate.currentDate().addDays(1))

        form_layout.addWidget(self.check_out, 6, 1)

        # Payment info
        form_layout.addWidget(QLabel("Card Type:"), 7, 0)

        self.card_type = QComboBox()

        self.card_type.addItems(["Visa", "MasterCard", "American Express"])

        form_layout.addWidget(self.card_type, 7, 1)

        form_layout.addWidget(QLabel("Card Number:"), 8, 0)

        self.card_number = QLineEdit()

        form_layout.addWidget(self.card_number, 8, 1)

        form_layout.addWidget(QLabel("Expiration Date (MM/YY):"), 9, 0)

        self.expiration_date = QLineEdit()

        self.expiration_date.setInputMask("99/99")

        form_layout.addWidget(self.expiration_date, 9, 1)

        form_layout.addWidget(QLabel("CVV:"), 10, 0)

        self.cvv = QLineEdit()

        self.cvv.setEchoMode(QLineEdit.Password)

        self.cvv.setMaxLength(4)

        form_layout.addWidget(self.cvv, 10, 1)

        # Create booking submission button
        layout.addLayout(form_layout)

        # Add total price display
        self.total_price = QLabel("Total: $0.00")
        self.total_price.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.total_price)

        # Connect date changes to update total price
        self.check_in.dateChanged.connect(self.update_total_price)
        self.check_out.dateChanged.connect(self.update_total_price)

        self.update_total_price()

        self.submitButton = QPushButton("Confirm Booking")
        self.submitButton.clicked.connect(self.submit_booking)

        layout.addWidget(self.submitButton)

        self.setLayout(layout)

    def update_total_price(self):
        # Calculate number of nights
        check_in = self.check_in.date().toPyDate()
        check_out = self.check_out.date().toPyDate()
        nights = (check_out - check_in).days
        # Update total price
        price_per_night = float(self.room_data.get('price', 0))
        total = price_per_night * nights
        self.total_price.setText(f"Total: ${total:.2f} ({nights} nights)")

    def submit_booking(self):
        # Validate dates
        check_in = self.check_in.date().toPyDate()
        check_out = self.check_out.date().toPyDate()

        if check_out <= check_in:
            QMessageBox.warning(
                self, "Error", "Check-out date must be after check-in date")
            return

        # Validate payment info
        if not all([
            self.card_number.text().strip(),
            self.expiration_date.text().strip(),
            self.cvv.text().strip()
        ]):
            QMessageBox.warning(
                self, "Error", "Please fill in all payment details")
            return

        # Submit booking to backend
        try:
            # Format the request data to match backend expectations
            request_data = {
                'user_id': self.user_data.get('id', ''),
                'room_id': self.room_data.get('id'),
                'check_in': check_in.isoformat(),
                'check_out': check_out.isoformat(),
                'payment': {
                    'card_number': self.card_number.text().strip(),
                    'expiry_date': self.expiration_date.text().strip(),
                    'cvv': self.cvv.text().strip(),
                    'card_type': self.card_type.currentText(),
                    # --- ADD THIS LINE ---
                    'amount': float(self.room_data.get('price', 0)) * (check_out - check_in).days
                }
            }

            response = requests.post(
                'http://127.0.0.1:5000/booking', json=request_data)

            if response.ok:
                booking_data = response.json()
                # Add room type to booking data for display
                booking_data['room_type'] = self.room_data.get(
                    'room_type', 'N/A')

                # Show confirmation page
                from confirmationPlaceholder import ConfirmationPlaceHolder
                self.confirmation_page = ConfirmationPlaceHolder(
                    self.app,
                    self.user_data,
                    booking_data
                )
                self.confirmation_page.show()
                self.close()
            else:
                error_msg = response.json().get('error', 'Failed to create booking')
                QMessageBox.warning(
                    self, "Error", f"Failed to create booking: {error_msg}")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Server error: {str(e)}")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"non server exception: {str(e)}")
