import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QGridLayout, QDateEdit
)
from PyQt5.QtCore import QDate

#BookingForm class
class BookingForm(QWidget):
    #Constructor
    def __init__(self):
        super().__init__()
        #setting up the window properties
        self.setWindowTitle("Create Booking")
        self.setGeometry(200, 100, 400, 350)
        self.create_ui()

    #Creating the UI
    def create_ui(self):
        layout = QVBoxLayout()
        form_layout = QGridLayout()

        #Guest info
        form_layout.addWidget(QLabel("Name:"), 0, 0)

        self.name = QLineEdit()

        form_layout.addWidget(self.name, 0, 1)

        form_layout.addWidget(QLabel("Email:"), 1, 0)

        self.email = QLineEdit()

        form_layout.addWidget(self.email, 1, 1)

        #Room info
        form_layout.addWidget(QLabel("Room ID:"), 2, 0)

        self.room_id = QLineEdit()

        form_layout.addWidget(self.room_id, 2, 1)

        #Dates
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

        #Payment info
        form_layout.addWidget(QLabel("Card Type:"), 5, 0)

        self.card_type = QComboBox()

        self.card_type.addItems(["Visa", "MasterCard", "American Express"])

        form_layout.addWidget(self.card_type, 5, 1)

        form_layout.addWidget(QLabel("Card Number:"), 6, 0)

        self.card_number = QLineEdit()

        form_layout.addWidget(self.card_number, 6, 1)

        form_layout.addWidget(QLabel("Expiration Date (MM/YY):"), 7, 0)

        self.expiration_date = QLineEdit()

        self.expiration_date.setInputMask("99/99")

        form_layout.addWidget(self.expiration_date, 7, 1)

        form_layout.addWidget(QLabel("CVV:"), 8, 0)

        self.cvv = QLineEdit()

        self.cvv.setEchoMode(QLineEdit.Password)

        self.cvv.setMaxLength(4)

        form_layout.addWidget(self.cvv, 8, 1)

        #create booking submition button
        layout.addLayout(form_layout)

        self.submitButton = QPushButton("Create Booking")

        layout.addWidget(self.submitButton)

        self.setLayout(layout)

#If ran directly execute the app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    booking_form = BookingForm()
    booking_form.show()
    sys.exit(app.exec_())
