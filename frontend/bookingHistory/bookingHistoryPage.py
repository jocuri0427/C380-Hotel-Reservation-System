import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
#BookingHistoryPage
class BookingHistoryPage(QWidget):
    #Constructor
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Booking History")
        self.setGeometry(200, 100, 600, 400)
        self.create_ui()

    #Creating UI
    def create_ui(self):
        main_layout = QVBoxLayout()

        #Title
        title = QLabel("Your Reservations")

        title.setFont(QFont("Arial", 20))

        title.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)

        #History table
        self.history_table = QTableWidget()

        self.history_table.setColumnCount(5)

        self.history_table.setHorizontalHeaderLabels(["Confirmation #", "Room Type", "Check-in", "Check-out", "Status"])

        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.populate_table_with_sample_data()

        main_layout.addWidget(self.history_table)

        self.setLayout(main_layout)

    #Putting sample data for the table
    def populate_table_with_sample_data(self):
        sample_bookings = [
            ("Dummy_id_1", "Dummy Deluxe Room", "2025-07-20", "2025-07-25", "Confirmed"),
            ("Dummy_id_2", "Dummy Standard Room", "2025-06-15", "2025-06-18", "Completed"),
            ("Dummy_id_3", "Dummy Suite Room", "2025-05-01", "2025-05-05", "Cancelled"),
            ("Dummy_id_4", "Dummy Deluxe Room", "2025-08-10", "2025-08-15", "Upcoming"),
        ]

        self.history_table.setRowCount(len(sample_bookings))

        for row, booking in enumerate(sample_bookings):
            for col, data in enumerate(booking):
                self.history_table.setItem(row, col, QTableWidgetItem(str(data)))

#allowing to run the screen directly
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BookingHistoryPage()
    window.show()
    sys.exit(app.exec_())
