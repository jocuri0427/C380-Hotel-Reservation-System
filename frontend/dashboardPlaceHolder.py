import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QApplication, QPushButton, QMessageBox
)

from frontend.bookingPage import BookingPage


class DashboardPlaceHolder(QWidget):
    def __init__(self, app, user_data):
        super().__init__()
        self.app = app
        self.user_data = user_data
        self.setWindowTitle("Dashboard")
        self.resize(800, 600)
        self.center()
        self.create_ui()

    def center(self):
        # Center the window on the screen
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def create_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Dashboard")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Placeholder text
        placeholder = QLabel("Placeholder for Dashboard - Pending Tochi's Implementation")
        placeholder.setFont(QFont("Arial", 16))
        placeholder.setAlignment(Qt.AlignCenter)

        # User info
        user_info = QLabel(
            f"Logged in as user: {self.user_data.get('name', 'User')} ({self.user_data.get('email', 'N/A')}) "
        )
        user_info.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(placeholder)
        layout.addSpacing(30)
        # Add Book Room button
        book_button = QPushButton("Book a Room")
        book_button.clicked.connect(self.open_booking_form)
        
        # Booking History button
        history_button = QPushButton("Booking History")

        history_button.clicked.connect(self.open_booking_history)

        
        # Add widgets to main layout
        layout.addWidget(book_button)
        layout.addWidget(history_button)
        layout.addWidget(user_info)
        layout.addWidget(book_button)
        self.setLayout(layout)

        # Fetch rooms from backend
        self.fetch_rooms()

    def fetch_rooms(self):
        try:
            response = requests.get('http://127.0.0.1:5000/rooms', timeout=10)
            if response.status_code == 200:
                rooms = response.json()
                if rooms:
                    self.room_data = rooms[0]  # Store first available room
        except requests.RequestException as e:
            QMessageBox.warning(self, "Error", f"Failed to fetch rooms data: {str(e)}")

    def open_booking_form(self):
        if not self.room_data:
            QMessageBox.warning(self, "Error", "No rooms available")
            return

        self.booking_form = BookingPage(self.app, self.user_data, self.room_data)
        self.booking_form.show()
        
    def open_booking_history(self):
        from bookingHistoryPage import BookingHistoryPage
        self.booking_history = BookingHistoryPage(self.app, self.user_data)
        self.booking_history.show()
        self.close()
