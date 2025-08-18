import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGridLayout, QMessageBox
)

# Import all possible dashboards
from website import Dashboard
from managerDashboardPlaceHolder import ManagerDashboardPlaceHolder


class LoginPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("User Login")
        self.resize(400, 300)
        self.center()
        self.create_ui()

    def center(self):
        # Center the window on the screen
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def create_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Login to Your Account")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Form layout
        form_layout = QGridLayout()
        form_layout.setSpacing(10)

        # Email field
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        form_layout.addWidget(email_label, 0, 0)
        form_layout.addWidget(self.email_input, 0, 1)

        # Password field
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(password_label, 1, 0)
        form_layout.addWidget(self.password_input, 1, 1)

        main_layout.addLayout(form_layout)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet(
            "background-color: #007BFF; color: white; padding: 10px;")
        self.login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        # Registration link
        register_link = QLabel("Create an account")
        register_link.setStyleSheet(
            "color: darkblue; text-decoration: underline;")
        register_link.setCursor(Qt.PointingHandCursor)
        register_link.mousePressEvent = lambda e: self.show_registration()
        main_layout.addWidget(register_link, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def show_registration(self):
        # avoids circular import
        from registrationPage import RegistrationPage
        self.registration_window = RegistrationPage(self.app)
        self.registration_window.show()
        self.close()

    def handle_login(self):
        # Get form data
        email = self.email_input.text().strip()
        password = self.password_input.text()

        # Simple validation
        if not all([email, password]):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        try:
            # Prepare login data
            login_data = {"email": email, "password": password}

            # Make API request
            response = requests.post(
                "http://127.0.0.1:5000/login",
                json=login_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            # Handle response
            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    QMessageBox.warning(self, "Login Failed", data["error"])
                    return

                user_data = {
                    "id": data.get("user_id"),
                    "name": data.get("name", "User"),
                    "email": email,
                    "user_type": data.get("user_type", "user")
                }

                # Save to app
                self.app.current_user = user_data

                # --- MODIFIED: Redirect based on user type ---
                if user_data.get('user_type') == 'manager':
                    self.next_win = ManagerDashboardPlaceHolder(
                        self.app, user_data)
                    self.next_win.show()
                else:
                    self.next_win = Dashboard(self.app, user_data)
                    self.next_win.show()

                self.close()
                # --- END OF MODIFICATION ---

            else:
                QMessageBox.warning(
                    self, "Error",
                    "Login failed. Please check your credentials and try again."
                )

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"server exception: {str(e)}")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"non server exception: {str(e)}")
