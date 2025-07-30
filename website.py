import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QGridLayout, QHBoxLayout, QFrame, QDateEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate

print("script is running")

class hoverCard(QFrame):
    def __init__(self, icon, textLabel, onClick):
        super().__init__()
        self.setFrameShape(QFrame.NoFrame)
        self.regStyle = """
            background-color: white; border: none; border-radius: 10px; padding: 25px;
        """
        self.hoverStyle = """ background-color: #f0f8ff; border: none; border-radius: 10px; padding: 25px;
        """
        self.setStyleSheet(self.regStyle)
        self.textLabel = textLabel
        self.onClick = onClick

        self.layout = QVBoxLayout()
        self.iconLabel = QLabel(icon)
        self.iconLabel.setFont(QFont("Arial", 28))
        self.iconLabel.setAlignment(Qt.AlignCenter)

        self.label = QLabel(textLabel)
        self.label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.iconLabel)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.setCursor(Qt.PointingHandCursor)

    def enterEvent(self, event):
        self.setStyleSheet(self.hoverStyle)
    
    def leaveEvent(self, event):
        self.setStyleSheet(self.regStyle)

    def mousePressEvent(self, event):
        self.onClick(self.textLabel)

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hotel Reservation System")
        self.setGeometry(200, 100, 800, 500)
        self.ui_Setup()

    def ui_Setup(self):
        self.layoutMain = QVBoxLayout()

        
        self.title = QLabel("Find Your Perfect Room")
        self.title.setFont(QFont("Arial", 20))
        self.title.setAlignment(Qt.AlignCenter)

        self.subtitle = QLabel("Search and book the ideal accommodation for your stay")
        self.subtitle.setAlignment(Qt.AlignCenter)

        self.layoutMain.addWidget(self.title)
        self.layoutMain.addWidget(self.subtitle)

        
        self.formLayout = QGridLayout()
        self.formLayout.addWidget(QLabel("Check-in:"), 0, 0)
        self.checkin = QDateEdit()
        self.checkin.setCalendarPopup(True)
        self.checkin.setDate(QDate.currentDate())
        self.formLayout.addWidget(self.checkin, 0, 1)

        self.formLayout.addWidget(QLabel("Check-out:"), 0, 2)
        self.checkout = QDateEdit()
        self.checkout.setCalendarPopup(True)
        self.checkout.setDate(QDate.currentDate())
        self.formLayout.addWidget(self.checkout, 0, 3)

        self.formLayout.addWidget(QLabel("Guests:"), 1, 0)
        self.guests = QComboBox()
        self.guests.addItems(["1 Guest", "2 Guests", "3 Guests"])
        self.formLayout.addWidget(self.guests, 1, 1)

        self.formLayout.addWidget(QLabel("Room Type:"), 1, 2)
        self.roomType = QLabel("Select a Room Type")
        self.roomType.setStyleSheet("font-weight: bold; padding: 6px;")
        self.formLayout.addWidget(self.roomType, 1, 3)

        self.layoutMain.addLayout(self.formLayout)

        
        self.searchButton = QPushButton("Search Rooms")
        self.searchButton.setStyleSheet("background-color: #007BFF; color: white; padding: 10px;")
        self.layoutMain.addWidget(self.searchButton)

        
        self.cardLayout = QHBoxLayout()
        self.cardLayout.addWidget(hoverCard("🔔", "Standard Room", self.setRoomType))
        self.cardLayout.addWidget(hoverCard("🏨", "Deluxe Room", self.setRoomType))
        self.cardLayout.addWidget(hoverCard("🏰", "Suite Room", self.setRoomType))

        self.layoutMain.addLayout(self.cardLayout)

        self.setLayout(self.layoutMain)

    def setRoomType(self, value):
        self.roomType.setText(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
