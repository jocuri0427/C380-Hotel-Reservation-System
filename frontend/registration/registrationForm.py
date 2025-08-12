import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
#RegistrationForm class
class RegistrationForm(QWidget):
    #Constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Registration")
        self.setGeometry(200, 100, 400, 250)
        self.create_ui()

    #creating the UI
    def create_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        #creating the title
        self.title = QLabel("Create Your Account")

        self.title.setFont(QFont("Arial", 20))

        self.title.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(self.title)

        form_layout = QGridLayout()

        #User info
        form_layout.addWidget(QLabel("Name:"), 0, 0)

        self.name = QLineEdit()

        form_layout.addWidget(self.name, 0, 1)

        form_layout.addWidget(QLabel("Email:"), 1, 0)

        self.email = QLineEdit()

        form_layout.addWidget(self.email, 1, 1)

        #User pass
        form_layout.addWidget(QLabel("Password:"), 2, 0)

        self.password = QLineEdit()

        self.password.setEchoMode(QLineEdit.Password)

        form_layout.addWidget(self.password, 2, 1)

        form_layout.addWidget(QLabel("Confirm Password:"), 3, 0)

        self.confirm_password = QLineEdit()

        self.confirm_password.setEchoMode(QLineEdit.Password)

        form_layout.addWidget(self.confirm_password, 3, 1)

        main_layout.addLayout(form_layout)

        #Registration button
        self.register_button = QPushButton("Register")

        self.register_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px;")

        main_layout.addWidget(self.register_button)

        self.setLayout(main_layout)

#Only when the app is ran directly start the app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec_())
