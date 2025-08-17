from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QApplication
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
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
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
        
        # Placeholder text
        placeholder = QLabel("Placeholder for Manager Dashboard")
        placeholder.setFont(QFont("Arial", 16))
        placeholder.setAlignment(Qt.AlignCenter)
        
        # User info
        user_info = QLabel(
            f"Logged in as manager: {self.user_data.get('name', 'N/A')} ({self.user_data.get('email', 'N/A')}) "
        )
        user_info.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(placeholder)
        layout.addSpacing(30)
        layout.addWidget(user_info)
        
        self.setLayout(layout)
