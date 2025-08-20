import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton, QMessageBox, QTextEdit
)


class ManagerDashboardPlaceHolder(QWidget):
    def __init__(self, app, user_data):
        super().__init__()
        self.app = app
        self.user_data = user_data
        self.setWindowTitle("Manager Dashboard")
        self.resize(800, 600)
        self.center()
        self.create_ui()

    def center(self):
        # center the window on screen
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def create_ui(self):
        # main UI setup: layout and widgets
        layout = QVBoxLayout()

        top_bar_layout = QHBoxLayout()
        top_bar_layout.addStretch(1)

        self.logout_button = QPushButton("Log Out")
        self.logout_button.setFixedWidth(100)
        self.logout_button.clicked.connect(self.handle_logout)
        top_bar_layout.addWidget(self.logout_button)

        layout.addLayout(top_bar_layout)

        title = QLabel("Manager Dashboard")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        user_info = QLabel(
            f"Logged in as manager: {self.user_data.get('name', 'N/A')} ({self.user_data.get('email', 'N/A')}) "
        )
        user_info.setAlignment(Qt.AlignCenter)

        self.report_button = QPushButton("Generate Bookings Report")
        self.report_button.setFont(QFont("Arial", 12))
        self.report_button.setFixedWidth(250)
        self.report_button.clicked.connect(self.generate_bookings_report)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.report_button)
        button_layout.addStretch(1)

        layout.addStretch(1)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(user_info)
        layout.addSpacing(20)
        layout.addLayout(button_layout)
        layout.addStretch(1)

        self.setLayout(layout)

    def handle_logout(self):
        # handle logout action, show login page
        from loginPage import LoginPage
        self.login_window = LoginPage(self.app)
        self.login_window.show()
        self.close()

    def generate_bookings_report(self):
        try:
            response = requests.get(
                "http://127.0.0.1:5000/reports/all_bookings")
            if response.ok:
                report_data = response.json()

                # format data to display
                report_text = "--- All Bookings Report ---\n\n"
                for entry in report_data:
                    report_text += (
                        f"Confirmation: {entry['confirmation_number']}\n"
                        f"  User: {entry['user_name']} ({entry['user_email']})\n"
                        f"  Room: {entry['room_number']} ({entry['room_type']})\n"
                        f"  Check-in: {entry['check_in']} | Check-out: {entry['check_out']}\n"
                        f"  Status: {entry['status']}\n"
                        "--------------------------------\n"
                    )

                # show report (read-only)
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Bookings Report")
                msg_box.setMinimumSize(700, 500)

                text_edit = QTextEdit()
                text_edit.setPlainText(report_text)
                text_edit.setReadOnly(True)
                text_edit.setMinimumSize(650, 400)

                msg_box.layout().addWidget(text_edit, 0, 0, 1, msg_box.layout().columnCount())
                msg_box.exec_()

            else:
                # error msg if report creation fails
                error_msg = response.json().get('error', 'Failed to generate report.')
                QMessageBox.warning(self, "Error", error_msg)

        except requests.exceptions.RequestException as e:
            # error msg if server is unreachable
            QMessageBox.critical(self, "Server Error",
                                 f"Could not connect to the server: {e}")
