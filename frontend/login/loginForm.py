import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Login")
        self.setGeometry(200, 100, 400, 200)
        self.create_ui()

    def create_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Login to Your Account")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)

        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("Email:"), 0, 0)
        self.email = QLineEdit()
        form_layout.addWidget(self.email, 0, 1)

        form_layout.addWidget(QLabel("Password:"), 1, 0)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password, 1, 1)

        main_layout.addLayout(form_layout)

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px;")
        main_layout.addWidget(self.login_button)

        self.forgot_password_label = QLabel("Forgot Password?")
        self.forgot_password_label.setAlignment(Qt.AlignCenter)
        self.forgot_password_label.setStyleSheet("color: #007BFF;")
        self.forgot_password_label.setCursor(Qt.PointingHandCursor)
        main_layout.addWidget(self.forgot_password_label)

        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginForm()
    window.show()
    sys.exit(app.exec_())
