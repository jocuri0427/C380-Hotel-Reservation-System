from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QApplication)


class ConfirmationPlaceHolder(QWidget):
    def __init__(self, app, user_data, booking_data=None, parent=None):
        super().__init__(parent)
        self.app = app
        self.user_data = user_data
        self.booking_data = booking_data or {}
        self.setWindowTitle("Booking Confirmation Placeholder")
        self.resize(800, 600)
        self.center()
        self.setup_ui()

    def center(self):
        # Center the window on the screen
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
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
        
        # Placeholder text
        placeholder = QLabel("Placeholder for Confirmation - Pending Toschi's Implementation")
        placeholder.setFont(QFont("Arial", 16))
        placeholder.setAlignment(Qt.AlignCenter)
        
        # Confirmation message
        message = QLabel("Booking Confirmed!")
        message.setFont(QFont("Arial", 14))
        message.setAlignment(Qt.AlignCenter)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("on cancel booking success call")
        cancel_btn.clicked.connect(self.on_back_to_dashboard)
        
        modify_btn = QPushButton("on modify booking success call")
        modify_btn.clicked.connect(self.on_back_to_dashboard)

        back_btn = QPushButton("Go back to Dashboard")
        back_btn.clicked.connect(self.on_back_to_dashboard)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(modify_btn)
        btn_layout.addWidget(back_btn)
        
        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(placeholder)
        layout.addSpacing(20)
        layout.addWidget(message)
        layout.addSpacing(20)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def on_back_to_dashboard(self):
        from dashboardPlaceHolder import DashboardPlaceHolder
        self.dashboard = DashboardPlaceHolder(self.app, self.user_data)
        self.dashboard.show()
        self.close()
