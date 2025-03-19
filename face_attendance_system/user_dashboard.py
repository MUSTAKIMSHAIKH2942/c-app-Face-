# from PyQt5.QtWidgets import (
#     QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout, QFrame,
#     QGridLayout, QMessageBox
# )
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import Qt

# from utils.file_utils import load_cameras, load_users, save_users
# from train_model_screen import TrainModelScreen  # Assumed screen for training
# from camera_feed_screen import CameraFeedScreen  # Assumed camera feed UI

# class UserDashboard(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("User Dashboard")
#         self.setGeometry(100, 100, 1000, 700)
#         self.setStyleSheet("background-color: #1E1E1E; color: white;")
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         # **Top Navigation Icons**
#         top_nav = QHBoxLayout()
#         self.menu_btn = self.create_icon_button("icons/menu.png", "Menu")
#         self.live_play_btn = self.create_icon_button("icons/live.png", "Live Video")
#         self.connect_camera_btn = self.create_icon_button("icons/connect.png", "Connect Camera")
#         self.add_camera_btn = self.create_icon_button("icons/add_camera.png", "Add Camera")

#         top_nav.addWidget(self.menu_btn)
#         top_nav.addWidget(self.live_play_btn)
#         top_nav.addWidget(self.connect_camera_btn)
#         top_nav.addWidget(self.add_camera_btn)
#         layout.addLayout(top_nav)

#         # **Main Layout (3 Sections)**
#         main_layout = QHBoxLayout()

#         # **Left Panel (Camera List)**
#         self.camera_list = QListWidget()
#         self.camera_list.setStyleSheet("background-color: #333; color: white; font-size: 16px;")
#         self.camera_list.itemClicked.connect(self.open_camera_feed)
#         self.load_cameras()
#         main_layout.addWidget(self.camera_list, 2)

#         # **Center Panel (Face Recognition & Add-ons)**
#         center_layout = QVBoxLayout()
#         self.face_recognition_label = QLabel("Face Recognition & Add-ons")
#         self.face_recognition_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
#         center_layout.addWidget(self.face_recognition_label, alignment=Qt.AlignCenter)

#         self.train_model_btn = QPushButton("Train Model")
#         self.train_model_btn.setStyleSheet("padding: 12px; font-size: 16px; background-color: #007BFF; color: white;")
#         self.train_model_btn.clicked.connect(self.open_train_model)
#         center_layout.addWidget(self.train_model_btn, alignment=Qt.AlignCenter)

#         self.view_users_btn = QPushButton("View Users Dashboard")
#         self.view_users_btn.setStyleSheet("padding: 12px; font-size: 16px; background-color: #28A745; color: white;")
#         center_layout.addWidget(self.view_users_btn, alignment=Qt.AlignCenter)

#         main_layout.addLayout(center_layout, 3)

#         # **Right Panel (Live Logs)**
#         self.log_label = QLabel("Live Logs")
#         self.log_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
#         self.log_list = QListWidget()
#         self.log_list.setStyleSheet("background-color: #222; color: white; font-size: 14px;")

#         right_layout = QVBoxLayout()
#         right_layout.addWidget(self.log_label)
#         right_layout.addWidget(self.log_list)
#         main_layout.addLayout(right_layout, 3)

#         layout.addLayout(main_layout)
#         self.setLayout(layout)

#     def create_icon_button(self, icon_path, tooltip):
#         """Helper function to create an icon button."""
#         button = QPushButton()
#         button.setIcon(QIcon(icon_path))
#         button.setStyleSheet("border: none; padding: 8px; background-color: transparent;")
#         button.setToolTip(tooltip)
#         return button

#     def load_cameras(self):
#         """Load camera list dynamically from the database."""
#         self.camera_list.clear()
#         cameras = load_cameras()
#         for camera in cameras:
#             self.camera_list.addItem(camera["name"])

#     def open_camera_feed(self, item):
#         """Open the selected camera feed."""
#         camera_name = item.text()
#         self.log_list.addItem(f"Opened camera feed: {camera_name}")
#         self.camera_feed_screen = CameraFeedScreen(camera_name)
#         self.camera_feed_screen.show()

#     def open_train_model(self):
#         """Open the model training screen."""
#         users = load_users()
#         if len(users) == 0:
#             QMessageBox.warning(self, "No Users", "No known persons available for training.")
#             return
#         self.train_model_screen = TrainModelScreen()
#         self.train_model_screen.show()

#     def add_log_entry(self, message):
#         """Dynamically add log entries."""
#         self.log_list.addItem(message)



import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QGridLayout, QTextEdit, QComboBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import add_camera_screen

class UserDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera Dashboard")
        self.setGeometry(100, 100, 1400, 900)

        # Set black and green color theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #15171c;
            }
            QPushButton {
                background-color: #5371ff;
                color: #ffffff;  /* Text color changed to white */
                font-size: 14px;
                padding: 10px;
                border: none;
                border-radius: 10px;  /* Added border radius */
            }
            QPushButton:hover {
                background-color: #3a5bff;  /* Slightly darker blue on hover */
            }
            QListWidget, QTextEdit, QComboBox {
                background-color: #15171c;
                color: #ffffff;  /* Text color changed to white */
                border: 1px solid #5371ff;
                font-size: 14px;
                border-radius: 5px;  /* Added border radius */
            }
            QLabel {
                color: #ffffff;  /* Text color changed to white */
                font-size: 16px;
            }
        """)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Top horizontal plane (centered options)
        top_panel = QHBoxLayout()
        main_layout.addLayout(top_panel)

        # Add stretch to center the buttons
        top_panel.addStretch()
        top_panel.addWidget(QPushButton("Live Feed"))
        top_panel.addWidget(QPushButton("Replay"))
        top_panel.addWidget(QPushButton("Export"))
        top_panel.addStretch()

        # User section (photo and name)
        user_section = QVBoxLayout()
        user_photo = QLabel()
        user_photo.setPixmap(QPixmap("user_photo.png").scaled(50, 50, Qt.KeepAspectRatio))  # Replace with actual photo path
        user_section.addWidget(user_photo)
        user_section.addWidget(QLabel("User Name"))
        top_panel.addLayout(user_section)

        # Middle section (left, middle, right panels)
        middle_section = QHBoxLayout()
        main_layout.addLayout(middle_section)

        # Left panel (Add Camera, Camera List, and Grid View Options)
        left_panel = QVBoxLayout()
        left_panel.addWidget(QPushButton("Add Camera"))
        camera_list = QListWidget()
        camera_list.addItems([f"Camera O{i}" for i in range(1, 10)] + ["Camera IO"])
        left_panel.addWidget(camera_list)

        # Grid View Options (Combo Box)
        grid_options = QComboBox()
        grid_options.addItems(["2X2","4x4", "6x6", "8x8"])
        grid_options.currentTextChanged.connect(self.change_grid_view)
        left_panel.addWidget(QLabel("Grid View:"))
        left_panel.addWidget(grid_options)

        middle_section.addLayout(left_panel)

        # Middle panel (Grid View for Video Feeds)
        self.middle_panel = QGridLayout()
        self.current_grid_size = 2  # Default grid size
        self.update_grid_view(2)  # Initialize with 3x3 grid
        middle_section.addLayout(self.middle_panel, stretch=5)  # Middle panel is bigger

        # Right panel (Camera Management and Activity Log)
        right_panel = QVBoxLayout()
        right_panel.addWidget(QPushButton("Load Camera"))
        right_panel.addWidget(QPushButton("Save Camera"))
        right_panel.addWidget(QPushButton("Add IP Camera"))
        activity_log = QTextEdit()
        activity_log.setReadOnly(True)
        activity_log.setPlaceholderText("Activity Log: Person Detected: John Doe")
        right_panel.addWidget(activity_log)
        middle_section.addLayout(right_panel, stretch=2)  # Right panel is narrower

        # Bottom options (Add Known Person, User, License Validation, Exit)
        bottom_panel = QHBoxLayout()
        bottom_panel.addWidget(QPushButton("Add Known Person"))
        bottom_panel.addWidget(QPushButton("User"))
        bottom_panel.addWidget(QPushButton("License Validation"))
        bottom_panel.addWidget(QPushButton("Exit"))
        main_layout.addLayout(bottom_panel)

    def open_add_camera_screen(self):
        """Open the Add Camera screen."""
        self.add_camera_screen = add_camera_screen()
        self.add_camera_screen.show()

    def change_grid_view(self, text):
        """Change the grid view based on the selected option."""
        if text == "2X2":
            self.update_grid_view(2)
        elif text == "4x4":
            self.update_grid_view(4)
        elif text == "6x6":
            self.update_grid_view(6)
        elif text == "8x8":
            self.update_grid_view(8)

  
    def update_grid_view(self, size):
        """Update the video feed grid layout dynamically with rounded borders."""
        # Remove existing widgets
        while self.middle_panel.count():
            item = self.middle_panel.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.current_grid_size = size  # Update grid size
        
        for i in range(size):
            for j in range(size):
                feed_widget = QLabel(f"Feed {i * size + j + 1}")  # Placeholder for camera feeds
                # feed_label.setStyleSheet("border: 2px solid #5371ff; color: #ffffff;")  
                feed_widget.setAlignment(Qt.AlignCenter)
                
                # Apply rounded corners and border styling
                feed_widget.setStyleSheet("""
                    background-color: black;
                    min-height: 150px;
                    border-radius: 15px; /* Rounded corners */
                    border: 2px solid #555; /* Optional border */
                    color: white;
                    border: 2px solid #5371ff; color: #ffffff;
                """)
                
                self.middle_panel.addWidget(feed_widget, i, j)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = UserDashboard()
    dashboard.show()
    sys.exit(app.exec_())
























  # def update_grid_view(self, size):
    #     """Update the grid view with the specified size."""
    #     # Clear the existing grid
    #     for i in reversed(range(self.middle_panel.count())):
    #         self.middle_panel.itemAt(i).widget().setParent(None)

    #     # Add new grid items
    #     for i in range(size):
    #         for j in range(size):
    #             feed_label = QLabel(f"Camera Feed {i * size + j + 1}")
    #             feed_label.setAlignment(Qt.AlignCenter)
    #             feed_label.setStyleSheet("border: 2px solid #5371ff; color: #ffffff;")  
    #             self.middle_panel.addWidget(feed_label, i, j)

    #     self.current_grid_size = size