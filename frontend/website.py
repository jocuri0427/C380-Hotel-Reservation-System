import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QGridLayout, QHBoxLayout, QFrame, QDateEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate

# this is to try to call the backend, might be a lil flakey cause i was looking through tiktok for help lol
import requests
BASE_URL = "http://127.0.0.1:5000"

print("script is running")


class hoverCard(QFrame):
    def __init__(self, icon, textLabel, onClick):
        super().__init__()
        # regular and hover style, nothing crazy
        self.setFrameShape(QFrame.NoFrame)
        self.regStyle = """
            background-color: white; border: none; border-radius: 10px; padding: 25px;
        """
        self.hoverStyle = """ background-color: #f0f8ff; border: none; border-radius: 10px; padding: 25px;
        """
        self.setStyleSheet(self.regStyle)
        self.textLabel = textLabel
        self.onClick = onClick

        # layout for the cards
        self.layout = QVBoxLayout()
        self.iconLabel = QLabel(icon)
        self.iconLabel.setFont(QFont("Arial", 28))
        self.iconLabel.setAlignment(Qt.AlignCenter)

        self.label = QLabel(textLabel)
        self.label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.iconLabel)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # so the mouse changes to pointer when over card
        self.setCursor(Qt.PointingHandCursor)

    # just for decoration fr
    def enterEvent(self, event):
        self.setStyleSheet(self.hoverStyle)

    def leaveEvent(self, event):
        self.setStyleSheet(self.regStyle)

    # when you click, it sends the text to the function passed in
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

        # fallback prices if backend doesn’t send anything
        self.nightly_prices = {
            "Standard Room": 120,
            "Deluxe Room": 175,
            "Suite Room": 250
        }
        # this will store /rooms/search results from backend
        self.rooms_from_backend = []

        # title + subtitle at top
        self.title = QLabel("Find Your Perfect Room")
        self.title.setFont(QFont("Arial", 20))
        self.title.setAlignment(Qt.AlignCenter)

        self.subtitle = QLabel(
            "Search and book the ideal accommodation for your stay")
        self.subtitle.setAlignment(Qt.AlignCenter)

        self.layoutMain.addWidget(self.title)
        self.layoutMain.addWidget(self.subtitle)

        # label to show the price result
        self.priceLabel = QLabel("")
        self.priceLabel.setAlignment(Qt.AlignCenter)
        self.priceLabel.setStyleSheet("font-weight: bold; padding: 6px;")
        self.layoutMain.addWidget(self.priceLabel)

        # form with dates, guests, room type
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

        # update price whenever dates change
        self.checkin.dateChanged.connect(self.update_price)
        self.checkout.dateChanged.connect(self.update_price)

        self.formLayout.addWidget(QLabel("Guests:"), 1, 0)
        self.guests = QComboBox()
        self.guests.addItems(["1 Guest", "2 Guests", "3 Guests"])
        self.formLayout.addWidget(self.guests, 1, 1)

        self.formLayout.addWidget(QLabel("Room Type:"), 1, 2)
        self.roomType = QLabel("Select a Room Type")
        self.roomType.setStyleSheet("font-weight: bold; padding: 6px;")
        self.formLayout.addWidget(self.roomType, 1, 3)

        self.layoutMain.addLayout(self.formLayout)

        # button to activate the backend and then search for the rooms.
        self.searchButton = QPushButton("Search Rooms")
        self.searchButton.setStyleSheet(
            "background-color: #007BFF; color: white; padding: 10px;")
        self.layoutMain.addWidget(self.searchButton)

        # when we click search, it gets the backend data then updates price
        self.searchButton.clicked.connect(self.fetch_rooms_and_update)

        # little cards for room options added some emojis so it doesnt look so dead yk
        self.cardLayout = QHBoxLayout()
        self.cardLayout.addWidget(
            hoverCard("🔔", "Standard Room", self.setRoomType))
        self.cardLayout.addWidget(
            hoverCard("🏨", "Deluxe Room", self.setRoomType))
        self.cardLayout.addWidget(
            hoverCard("🏰", "Suite Room", self.setRoomType))

        self.layoutMain.addLayout(self.cardLayout)

        self.setLayout(self.layoutMain)

    def setRoomType(self, value):
        # this will update the label for the room type then recalculates price
        self.roomType.setText(value)
        self.update_price()

    # goes to backend /rooms/search and saves results
    def fetch_rooms_and_update(self):
        ci = self.checkin.date().toString("yyyy-MM-dd")
        co = self.checkout.date().toString("yyyy-MM-dd")
        try:
            r = requests.get(f"{BASE_URL}/rooms/search",
                             params={"check_in": ci, "check_out": co},
                             timeout=5)
            r.raise_for_status()
            data = r.json()
            self.rooms_from_backend = data if isinstance(data, list) else []
        except Exception:

            self.rooms_from_backend = []
        self.update_price()

    # this will get the nightly rate from backend if the backend flakes then we use the set ones.
    def get_nightly_from_backend_or_local(self, room_name):
        for room in self.rooms_from_backend:
            api_name = (
                room.get("name") or
                room.get("type") or
                room.get("room_type") or
                room.get("roomName") or
                room.get("title")
            )
            if api_name and api_name.strip().lower() == room_name.strip().lower():
                nightly = (
                    room.get("base_price") or
                    room.get("price") or
                    room.get("rate") or
                    room.get("nightly") or
                    room.get("cost")
                )
                if nightly is not None:
                    try:
                        return float(nightly)
                    except:
                        pass
        return float(self.nightly_prices.get(room_name, 0))

    # this calculates nights times nightly and gives us the total
    def update_price(self):
        room_name = self.roomType.text()
        if room_name == "Select a Room Type":
            self.priceLabel.setText("Pick a room type to see price.")
            return

        ci = self.checkin.date()
        co = self.checkout.date()
        nights = ci.daysTo(co)
        if nights <= 0:
            self.priceLabel.setText("Check-out must be after check-in.")
            return

        nightly = self.get_nightly_from_backend_or_local(room_name)
        total = nightly * nights
        self.priceLabel.setText(
            f"{room_name}: ${nightly:.2f} × {nights} night{'s' if nights != 1 else ''} = ${total:.2f}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
