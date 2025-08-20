import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGridLayout, QComboBox, QMessageBox
)


class RegistrationPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("User Registration")
        self.resize(500, 500)
        self.center()
        self.setup_ui()

    def center(self):
        # center the window on the screen
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(20)

        # title
        title = QLabel("Create Your Account")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # form layout
        form_layout = QGridLayout()
        form_layout.setSpacing(15)

        # name field
        name_label = QLabel("Full Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")
        form_layout.addWidget(name_label, 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)

        # email field
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        form_layout.addWidget(email_label, 1, 0)
        form_layout.addWidget(self.email_input, 1, 1)

        # password field
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(password_label, 2, 0)
        form_layout.addWidget(self.password_input, 2, 1)

        # confirm password field
        confirm_password_label = QLabel("Confirm Password:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(confirm_password_label, 3, 0)
        form_layout.addWidget(self.confirm_password_input, 3, 1)

        # ser type
        user_type_label = QLabel("Account Type:")
        self.user_type_combo = QComboBox()
        self.user_type_combo.addItem("User", "user")
        self.user_type_combo.addItem("Manager", "manager")
        form_layout.addWidget(user_type_label, 4, 0)
        form_layout.addWidget(self.user_type_combo, 4, 1)

        main_layout.addLayout(form_layout)

        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.setStyleSheet(
            "background-color: #007BFF; color: white; padding: 10px;")
        self.register_button.clicked.connect(self.handle_registration)
        main_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        # Back to login link
        login_link = QLabel("Back to Login")
        login_link.setStyleSheet(
            "color: darkblue; text-decoration: underline;")
        login_link.setCursor(Qt.PointingHandCursor)
        login_link.mousePressEvent = lambda e: self.show_login()
        main_layout.addWidget(login_link, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def show_login(self):
        # gives some circular import issue if put at the top
        from loginPage import LoginPage
        self.login_window = LoginPage(self.app)
        self.login_window.show()
        self.close()

    def handle_registration(self):
        # set form data
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        user_type = self.user_type_combo.currentData()

        # simple validation
        if not all([name, email, password, self.confirm_password_input.text()]):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        if password != self.confirm_password_input.text():
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        try:
            # prepare registration data
            registration_data = {
                "name": name,
                "email": email,
                "password": password,
                "user_type": user_type
            }

            # make API request
            response = requests.post(
                "http://127.0.0.1:5000/register",
                json=registration_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            # handle response
            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    QMessageBox.warning(
                        self, "Registration Failed", data["error"])
                else:
                    QMessageBox.information(self, "Success",
                                            "Registration successful! Please login with your credentials.")
                    self.show_login()
            else:
                error_msg = response.json().get('error', 'Registration failed. Please try again.')
                QMessageBox.warning(self, "Error", error_msg)

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"server exception: {str(e)}")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"non server exception: {str(e)}")
