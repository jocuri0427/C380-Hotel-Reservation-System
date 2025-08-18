from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton, QMessageBox, QTextEdit
)


class ConfirmationPlaceHolder(QWidget):
    def __init__(self, app, user_data, booking_data=None, parent=None):
        super().__init__(parent)
        self.app = app
        self.user_data = user_data
        self.booking_data = booking_data or {}
        self.setWindowTitle("Booking Confirmation")
        self.resize(800, 600)
        self.center()
        self.setup_ui()

    def center(self):
        # Center the window on the screen
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Booking Confirmation")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Confirmation message
        message = QLabel(
            "✅ Your booking is confirmed!\nThank you for choosing us 🙂")
        message.setFont(QFont("Arial", 18))
        message.setAlignment(Qt.AlignCenter)

        # Buttons row
        btn_layout = QHBoxLayout()

        cancel_btn = QPushButton("Cancel Booking")
        cancel_btn.setStyleSheet(
            "background-color: #dc3545; color: white; padding: 10px;")
        cancel_btn.clicked.connect(self.go_to_booking_history)

        modify_btn = QPushButton("Modify Booking")
        modify_btn.setStyleSheet(
            "background-color: #ffc107; color: black; padding: 10px;")
        # CORRECTED THIS LINE
        modify_btn.clicked.connect(self.go_to_booking_history)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(modify_btn)

        # Add widgets to layout
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(message)
        layout.addSpacing(30)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def go_to_booking_history(self):
        from bookingHistoryPage import BookingHistoryPage
        self.booking_history = BookingHistoryPage(self.app, self.user_data)
        self.booking_history.show()
        self.close()
