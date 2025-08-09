import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QGridLayout, QDateEdit
)
from PyQt5.QtCore import QDate

class BookingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Booking")
        self.setGeometry(200, 100, 400, 300)
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout()
        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("Name:"), 0, 0)
        self.name = QLineEdit()
        form_layout.addWidget(self.name, 0, 1)

        form_layout.addWidget(QLabel("Email:"), 1, 0)
        self.email = QLineEdit()
        form_layout.addWidget(self.email, 1, 1)

        form_layout.addWidget(QLabel("Room ID:"), 2, 0)
        self.room_id = QLineEdit()
        form_layout.addWidget(self.room_id, 2, 1)

        form_layout.addWidget(QLabel("Check-in Date:"), 3, 0)
        self.check_in = QDateEdit()
        self.check_in.setCalendarPopup(True)
        self.check_in.setDate(QDate.currentDate())
        form_layout.addWidget(self.check_in, 3, 1)

        form_layout.addWidget(QLabel("Check-out Date:"), 4, 0)
        self.check_out = QDateEdit()
        self.check_out.setCalendarPopup(True)
        self.check_out.setDate(QDate.currentDate().addDays(1))
        form_layout.addWidget(self.check_out, 4, 1)

        layout.addLayout(form_layout)

        self.submitButton = QPushButton("Create Booking")
        layout.addWidget(self.submitButton)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    booking_form = BookingForm()
    booking_form.show()
    sys.exit(app.exec_())
