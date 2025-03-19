from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
from utils.file_utils import load_users, save_users
from utils.constants import MAX_USERS

class AddUserScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add User")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("background-color: black; color: white;")
        self.parent = parent
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

        # Role selection
        self.role_input = QLineEdit(self)
        self.role_input.setPlaceholderText("Role (admin/user)")
        self.role_input.setStyleSheet("padding: 10px; font-size: 14px;")
        layout.addWidget(self.role_input)

        # Add user button
        self.add_button = QPushButton("Add User")
        self.add_button.setIcon(QIcon("icons/add_user.png"))
        self.add_button.setStyleSheet("padding: 15px; font-size: 16px;")
        self.add_button.clicked.connect(self.add_user)
        layout.addWidget(self.add_button)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 14px;")
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_input.text().strip().lower()

        if not username or not password or not role:
            self.error_label.setText("All fields are required.")
            return

        if role not in ["admin", "user"]:
            self.error_label.setText("Role must be 'admin' or 'user'.")
            return

        users = load_users()
        if len(users) >= MAX_USERS:
            QMessageBox.warning(self, "Limit Exceeded", f"Cannot add more than {MAX_USERS} users.")
            return

        # Check for duplicate username
        for user in users:
            if user["username"] == username:
                self.error_label.setText("Username already exists.")
                return

        # Add new user
        users.append({"username": username, "password": password, "role": role})
        save_users(users)

        # Update parent dashboard
        if self.parent:
            self.parent.user_count_label.setText(f"Users: {len(users)}/{MAX_USERS}")

        QMessageBox.information(self, "Success", "User added successfully!")
        self.close()
        
        
        
        
        # from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
# from PyQt5.QtGui import QIcon
# from utils.file_utils import load_users, save_users
# from utils.constants import MAX_USERS

# class AddUserScreen(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Add User")
#         self.setGeometry(200, 200, 400, 300)
#         self.setStyleSheet("background-color: black; color: white;")
#         self.parent = parent
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         # Username input
#         self.username_input = QLineEdit(self)
#         self.username_input.setPlaceholderText("Username")
#         self.username_input.setStyleSheet("padding: 10px; font-size: 14px;")
#         layout.addWidget(self.username_input)

#         # Password input
#         self.password_input = QLineEdit(self)
#         self.password_input.setPlaceholderText("Password")
#         self.password_input.setEchoMode(QLineEdit.Password)
#         self.password_input.setStyleSheet("padding: 10px; font-size: 14px;")
#         layout.addWidget(self.password_input)

#         # Role selection
#         self.role_input = QLineEdit(self)
#         self.role_input.setPlaceholderText("Role (admin/user)")
#         self.role_input.setStyleSheet("padding: 10px; font-size: 14px;")
#         layout.addWidget(self.role_input)

#         # Add user button
#         self.add_button = QPushButton("Add User")
#         self.add_button.setIcon(QIcon("icons/add_user.png"))
#         self.add_button.setStyleSheet("padding: 15px; font-size: 16px;")
#         self.add_button.clicked.connect(self.add_user)
#         layout.addWidget(self.add_button)

#         # Error label
#         self.error_label = QLabel("")
#         self.error_label.setStyleSheet("color: red; font-size: 14px;")
#         layout.addWidget(self.error_label)

#         self.setLayout(layout)

#     def add_user(self):
#         username = self.username_input.text().strip()
#         password = self.password_input.text().strip()
#         role = self.role_input.text().strip().lower()

#         if not username or not password or not role:
#             self.error_label.setText("All fields are required.")
#             return

#         if role not in ["admin", "user"]:
#             self.error_label.setText("Role must be 'admin' or 'user'.")
#             return

#         users = load_users()
#         if len(users) >= MAX_USERS:
#             QMessageBox.warning(self, "Limit Exceeded", f"Cannot add more than {MAX_USERS} users.")
#             return

#         # Check for duplicate username
#         for user in users:
#             if user["username"] == username:
#                 self.error_label.setText("Username already exists.")
#                 return

#         # Add new user
#         users.append({"username": username, "password": password, "role": role})
#         save_users(users)

#         # Update parent dashboard
#         if self.parent:
#             self.parent.user_count_label.setText(f"Users: {len(users)}/{MAX_USERS}")

#         QMessageBox.information(self, "Success", "User added successfully!")
#         self.close()