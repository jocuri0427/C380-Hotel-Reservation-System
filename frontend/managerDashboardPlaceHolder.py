import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QApplication, QPushButton, QMessageBox, QTextEdit
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
        # Center the window on the screen
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(
            QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def create_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Manager Dashboard")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # User info
        user_info = QLabel(
            f"Logged in as manager: {self.user_data.get('name', 'N/A')} ({self.user_data.get('email', 'N/A')}) "
        )
        user_info.setAlignment(Qt.AlignCenter)

        self.report_button = QPushButton("Generate Bookings Report")
        self.report_button.setFont(QFont("Arial", 12))
        self.report_button.clicked.connect(self.generate_bookings_report)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(user_info)
        layout.addSpacing(20)
        layout.addWidget(self.report_button) # Add button to layout

        self.setLayout(layout)

    def generate_bookings_report(self):
        try:
            response = requests.get("http://127.0.0.1:5000/reports/all_bookings")
            if response.ok:
                report_data = response.json()
                
                # Format the report for display
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

                # Display the report in a scrollable message box
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
                error_msg = response.json().get('error', 'Failed to generate report.')
                QMessageBox.warning(self, "Error", error_msg)

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Server Error", f"Could not connect to the server: {e}")
