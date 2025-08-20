import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QGridLayout, QHBoxLayout, QFrame, QDateEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate

import requests

BASE_URL = "http://127.0.0.1:5000"

print("script is running")  # quick check it launched


class HoverCard(QFrame):
    # Clickable room card. Simple and clear.
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

        # icon on top, text under it
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
    # Main screen. Pick dates. Pick a room. Book it.
    def __init__(self, app=None, userData=None):
        super().__init__()
        self.app = app
        self.userData = userData or {}

        who = self.userData.get("name", "Guest")
        self.setWindowTitle(f"Hotel Reservation System. Welcome, {who}")
        self.setGeometry(200, 100, 800, 520)

        # One session for all API calls. Faster and cleaner.
        self.http = requests.Session()
        self.http.headers.update({"X-App": "hotel-desktop-ui"})

        # Cache results for the same date range.
        self.roomCache = {}

        self.uiSetup()

    def uiSetup(self):
        self.layoutMain = QVBoxLayout()

        # logout on the right
        topBarLayout = QHBoxLayout()
        topBarLayout.addStretch(1)
        self.logoutButton = QPushButton("Log Out")
        self.logoutButton.setFixedWidth(100)
        self.logoutButton.clicked.connect(self.handleLogout)
        topBarLayout.addWidget(self.logoutButton)
        self.layoutMain.addLayout(topBarLayout)

        # fallback prices if API is quiet
        self.nightlyPrices = {
            "Standard Room": 120,
            "Deluxe Room": 175,
            "Suite Room": 250
        }
        self.roomsFromBackend = []

        # headers
        self.title = QLabel("Find a room")
        self.title.setFont(QFont("Arial", 20))
        self.title.setAlignment(Qt.AlignCenter)

        self.subtitle = QLabel("Pick dates, pick a room, book it.")
        self.subtitle.setAlignment(Qt.AlignCenter)

        self.layoutMain.addWidget(self.title)
        self.layoutMain.addWidget(self.subtitle)

        # live price readout
        self.priceLabel = QLabel("")
        self.priceLabel.setAlignment(Qt.AlignCenter)
        self.priceLabel.setStyleSheet("font-weight: bold; padding: 6px;")
        self.layoutMain.addWidget(self.priceLabel)

        # form controls
        self.formLayout = QGridLayout()
        self.formLayout.addWidget(QLabel("Check in"), 0, 0)
        self.checkin = QDateEdit()
        self.checkin.setCalendarPopup(True)
        self.checkin.setDate(QDate.currentDate())
        self.formLayout.addWidget(self.checkin, 0, 1)

        self.formLayout.addWidget(QLabel("Check out"), 0, 2)
        self.checkout = QDateEdit()
        self.checkout.setCalendarPopup(True)
        self.checkout.setDate(QDate.currentDate())
        self.formLayout.addWidget(self.checkout, 0, 3)

        self.checkin.dateChanged.connect(self.updatePrice)
        self.checkout.dateChanged.connect(self.updatePrice)

        self.formLayout.addWidget(QLabel("Guests"), 1, 0)
        self.guests = QComboBox()
        self.guests.addItems(["1 Guest", "2 Guests", "3 Guests"])
        self.formLayout.addWidget(self.guests, 1, 1)

        self.formLayout.addWidget(QLabel("Room type"), 1, 2)
        self.roomType = QLabel("Select a Room Type")
        self.roomType.setStyleSheet("font-weight: bold; padding: 6px;")
        self.formLayout.addWidget(self.roomType, 1, 3)

        self.layoutMain.addLayout(self.formLayout)

        # booking and history actions
        actionsRow = QHBoxLayout()
        self.bookNowBtn = QPushButton("Continue to Booking")
        self.bookNowBtn.setStyleSheet("background-color: #007BFF; color: white; padding: 10px;")
        self.bookNowBtn.clicked.connect(self.onBookNow)
        self.bookNowBtn.setEnabled(False)  # enable after a room is chosen

        self.viewHistoryBtn = QPushButton("View Past Bookings")
        self.viewHistoryBtn.setStyleSheet("background-color: #6c757d; color: white; padding: 10px;")
        self.viewHistoryBtn.clicked.connect(self.onViewHistory)

        actionsRow.addWidget(self.bookNowBtn)
        actionsRow.addWidget(self.viewHistoryBtn)
        actionsRow.setAlignment(Qt.AlignCenter)
        self.layoutMain.addLayout(actionsRow)

        # room choice cards
        self.cardLayout = QHBoxLayout()
        self.cardLayout.addWidget(HoverCard("🔔", "Standard Room", self.setRoomType))
        self.cardLayout.addWidget(HoverCard("🏨", "Deluxe Room", self.setRoomType))
        self.cardLayout.addWidget(HoverCard("🏰", "Suite Room", self.setRoomType))
        self.layoutMain.addLayout(self.cardLayout)

        self.setLayout(self.layoutMain)

        # simple tab order. makes keyboard navigation smooth.
        self.setTabOrder(self.checkin, self.checkout)
        self.setTabOrder(self.checkout, self.guests)
        self.setTabOrder(self.guests, self.bookNowBtn)

    def handleLogout(self):
        # Confirm before logging out.
        reply = QMessageBox.question(self, "Log out", "Log out now?")
        if reply == QMessageBox.Yes:
            from loginPage import LoginPage
            self.loginWindow = LoginPage(self.app)
            self.loginWindow.show()
            self.close()

    def setRoomType(self, value):
        # Update selection and show price.
        self.roomType.setText(value)
        self.bookNowBtn.setEnabled(True)
        self.updatePrice()

    def getWithRetry(self, url, retries=3, **kwargs):
        # Tiny retry loop for flaky networks.
        lastErr = None
        for _ in range(retries):
            try:
                r = self.http.get(url, timeout=5, **kwargs)
                r.raise_for_status()
                return r
            except requests.RequestException as e:
                lastErr = e
        raise lastErr if lastErr else RuntimeError("request failed")

    def fetchRoomsAndCache(self):
        # Pull available rooms for the chosen dates. Cache the result.
        ci = self.checkin.date().toString("yyyy-MM-dd")
        co = self.checkout.date().toString("yyyy-MM-dd")
        key = (ci, co)

        if key in self.roomCache:
            self.roomsFromBackend = self.roomCache[key]
            return

        try:
            resp = self.getWithRetry(
                f"{BASE_URL}/rooms/search",
                params={"check_in": ci, "check_out": co}
            )
            data = resp.json()
            self.roomsFromBackend = data if isinstance(data, list) else []
            self.roomCache[key] = self.roomsFromBackend
        except requests.RequestException:
            self.roomsFromBackend = []

    def matchRoomName(self, room):
        # Find the name field the API used.
        for k in ("name", "type", "room_type", "roomName", "title"):
            val = room.get(k)
            if isinstance(val, str) and val.strip():
                return val.strip()
        return None

    def extractPrice(self, room):
        # Grab a price field that exists and is a number.
        for k in ("base_price", "price", "rate", "nightly", "cost"):
            val = room.get(k)
            try:
                if val is not None:
                    return float(val)
            except (TypeError, ValueError):
                continue
        return None

    def nightlyRate(self, roomName):
        # Use API price if present. Fall back to local defaults.
        for room in self.roomsFromBackend:
            apiName = self.matchRoomName(room)
            if apiName and apiName.casefold() == roomName.casefold():
                price = self.extractPrice(room)
                if price is not None:
                    return price
        return float(self.nightlyPrices.get(roomName, 0.0))

    def updatePrice(self):
        # Update the price label when dates or room change.
        roomName = self.roomType.text()
        if roomName == "Select a Room Type":
            self.priceLabel.setText("Select a room type to see the price.")
            return

        ci = self.checkin.date()
        co = self.checkout.date()
        nights = ci.daysTo(co)
        if nights <= 0:
            self.priceLabel.setText("Check-out must be after check-in.")
            return

        self.fetchRoomsAndCache()
        nightly = self.nightlyRate(roomName)
        total = nightly * nights
        plural = "nights" if nights != 1 else "night"
        self.priceLabel.setText(f"{roomName}: ${nightly:.2f} × {nights} {plural} = ${total:.2f}")

    def buildBookingPayload(self):
        # Build the JSON body to send when booking.
        roomName = self.roomType.text()
        if roomName == "Select a Room Type":
            return None, "Please select a room type."

        ciQ = self.checkin.date()
        coQ = self.checkout.date()
        nights = ciQ.daysTo(coQ)
        if nights <= 0:
            return None, "Check-out must be after check-in."

        self.fetchRoomsAndCache()
        nightly = self.nightlyRate(roomName)
        total = nightly * nights
        guestsText = self.guests.currentText()

        bookingData = {
            "room_type": roomName,
            "check_in": ciQ.toString("yyyy-MM-dd"),
            "check_out": coQ.toString("yyyy-MM-dd"),
            "nights": int(nights),
            "guests": guestsText,
            "price_per_night": float(nightly),
            "total_price": float(total)
        }
        return bookingData, None

    def getSelectedRoomData(self, roomName):
        # Return the full room dict that matches the choice.
        for room in self.roomsFromBackend:
            apiName = room.get("room_type")
            if apiName and apiName.strip().lower() == roomName.strip().lower():
                return room
        return None

    def onBookNow(self):
        # Booking flow. Validate, then open the booking page.
        bookingPayload, err = self.buildBookingPayload()
        if err:
            QMessageBox.warning(self, "Please check your dates", err)
            return

        self.fetchRoomsAndCache()
        roomName = bookingPayload.get("room_type")
        roomData = self.getSelectedRoomData(roomName)

        if roomData is None:
            QMessageBox.information(self, "No matching room", "That room type is not available for these dates.")
            return

        try:
            from bookingPage import BookingPage
        except Exception as e:
            QMessageBox.critical(self, "Could not open booking", f"Booking page failed to load.\n{e}")
            return

        self.nextWin = BookingPage(self.app, self.userData, roomData)
        self.nextWin.show()
        self.close()

    def onViewHistory(self):
        # Open the booking history page.
        try:
            from bookingHistoryPage import BookingHistoryPage
        except Exception as e:
            QMessageBox.critical(self, "Could not open history", f"Booking history failed to load.\n{e}")
            return

        self.nextWin = BookingHistoryPage(self.app, self.userData)
        self.nextWin.show()
        self.close()


if __name__ == "__main__":
    # Run the app with a dummy user. Replace with real user data after login.
    qtapp = QApplication(sys.argv)
    dummyUser = {"id": 1, "name": "Guest", "email": "guest@example.com"}
    window = Dashboard(qtapp, dummyUser)
    window.show()
    sys.exit(qtapp.exec_())
