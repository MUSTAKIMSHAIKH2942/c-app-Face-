# from PyQt5.QtWidgets import (
#     QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout, QCheckBox, QLineEdit
# )
# from PyQt5.QtGui import QIcon
# from utils.constants import MAX_CAMERAS, MAX_USERS
# from utils.file_utils import load_cameras, save_cameras, load_users, save_limits
# from add_user_screen import AddUserScreen
# from add_camera_screen import AddCameraScreen

# class AdminDashboard(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Admin Dashboard")
#         self.setGeometry(100, 100, 800, 600)
#         self.setStyleSheet("background-color: black; color: white;")
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         # Header
#         header = QLabel("Admin Dashboard")
#         header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
#         layout.addWidget(header)

#         # Buttons Layout
#         button_layout = QHBoxLayout()

#         self.add_user_button = QPushButton("Add User")
#         self.add_user_button.setIcon(QIcon("icons/add_user.png"))
#         self.add_user_button.setStyleSheet("padding: 15px; font-size: 16px;")
#         self.add_user_button.clicked.connect(self.add_user)
#         button_layout.addWidget(self.add_user_button)

#         self.add_camera_button = QPushButton("Add Camera")
#         self.add_camera_button.setIcon(QIcon("icons/add_camera.png"))
#         self.add_camera_button.setStyleSheet("padding: 15px; font-size: 16px;")
#         self.add_camera_button.clicked.connect(self.add_camera)
#         button_layout.addWidget(self.add_camera_button)

#         layout.addLayout(button_layout)

#         # Status Labels
#         self.user_count_label = QLabel(f"Users: {len(load_users())}/{MAX_USERS}")
#         self.user_count_label.setStyleSheet("font-size: 16px; margin-top: 20px;")
#         layout.addWidget(self.user_count_label)

#         self.camera_count_label = QLabel(f"Cameras: {len(load_cameras())}/{MAX_CAMERAS}")
#         self.camera_count_label.setStyleSheet("font-size: 16px; margin-top: 10px;")
#         layout.addWidget(self.camera_count_label)

#         # Add-ons Toggle Section
#         self.addons_label = QLabel("Add-ons Settings")
#         self.addons_label.setStyleSheet("font-size: 18px; margin-top: 20px; font-weight: bold;")
#         layout.addWidget(self.addons_label)

#         self.unknown_persons_toggle = QCheckBox("Enable Unknown Person Tracking")
#         self.unknown_persons_toggle.setStyleSheet("font-size: 16px;")
#         layout.addWidget(self.unknown_persons_toggle)

#         # View Unknown Persons Button
#         self.view_unknowns_button = QPushButton("View Unknown Person Data")
#         self.view_unknowns_button.setStyleSheet("padding: 10px; font-size: 16px;")
#         self.view_unknowns_button.clicked.connect(self.view_unknown_persons)
#         layout.addWidget(self.view_unknowns_button)

#         # Limits Section
#         self.limits_label = QLabel("Set User & Camera Limits")
#         self.limits_label.setStyleSheet("font-size: 18px; margin-top: 20px; font-weight: bold;")
#         layout.addWidget(self.limits_label)

#         limits_layout = QHBoxLayout()
#         self.user_limit_input = QLineEdit()
#         self.user_limit_input.setPlaceholderText("Max Users")
#         limits_layout.addWidget(self.user_limit_input)

#         self.camera_limit_input = QLineEdit()
#         self.camera_limit_input.setPlaceholderText("Max Cameras")
#         limits_layout.addWidget(self.camera_limit_input)

#         self.update_limits_button = QPushButton("Update Limits")
#         self.update_limits_button.clicked.connect(self.update_limits)
#         limits_layout.addWidget(self.update_limits_button)

#         layout.addLayout(limits_layout)

#         self.setLayout(layout)

#     def add_user(self):
#         users = load_users()
#         if len(users) >= MAX_USERS:
#             QMessageBox.warning(self, "Limit Exceeded", f"Cannot add more than {MAX_USERS} users.")
#             return
#         self.add_user_screen = AddUserScreen(self)
#         self.add_user_screen.show()

#     def add_camera(self):
#         cameras = load_cameras()
#         if len(cameras) >= MAX_CAMERAS:
#             QMessageBox.warning(self, "Limit Exceeded", f"Cannot add more than {MAX_CAMERAS} cameras.")
#             return
#         self.add_camera_screen = AddCameraScreen(self)
#         self.add_camera_screen.show()

#     def view_unknown_persons(self):
#         QMessageBox.information(self, "Unknown Persons", "Displaying unknown persons data...")

#     def update_limits(self):
#         try:
#             new_max_users = int(self.user_limit_input.text())
#             new_max_cameras = int(self.camera_limit_input.text())

#             if new_max_users < 1 or new_max_cameras < 1:
#                 QMessageBox.warning(self, "Invalid Input", "Limits must be greater than 0.")
#                 return

#             save_limits(new_max_users, new_max_cameras)
#             QMessageBox.information(self, "Success", "Limits updated successfully.")
#         except ValueError:
#             QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for limits.")


from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout, QCheckBox, QLineEdit
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QPropertyAnimation, QRect
from utils.constants import MAX_CAMERAS, MAX_USERS
from utils.file_utils import load_cameras, save_cameras, load_users, save_limits
from add_user_screen import AddUserScreen
from add_camera_screen import AddCameraScreen
from view_unknown_persons import UnknownPersonsViewer

