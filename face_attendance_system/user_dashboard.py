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
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import cv2
import face_recognition
import numpy as np
from camera_feed_screen import CameraFeedScreen
from train_model_screen import TrainModelScreen
from utils.file_utils import load_cameras, load_users

class FaceRecognition(QThread):
    recognition_result = pyqtSignal(str)

    def __init__(self, known_faces, known_names):
        super().__init__()
        self.known_faces = known_faces
        self.known_names = known_names
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_faces, face_encoding)
                name = "Unknown"

                if True in matches:
                    matched_idx = np.where(matches)[0][0]
                    name = self.known_names[matched_idx]

                self.recognition_result.emit(f"Detected: {name}")

        cap.release()

    def stop(self):
        self.running = False
        self.quit()

class UserDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Dashboard")
        self.setGeometry(100, 100, 1000, 700)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # **Camera List**
        self.camera_list = QListWidget()
        self.camera_list.itemClicked.connect(self.open_camera_feed)
        self.load_cameras()
        layout.addWidget(self.camera_list)

        # **Train Model Button**
        self.train_model_btn = QPushButton("Train Model")
        self.train_model_btn.clicked.connect(self.open_train_model)
        layout.addWidget(self.train_model_btn)

        # **Start Face Recognition**
        self.start_recognition_btn = QPushButton("Start Face Recognition")
        self.start_recognition_btn.clicked.connect(self.start_face_recognition)
        layout.addWidget(self.start_recognition_btn)

        self.setLayout(layout)

    def load_cameras(self):
        self.camera_list.clear()
        cameras = load_cameras()
        for cam in cameras:
            self.camera_list.addItem(cam["name"])

    def open_camera_feed(self, item):
        self.camera_screen = CameraFeedScreen(item.text())
        self.camera_screen.show()

    def open_train_model(self):
        self.train_screen = TrainModelScreen()
        self.train_screen.show()

    def start_face_recognition(self):
        users = load_users()
        if not users:
            QMessageBox.warning(self, "No Users", "No trained faces available.")
            return
        
        known_faces = [np.array(user['encoding']) for user in users]
        known_names = [user['name'] for user in users]
        
        self.recognition_thread = FaceRecognition(known_faces, known_names)
        self.recognition_thread.recognition_result.connect(self.display_recognition_result)
        self.recognition_thread.start()
    
    def display_recognition_result(self, result):
        QMessageBox.information(self, "Recognition Result", result)
