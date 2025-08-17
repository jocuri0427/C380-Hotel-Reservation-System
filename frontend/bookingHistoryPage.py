import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QMessageBox
)


class BookingHistoryPage(QWidget):
    def __init__(self, app, user_data, parent=None):
        super().__init__(parent)
        self.app = app
        self.user_data = user_data
        self.setWindowTitle("Booking History")
        self.resize(800, 500)
        self.setup_ui()
        self.load_bookings()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("My Bookings")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Back button
        self.back_btn = QPushButton("Back to Dashboard")
        self.back_btn.clicked.connect(self.on_back_to_dashboard)

        # Bookings table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Room Type", "Check-in", "Check-out", "Price PerNight", "Status"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Add widgets to layout
        layout.addWidget(self.back_btn)
        layout.addWidget(self.history_table)

        self.setLayout(layout)

    def load_bookings(self):
        try:
            response = requests.get(
                f"http://127.0.0.1:5000/bookings/user/{self.user_data['id']}",
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if response.status_code == 200:
                bookings = response.json()
                self.display_bookings(bookings)
            else:
                error_msg = response.json().get('error', 'Failed to load bookings')
                QMessageBox.warning(self, "Error", f"Failed to load bookings: {error_msg}")

        except requests.exceptions as e:
            QMessageBox.critical(self, "Error", f"server exception: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"non server exception: {str(e)}")

    def display_bookings(self, bookings):
        self.history_table.setRowCount(len(bookings))

        for row, booking in enumerate(bookings):
            self.history_table.setItem(row, 0, QTableWidgetItem(booking.get('room_type', 'N/A')))
            self.history_table.setItem(row, 1, QTableWidgetItem(booking.get('check_in', 'N/A')))
            self.history_table.setItem(row, 2, QTableWidgetItem(booking.get('check_out', 'N/A')))
            self.history_table.setItem(row, 3, QTableWidgetItem(f"${booking.get('price_per_night', '0')}"))
            status_item = QTableWidgetItem(booking.get('status', 'N/A'))
            self.history_table.setItem(row, 4, status_item)

    def on_back_to_dashboard(self):
        from dashboardPlaceHolder import DashboardPlaceHolder
        self.dashboard = DashboardPlaceHolder(self.app, self.user_data)
        self.dashboard.show()
        self.close()
