import sys
import requests
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGridLayout, QMessageBox, QDateEdit, QComboBox
)


class ModifyBookingPage(QWidget):
    def __init__(self, app, user_data, booking_data):
        super().__init__()
        self.app = app
        self.user_data = user_data
        self.booking_data = booking_data
        self.setWindowTitle("Modify Booking")
        self.resize(450, 400)
        self.create_ui()
        self.load_room_types()

    def create_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("Modify Your Booking")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)

        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("Confirmation #:"), 0, 0)
        self.confirmation_label = QLineEdit(
            self.booking_data.get('confirmation_number', 'N/A'))
        self.confirmation_label.setReadOnly(True)
        form_layout.addWidget(self.confirmation_label, 0, 1)

        form_layout.addWidget(QLabel("New Room Type:"), 1, 0)
        self.room_type_combo = QComboBox()
        form_layout.addWidget(self.room_type_combo, 1, 1)

        form_layout.addWidget(QLabel("New Check-in:"), 2, 0)
        self.check_in_edit = QDateEdit()
        self.check_in_edit.setCalendarPopup(True)
        self.check_in_edit.setDate(QDate.fromString(
            self.booking_data.get('check_in'), 'yyyy-MM-dd'))
        form_layout.addWidget(self.check_in_edit, 2, 1)

        form_layout.addWidget(QLabel("New Check-out:"), 3, 0)
        self.check_out_edit = QDateEdit()
        self.check_out_edit.setCalendarPopup(True)
        self.check_out_edit.setDate(QDate.fromString(
            self.booking_data.get('check_out'), 'yyyy-MM-dd'))
        form_layout.addWidget(self.check_out_edit, 3, 1)

        layout.addLayout(form_layout)

        self.submit_button = QPushButton("Confirm Changes")
        self.submit_button.setStyleSheet(
            "background-color: #007BFF; color: white; padding: 10px;")
        self.submit_button.clicked.connect(self.handle_modification)
        layout.addWidget(self.submit_button)

        self.back_button = QPushButton("Back to Booking History")
        self.back_button.clicked.connect(self.go_to_booking_history)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_room_types(self):
        try:
            response = requests.get("http://127.0.0.1:5000/rooms")
            if response.ok:
                rooms = response.json()
                room_types = sorted(
                    list(set(room['room_type'] for room in rooms)))
                self.room_type_combo.addItems(room_types)

                current_room_type = self.booking_data.get('room_type')
                if current_room_type in room_types:
                    self.room_type_combo.setCurrentText(current_room_type)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Server Error",
                                 f"Could not load room types: {e}")

    def handle_modification(self):
        new_check_in = self.check_in_edit.date().toString('yyyy-MM-dd')
        new_check_out = self.check_out_edit.date().toString('yyyy-MM-dd')
        confirmation_number = self.booking_data.get('confirmation_number')
        new_room_type = self.room_type_combo.currentText()

        if self.check_in_edit.date() >= self.check_out_edit.date():
            QMessageBox.warning(
                self, "Invalid Dates", "Check-out date must be after the check-in date.")
            return

        payload = {
            "confirmation_number": confirmation_number,
            "new_check_in": new_check_in,
            "new_check_out": new_check_out,
            "new_room_type": new_room_type
        }

        try:
            response = requests.post(
                "http://127.0.0.1:5000/booking/modify", json=payload)
            if response.ok:
                QMessageBox.information(
                    self, "Success", "Your booking has been modified successfully.")
                self.go_to_booking_history()
            else:
                error_msg = response.json().get('error', 'Modification failed.')
                QMessageBox.warning(self, "Error", error_msg)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Server Error",
                                 f"Could not connect to the server: {e}")

    def go_to_booking_history(self):
        from bookingHistoryPage import BookingHistoryPage
        self.history_page = BookingHistoryPage(self.app, self.user_data)
        self.history_page.show()
        self.close()
