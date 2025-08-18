import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QGridLayout, QHBoxLayout, QFrame, QDateEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate

import requests
BASE_URL = "http://127.0.0.1:5000"

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
    def __init__(self, app=None, user_data=None):
        super().__init__()
        self.app = app
        self.user_data = user_data or {}
        who = self.user_data.get("name", "Guest")
        self.setWindowTitle(f"Hotel Reservation System, Welcome {who}")
        self.setGeometry(200, 100, 800, 520)
        self.ui_Setup()

    def ui_Setup(self):
        self.layoutMain = QVBoxLayout()

        # fallback prices if backend does not send anything
        self.nightly_prices = {
            "Standard Room": 120,
            "Deluxe Room": 175,
            "Suite Room": 250
        }
        self.rooms_from_backend = []

        # header
        self.title = QLabel("Find Your Perfect Room")
        self.title.setFont(QFont("Arial", 20))
        self.title.setAlignment(Qt.AlignCenter)

        self.subtitle = QLabel("Search and book the ideal accommodation for your stay")
        self.subtitle.setAlignment(Qt.AlignCenter)

        self.layoutMain.addWidget(self.title)
        self.layoutMain.addWidget(self.subtitle)

        # live price
        self.priceLabel = QLabel("")
        self.priceLabel.setAlignment(Qt.AlignCenter)
        self.priceLabel.setStyleSheet("font-weight: bold; padding: 6px;")
        self.layoutMain.addWidget(self.priceLabel)

        # form
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

        # actions row: Book Now + View Booking History
        actionsRow = QHBoxLayout()
        self.bookNowBtn = QPushButton("Book Now")
        self.bookNowBtn.setStyleSheet("background-color: #007BFF; color: white; padding: 10px;")
        self.bookNowBtn.clicked.connect(self.on_book_now)

        self.viewHistoryBtn = QPushButton("View Booking History")
        self.viewHistoryBtn.setStyleSheet("background-color: #6c757d; color: white; padding: 10px;")
        self.viewHistoryBtn.clicked.connect(self.on_view_history)

        actionsRow.addWidget(self.bookNowBtn)
        actionsRow.addWidget(self.viewHistoryBtn)
        actionsRow.setAlignment(Qt.AlignCenter)
        self.layoutMain.addLayout(actionsRow)

        # room cards
        self.cardLayout = QHBoxLayout()
        self.cardLayout.addWidget(hoverCard("🔔", "Standard Room", self.setRoomType))
        self.cardLayout.addWidget(hoverCard("🏨", "Deluxe Room", self.setRoomType))
        self.cardLayout.addWidget(hoverCard("🏰", "Suite Room", self.setRoomType))

        self.layoutMain.addLayout(self.cardLayout)

        self.setLayout(self.layoutMain)

    def setRoomType(self, value):
        self.roomType.setText(value)
        self.update_price()

    def fetch_rooms_and_cache(self):
        ci = self.checkin.date().toString("yyyy-MM-dd")
        co = self.checkout.date().toString("yyyy-MM-dd")
        try:
            r = requests.get(
                f"{BASE_URL}/rooms/search",
                params={"check_in": ci, "check_out": co},
                timeout=5
            )
            r.raise_for_status()
            data = r.json()
            self.rooms_from_backend = data if isinstance(data, list) else []
        except Exception:
            self.rooms_from_backend = []

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

        self.fetch_rooms_and_cache()

        nightly = self.get_nightly_from_backend_or_local(room_name)
        total = nightly * nights
        self.priceLabel.setText(
            f"{room_name}: ${nightly:.2f} × {nights} night{'s' if nights != 1 else ''} = ${total:.2f}"
        )

    def build_booking_payload(self):
        room_name = self.roomType.text()
        if room_name == "Select a Room Type":
            return None, "Please select a room type."

        ci_qdate = self.checkin.date()
        co_qdate = self.checkout.date()
        nights = ci_qdate.daysTo(co_qdate)
        if nights <= 0:
            return None, "Check-out must be after check-in."

        self.fetch_rooms_and_cache()

        nightly = self.get_nightly_from_backend_or_local(room_name)
        total = nightly * nights
        guests_text = self.guests.currentText()

        booking_data = {
            "room_type": room_name,
            "check_in": ci_qdate.toString("yyyy-MM-dd"),
            "check_out": co_qdate.toString("yyyy-MM-dd"),
            "nights": int(nights),
            "guests": guests_text,
            "price_per_night": float(nightly),
            "total_price": float(total)
        }
        return booking_data, None

    def on_book_now(self):
        booking_data, err = self.build_booking_payload()
        if err:
            QMessageBox.warning(self, "Invalid selection", err)
            return
        try:
            from confirmationPlaceholder import ConfirmationPlaceHolder
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Could not open confirmation page. {e}")
            return

        self.next_win = ConfirmationPlaceHolder(self.app, self.user_data, booking_data)
        self.next_win.show()
        self.close()

    def on_view_history(self):
        try:
            from bookingHistoryPage import BookingHistoryPage
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Could not open booking history. {e}")
            return

        self.next_win = BookingHistoryPage(self.app, self.user_data)
        self.next_win.show()
        self.close()


if __name__ == "__main__":
    qtapp = QApplication(sys.argv)
    dummy_user = {"id": 1, "name": "Guest", "email": "guest@example.com"}
    window = Dashboard(qtapp, dummy_user)
    window.show()
    sys.exit(qtapp.exec_())
