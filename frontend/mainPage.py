import sys
from PyQt5.QtWidgets import QApplication

from loginPage import LoginPage


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.current_user = None
        self.show_login()

    def show_login(self):
        self.login_window = LoginPage(self)
        self.login_window.show()

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    app = App()
    app.run()
