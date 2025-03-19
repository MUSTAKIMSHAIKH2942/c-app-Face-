from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
from utils.file_utils import load_cameras, save_cameras
from utils.constants import MAX_CAMERAS

class AddCameraScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Camera")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("background-color: black; color: white;")
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Camera name input
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Camera Name")
        self.name_input.setStyleSheet("padding: 10px; font-size: 14px;")
        layout.addWidget(self.name_input)

        # Camera IP input
        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText("Camera IP Address")
        self.ip_input.setStyleSheet("padding: 10px; font-size: 14px;")
        layout.addWidget(self.ip_input)

        # Add camera button
        self.add_button = QPushButton("Add Camera")
        self.add_button.setIcon(QIcon("icons/add_camera.png"))
        self.add_button.setStyleSheet("padding: 15px; font-size: 16px;")
        self.add_button.clicked.connect(self.add_camera)
        layout.addWidget(self.add_button)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 14px;")
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def add_camera(self):
        name = self.name_input.text().strip()
        ip = self.ip_input.text().strip()

        # Validate input fields
        if not name or not ip:
            self.error_label.setText("All fields are required.")
            return

        # Load current cameras
        cameras = load_cameras()

        # Check if we have reached the max number of cameras
        if len(cameras) >= MAX_CAMERAS:
            QMessageBox.warning(self, "Limit Exceeded", f"Cannot add more than {MAX_CAMERAS} cameras.")
            return

        # Check for duplicate IP
        for camera in cameras:
            if camera["ip"] == ip:
                self.error_label.setText("Camera IP already exists.")
                return

        # Add the new camera
        cameras.append({"name": name, "ip": ip})
        save_cameras(cameras)

        # Update parent dashboard if available
        if self.parent:
            self.parent.camera_count_label.setText(f"Cameras: {len(cameras)}/{MAX_CAMERAS}")

        # Show success message
        QMessageBox.information(self, "Success", "Camera added successfully!")
        self.close()
