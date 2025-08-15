import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGridLayout, QComboBox, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class RegistrationForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Registration")
        self.setGeometry(200, 100, 400, 300)
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Title
        self.title = QLabel("Create Your Account")
        self.title.setFont(QFont("Arial", 20))
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        # Form layout
        form_layout = QGridLayout()

        # Name field
        form_layout.addWidget(QLabel("Name:"), 0, 0)
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_input, 0, 1)

        # Email field
        form_layout.addWidget(QLabel("Email:"), 1, 0)
        self.email_input = QLineEdit()
        form_layout.addWidget(self.email_input, 1, 1)

        # User type selection
        form_layout.addWidget(QLabel("Account Type:"), 2, 0)
        self.user_type_combo = QComboBox()
        self.user_type_combo.addItem("User", "user")
        self.user_type_combo.addItem("Manager", "manager")
        form_layout.addWidget(self.user_type_combo, 2, 1)

        # Password field
        form_layout.addWidget(QLabel("Password:"), 3, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_input, 3, 1)

        # Confirm Password field
        form_layout.addWidget(QLabel("Confirm Password:"), 4, 0)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.confirm_password_input, 4, 1)

        main_layout.addLayout(form_layout)

        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px;")
        self.register_button.clicked.connect(self.handle_registration)
        main_layout.addWidget(self.register_button)

        self.setLayout(main_layout)
    
    def handle_registration(self):
        # Get form data
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        user_type = self.user_type_combo.currentData()

        # Simple validation
        if not all([name, email, password, confirm_password]):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return
            
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        try:
            # Prepare registration data
            registration_data = {
                "name": name,
                "email": email,
                "password": password,
                "user_type": user_type
            }

            # Print debug info
            print("Sending registration request to:", "http://127.0.0.1:5000/register")
            print("Data being sent:", registration_data)

            # Make API request with timeout and headers
            response = requests.post(
                "http://127.0.0.1:5000/register",
                json=registration_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            # Print response details for debugging
            print("Status code:", response.status_code)
            print("Response content:", response.text)
            
            # Try to parse JSON only if there's content
            response_data = {}
            if response.text.strip():
                try:
                    response_data = response.json()
                except ValueError as e:
                    print("Failed to parse JSON response:", e)
                    QMessageBox.critical(
                        self, 
                        "Server Error", 
                        f"Invalid response from server. Status: {response.status_code}\n{response.text}"
                    )
                    return
            
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Registration successful!")
                # self.close()
            else:
                error_msg = response_data.get('error', f'Registration failed with status {response.status_code}')
                QMessageBox.warning(self, "Error", error_msg)
                
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self, 
                "Connection Error", 
                f"Could not connect to the server.\n\nError: {str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"An unexpected error occurred:\n\n{str(e)}\n\nPlease check the console for more details."
            )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec_())
