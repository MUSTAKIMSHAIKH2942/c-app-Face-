import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from admin_dashboard import AdminDashboard
from user_dashboard import UserDashboard
from utils.file_utils import load_users

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 250)
        self.setStyleSheet("background-color: black; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Username input
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 10px; font-size: 14px;")
        layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 10px; font-size: 14px;")
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 15px; font-size: 14px;")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 14px;")
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        users = load_users()
        for user in users:
            if user["username"] == username and user["password"] == password:
                if user["role"] == "admin":
                    self.admin_dashboard = AdminDashboard()
                    self.admin_dashboard.show()
                    self.close()
                elif user["role"] == "user":
                    self.user_dashboard = UserDashboard()
                    self.user_dashboard.show()
                    self.close()
                return

        self.error_label.setText("Invalid credentials. Please try again.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())