import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QMessageBox, QHBoxLayout
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

        title = QLabel("My Bookings")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.back_btn = QPushButton("Back to Dashboard")
        self.back_btn.clicked.connect(self.on_back_to_dashboard)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(
            ["Room Type", "Check-in", "Check-out", "Price PerNight", "Status", "Action"])
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # CORRECTED RESIZING LOGIC
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch) # Room Type
        # Let the other columns, including Action, resize to their content
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

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
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"server exception: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"non server exception: {str(e)}")

    def display_bookings(self, bookings):
        self.history_table.setRowCount(len(bookings))

        for row, booking in enumerate(bookings):
            self.history_table.setItem(row, 0, QTableWidgetItem(booking.get('room_type', 'N/A')))
            self.history_table.setItem(row, 1, QTableWidgetItem(booking.get('check_in', 'N/A')))
            self.history_table.setItem(row, 2, QTableWidgetItem(booking.get('check_out', 'N/A')))
            # MODIFIED: Formatted the price to always show two decimal places
            price_per_night = booking.get('price_per_night', 0)
            self.history_table.setItem(row, 3, QTableWidgetItem(f"${price_per_night:.2f}"))
            self.history_table.setItem(row, 4, QTableWidgetItem(booking.get('status', 'N/A')))

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            confirmation_number = booking.get('confirmation_number')
            if booking.get('status', '').lower() == 'confirmed':
                # Modify Button
                modify_btn = QPushButton("Modify")
                modify_btn.setMinimumWidth(80) # SET MINIMUM BUTTON WIDTH
                modify_btn.clicked.connect(lambda _, b=booking: self.open_modify_page(b))
                action_layout.addWidget(modify_btn)

                # Cancel Button
                cancel_btn = QPushButton("Cancel")
                cancel_btn.setMinimumWidth(80) # SET MINIMUM BUTTON WIDTH
                cancel_btn.clicked.connect(lambda _, cn=confirmation_number: self.open_cancel_page(cn))
                action_layout.addWidget(cancel_btn)

            self.history_table.setCellWidget(row, 5, action_widget)

    def open_cancel_page(self, confirmation_number):
        from cancelBookingPage import CancelBookingPage
        self.cancel_page = CancelBookingPage(self.app, self.user_data, confirmation_number)
        self.cancel_page.show()
        self.close()

    def open_modify_page(self, booking_data):
        from modifyBookingPage import ModifyBookingPage
        self.modify_page = ModifyBookingPage(self.app, self.user_data, booking_data)
        self.modify_page.show()
        self.close()

    def on_back_to_dashboard(self):
        from website import Dashboard
        self.dashboard = Dashboard(self.app, self.user_data)
        self.dashboard.show()
        self.close()
