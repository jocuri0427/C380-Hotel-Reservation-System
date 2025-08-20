import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)


class CancelBookingPage(QWidget):
    def __init__(self, app, user_data, confirmation_number=None):
        super().__init__()
        self.app = app
        self.user_data = user_data
        self.setWindowTitle("Cancel Booking")
        self.resize(400, 250)
        self.create_ui(confirmation_number)

    def create_ui(self, confirmation_number):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        # Title
        title = QLabel("Cancel Your Booking")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Instruction Label
        instruction_label = QLabel(
            "Please enter the confirmation number of the booking you wish to cancel.")
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setWordWrap(True)
        layout.addWidget(instruction_label)

        # Confirmation Number Input
        self.confirmation_input = QLineEdit()
        self.confirmation_input.setPlaceholderText("e.g., CON-ABC1234")
        if confirmation_number:
            self.confirmation_input.setText(confirmation_number)
        layout.addWidget(self.confirmation_input)

        # Cancel Button
        self.cancel_button = QPushButton("Confirm Cancellation")
        self.cancel_button.setStyleSheet(
            "background-color: #dc3545; color: white; padding: 10px;")
        self.cancel_button.clicked.connect(self.handle_cancellation)
        layout.addWidget(self.cancel_button)

        # Back Button
        self.back_button = QPushButton("Back to Dashboard")
        self.back_button.clicked.connect(self.go_back_to_dashboard)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def handle_cancellation(self):
        confirmation_number = self.confirmation_input.text().strip()
        if not confirmation_number:
            QMessageBox.warning(
                self, "Error", "Please enter a confirmation number.")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/booking/cancel",
                json={"confirmation_number": confirmation_number},
                headers={"Content-Type": "application/json"}
            )

            if response.ok:
                QMessageBox.information(
                    self, "Success", "Your booking has been successfully cancelled.")
                self.go_back_to_dashboard()
            else:
                error_msg = response.json().get('error', 'Failed to cancel booking.')
                QMessageBox.warning(self, "Cancellation Failed", error_msg)

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Server Error",
                                 f"Could not connect to the server: {e}")

    def go_back_to_dashboard(self):
        from website import Dashboard
        self.dashboard = Dashboard(self.app, self.user_data)
        self.dashboard.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # dummy data for testing
    dummy_user = {"id": 1, "name": "Test User", "email": "test@example.com"}
    window = CancelBookingPage(app, dummy_user)
    window.show()
    sys.exit(app.exec_())