class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #121212; color: #ffffff;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Header
        header = QLabel("Admin Dashboard")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #1db954;")
        layout.addWidget(header)

        # Buttons Layout
        button_layout = QHBoxLayout()

        self.add_user_button = QPushButton("Add User")
        self.add_user_button.setIcon(QIcon("icons/add_user.png"))
        self.add_user_button.setStyleSheet("background-color: #1db954; padding: 15px; font-size: 16px; border-radius: 5px;")
        self.add_user_button.clicked.connect(self.add_user)
        button_layout.addWidget(self.add_user_button)

        self.add_camera_button = QPushButton("Add Camera")
        self.add_camera_button.setIcon(QIcon("icons/add_camera.png"))
        self.add_camera_button.setStyleSheet("background-color: #1db954; padding: 15px; font-size: 16px; border-radius: 5px;")
        self.add_camera_button.clicked.connect(self.add_camera)
        button_layout.addWidget(self.add_camera_button)

        layout.addLayout(button_layout)

        # Status Labels
        self.user_count_label = QLabel(f"Users: {len(load_users())}/{MAX_USERS}")
        self.user_count_label.setStyleSheet("font-size: 16px; margin-top: 20px;")
        layout.addWidget(self.user_count_label)

        self.camera_count_label = QLabel(f"Cameras: {len(load_cameras())}/{MAX_CAMERAS}")
        self.camera_count_label.setStyleSheet("font-size: 16px; margin-top: 10px;")
        layout.addWidget(self.camera_count_label)

        # Add-ons Toggle Section
        self.addons_label = QLabel("Add-ons Settings")
        self.addons_label.setStyleSheet("font-size: 18px; margin-top: 20px; font-weight: bold;")
        layout.addWidget(self.addons_label)

        self.unknown_persons_toggle = QCheckBox("Enable Unknown Person Tracking")
        self.unknown_persons_toggle.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.unknown_persons_toggle)

        # View Unknown Persons Button
        self.view_unknowns_button = QPushButton("View Unknown Person Data")
        self.view_unknowns_button.setStyleSheet("background-color: #1db954; padding: 10px; font-size: 16px; border-radius: 5px;")
        self.view_unknowns_button.clicked.connect(self.view_unknown_persons)
        layout.addWidget(self.view_unknowns_button)

        # Limits Section
        self.limits_label = QLabel("Set User & Camera Limits")
        self.limits_label.setStyleSheet("font-size: 18px; margin-top: 20px; font-weight: bold;")
        layout.addWidget(self.limits_label)

        limits_layout = QHBoxLayout()
        self.user_limit_input = QLineEdit()
        self.user_limit_input.setPlaceholderText("Max Users")
        limits_layout.addWidget(self.user_limit_input)

        self.camera_limit_input = QLineEdit()
        self.camera_limit_input.setPlaceholderText("Max Cameras")
        limits_layout.addWidget(self.camera_limit_input)

        self.update_limits_button = QPushButton("Update Limits")
        self.update_limits_button.setStyleSheet("background-color: #1db954; padding: 10px; border-radius: 5px;")
        self.update_limits_button.clicked.connect(self.update_limits)
        limits_layout.addWidget(self.update_limits_button)

        layout.addLayout(limits_layout)

        self.setLayout(layout)

    def animate_form_open(self, form):
        form.setGeometry(QRect(300, 200, 0, 0))
        form.show()
        animation = QPropertyAnimation(form, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(QRect(300, 200, 0, 0))
        animation.setEndValue(QRect(300, 200, 400, 300))
        animation.start()

    def add_user(self):
        users = load_users()
        if len(users) >= MAX_USERS:
            QMessageBox.warning(self, "Limit Exceeded", f"Cannot add more than {MAX_USERS} users.")
            return
        self.add_user_screen = AddUserScreen(self)
        self.animate_form_open(self.add_user_screen)

    def add_camera(self):
        cameras = load_cameras()
        if len(cameras) >= MAX_CAMERAS:
            QMessageBox.warning(self, "Limit Exceeded", f"Cannot add more than {MAX_CAMERAS} cameras.")
            return
        self.add_camera_screen = AddCameraScreen(self)
        self.animate_form_open(self.add_camera_screen)

    def view_unknown_persons(self):
        self.viewer = UnknownPersonsViewer()  # Create an instance of UnknownPersonsViewer
        self.viewer.show()  # Show the unknown persons log window

    # def update_limits(self):
    #     try:
    #         new_max_users = int(self.user_limit_input.text())
    #         new_max_cameras = int(self.camera_limit_input.text())

    #         if new_max_users < 1 or new_max_cameras < 1:
    #             QMessageBox.warning(self, "Invalid Input", "Limits must be greater than 0.")
    #             return

    #         save_limits(new_max_users, new_max_cameras)
    #         QMessageBox.information(self, "Success", "Limits updated successfully.")
    #     except ValueError:
    #         QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for limits.")
    
    def update_limits(self):
        try:
            new_max_users = int(self.user_limit_input.text())
            new_max_cameras = int(self.camera_limit_input.text())

            if new_max_users < 1 or new_max_cameras < 1:
                QMessageBox.warning(self, "Invalid Input", "Limits must be greater than 0.")
                return

            save_limits(new_max_users, new_max_cameras)

            # Update UI labels to reflect new limits
            self.user_count_label.setText(f"Users: {len(load_users())}/{new_max_users}")
            self.camera_count_label.setText(f"Cameras: {len(load_cameras())}/{new_max_cameras}")

            QMessageBox.information(self, "Success", "Limits updated successfully.")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for limits.")
