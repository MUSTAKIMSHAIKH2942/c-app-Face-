import sys
import json
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

class AddCameraDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Camera")
        self.setGeometry(300, 300, 400, 250)

        # Set dark theme
        self.setStyleSheet("background-color: black; color: white;")

        layout = QVBoxLayout()

        # Camera Name Input
        self.name_label = QLabel("Camera Name:")
        self.name_label.setStyleSheet("color: white;")
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("background-color: black; color: white; border: 1px solid white;")
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        # IP Address Input (Optional)
        self.ip_label = QLabel("IP Address (Optional):")
        self.ip_label.setStyleSheet("color: white;")
        self.ip_input = QLineEdit()
        self.ip_input.setStyleSheet("background-color: black; color: white; border: 1px solid white;")
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)

        # Location Input
        self.location_label = QLabel("Location:")
        self.location_label.setStyleSheet("color: white;")
        self.location_input = QLineEdit()
        self.location_input.setStyleSheet("background-color: black; color: white; border: 1px solid white;")
        layout.addWidget(self.location_label)
        layout.addWidget(self.location_input)

        # Submit Button
        self.submit_button = QPushButton("Add Camera")
        self.submit_button.setStyleSheet("""
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
        self.submit_button.clicked.connect(self.add_camera)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_camera(self):
        camera_name = self.name_input.text().strip()
        camera_ip = self.ip_input.text().strip() or ""  # Default to empty string if not provided
        location = self.location_input.text().strip()
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

        # File paths
        config_file = "data/limits.json"
        csv_file = "data/camera.csv"

        # Load camera limit from config.json
        max_cameras = 10  # Default limit if config file not found
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
            max_cameras = config.get("MAX_CAMERAS", 10)  # Default to 10 if missing

        # Read existing cameras from CSV
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
        else:
            df = pd.DataFrame(columns=["Camera Name", "IP Address", "Location", "Timestamp"])

        # Check if max cameras limit is reached
        if len(df) >= max_cameras:
            QMessageBox.warning(self, "Limit Exceeded", f"Camera limit of {max_cameras} reached! No more cameras can be added.")
            return

        # Add new camera details
        new_entry = pd.DataFrame([[camera_name, camera_ip, location, timestamp]],
                                  columns=df.columns)
        df = pd.concat([df, new_entry], ignore_index=True)

        # Save to camera.csv
        df.to_csv(csv_file, index=False)

        QMessageBox.information(self, "Success", f"Camera '{camera_name}' added successfully!")
        self.accept()

# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddCameraDialog()
    window.show()
    sys.exit(app.exec_())
