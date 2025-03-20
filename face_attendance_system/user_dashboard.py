import sys
import json
import cv2
import os
import numpy as np
import csv
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QGridLayout, QTextEdit, QComboBox,
    QMessageBox, QDialog, QTableWidgetItem, QTableWidget, QHeaderView
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
import pandas as pd
from add_camera_screen import AddCameraDialog

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
MODEL_PATH = "trained_model.yml"
DATA_PATH = "data/training_images"
LOGS_FILE = "data/logs.csv"
CAMERA_CSV = "data/camera.csv"

# Face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

if os.path.exists(MODEL_PATH):
    recognizer.read(MODEL_PATH)
else:
    recognizer = None  # No trained model yet

class CameraStreamFactory:
    @staticmethod
    def create_camera_stream(ip):
        try:
            return CameraStream(ip)
        except Exception as e:
            logging.error(f"Failed to create camera stream for IP {ip}: {str(e)}")
            raise ValueError(f"Failed to initialize camera stream: {str(e)}")

class CameraStream(QLabel):
    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self.cap = cv2.VideoCapture(ip)
        if not self.cap.isOpened():
            error_msg = f"Unable to open camera stream at {ip}. Please check the IP address and connection."
            logging.error(error_msg)
            raise ValueError(error_msg)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
    
    def update_frame(self):
        try:
            ret, frame = self.cap.read()
            if ret:
                frame, face_names = self.process_frame(frame)
                self.log_faces(face_names)
                self.display_frame(frame)
        except Exception as e:
            logging.error(f"Error updating frame: {str(e)}")
    
    def process_frame(self, frame):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            face_names = []
            
            for (x, y, w, h) in faces:
                face_img = gray[y:y+h, x:x+w]
                name = "Unknown"
                color = (0, 0, 255)  # Red for unknown
                
                if recognizer:
                    label, confidence = recognizer.predict(face_img)
                    if confidence < 80:  # Confidence threshold
                        name = f"Person {label}"
                        color = (0, 255, 0)  # Green for known
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                face_names.append(name)
            
            return frame, face_names
        except Exception as e:
            logging.error(f"Error processing frame: {str(e)}")
            return frame, []
    
    def log_faces(self, face_names):
        try:
            if face_names:
                with open(LOGS_FILE, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([face_names, cv2.getTickCount()])
        except Exception as e:
            logging.error(f"Error logging faces: {str(e)}")
    
    def display_frame(self, frame):
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qimg = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.setPixmap(QPixmap.fromImage(qimg))
        except Exception as e:
            logging.error(f"Error displaying frame: {str(e)}")
    
    def closeEvent(self, event):
        try:
            self.cap.release()
            logging.info(f"Camera stream at {self.ip} released.")
        except Exception as e:
            logging.error(f"Error releasing camera stream: {str(e)}")
        event.accept()

class UserDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera Dashboard")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #15171c;
            }
            QPushButton {
                background-color: #5371ff;
                color: #ffffff;
                font-size: 14px;
                padding: 10px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #3a5bff;
            }
            QListWidget, QTextEdit, QComboBox {
                background-color: #15171c;
                color: #ffffff;
                border: 1px solid #5371ff;
                font-size: 14px;
                border-radius: 5px;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
        """)
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Top Panel
        top_panel = QHBoxLayout()
        main_layout.addLayout(top_panel)
        top_panel.addStretch()
        top_panel.addWidget(QPushButton("Live Feed"))
        top_panel.addWidget(QPushButton("Train Model", clicked=self.train_model))
        top_panel.addStretch()

        # Left Panel
        left_panel = QVBoxLayout()
        self.camera_list = QListWidget()
        self.load_cameras()
        left_panel.addWidget(QPushButton("Add Camera", clicked=self.open_add_camera_dialog))
        left_panel.addWidget(self.camera_list)

        grid_options = QComboBox()
        grid_options.addItems(["2X2", "4x4"])
        grid_options.currentTextChanged.connect(self.change_grid_view)
        left_panel.addWidget(QLabel("Grid View:"))
        left_panel.addWidget(grid_options)

        # Middle Section
        middle_section = QHBoxLayout()
        main_layout.addLayout(middle_section)
        middle_section.addLayout(left_panel)

        # Middle Grid (Video Feeds)
        self.middle_panel = QGridLayout()
        self.update_grid_view(2)
        middle_section.addLayout(self.middle_panel, stretch=5)

        # Right Panel
        right_panel = QVBoxLayout()
        load_button = QPushButton("Load Camera")
        load_button.clicked.connect(self.load_cameras)
        right_panel.addWidget(load_button)

        self.activity_log = QTextEdit()
        self.activity_log.setReadOnly(True)
        self.activity_log.setPlaceholderText("Activity Log")
        right_panel.addWidget(self.activity_log)
        
        middle_section.addLayout(right_panel, stretch=2)

        # Bottom Panel
        bottom_panel = QHBoxLayout()
        bottom_panel.addWidget(QPushButton("Add Known Person"))
        user_button = QPushButton("User")
        user_button.clicked.connect(self.show_user_data)
        bottom_panel.addWidget(user_button)

        logs_button = QPushButton("Daily Logs")
        logs_button.clicked.connect(self.show_daily_logs)
        bottom_panel.addWidget(logs_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.exit_app)
        bottom_panel.addWidget(self.exit_button)
        main_layout.addLayout(bottom_panel)

    def exit_app(self):
        self.close()

    def closeEvent(self, event):
        for i in range(self.middle_panel.count()):
            widget = self.middle_panel.itemAt(i).widget()
            if isinstance(widget, CameraStream):
                widget.closeEvent(event)
        event.accept()

    def open_add_camera_dialog(self):
        dialog = AddCameraDialog()
        dialog.exec_()

    def load_cameras(self):
        try:
            if not os.path.exists(CAMERA_CSV):
                QMessageBox.warning(self, "File Not Found", "No camera data found. Please ensure the file exists at 'data/camera.csv'.")
                return

            df = pd.read_csv(CAMERA_CSV)
            self.camera_list.clear()

            for _, row in df.iterrows():
                camera_name = row["Camera Name"]
                ip_address = row["IP Address"] if pd.notna(row["IP Address"]) else "No IP"
                self.camera_list.addItem(f"{camera_name} ({ip_address})")
        except Exception as e:
            logging.error(f"Error loading cameras: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load cameras: {str(e)}")

    def change_grid_view(self, text):
        size = 2 if text == "2X2" else 4
        self.update_grid_view(size)

    def update_grid_view(self, size):
        try:
            while self.middle_panel.count():
                item = self.middle_panel.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            self.current_grid_size = size
            camera_ips = [self.camera_list.item(i).text().split("(")[-1].rstrip(")") for i in range(self.camera_list.count())]
            
            for i in range(size):
                for j in range(size):
                    idx = i * size + j
                    if idx < len(camera_ips):
                        try:
                            cam_feed = CameraStreamFactory.create_camera_stream(camera_ips[idx])
                            self.middle_panel.addWidget(cam_feed, i, j)
                        except ValueError as e:
                            logging.error(f"Error creating camera stream: {str(e)}")
                            QMessageBox.warning(self, "Error", str(e))
                    else:
                        placeholder = QLabel("No Feed")
                        placeholder.setAlignment(Qt.AlignCenter)
                        placeholder.setStyleSheet("background-color: black; color: white;")
                        self.middle_panel.addWidget(placeholder, i, j)
        except Exception as e:
            logging.error(f"Error updating grid view: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to update grid view: {str(e)}")

    def train_model(self):
        try:
            images, labels = [], []
            label_map = {}

            if not os.path.exists(DATA_PATH):
                QMessageBox.critical(self, "Error", "Training images folder not found! Please add images to 'data/training_images'.")
                return

            person_folders = [d for d in os.listdir(DATA_PATH) if os.path.isdir(os.path.join(DATA_PATH, d))]
            if not person_folders:
                QMessageBox.critical(self, "Error", "No person folders found in training data! Please add images to 'data/training_images'.")
                return

            for label, person in enumerate(person_folders):
                person_path = os.path.join(DATA_PATH, person)
                label_map[label] = person

                img_files = [f for f in os.listdir(person_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

                if not img_files:
                    QMessageBox.warning(self, "Warning", f"No images found for '{person}'. Skipping...")
                    continue

                for img_name in img_files:
                    img_path = os.path.join(person_path, img_name)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

                    if img is None:
                        QMessageBox.warning(self, "Warning", f"Could not read image: {img_name}. Skipping...")
                        continue

                    images.append(img)
                    labels.append(label)

            if images:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.train(images, np.array(labels))
                os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
                recognizer.write(MODEL_PATH)
                self.activity_log.append("✅ Model trained successfully!")
            else:
                QMessageBox.critical(self, "Error", "No valid images found for training!")
                self.activity_log.append("❌ No valid images found for training.")
        except Exception as e:
            logging.error(f"Error training model: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to train model: {str(e)}")

    def show_user_data(self):
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("User Data")
            dialog.setGeometry(100, 100, 800, 400)
            dialog.setStyleSheet("background-color: #15171c; color: #ffffff;")

            layout = QVBoxLayout()
            dialog.setLayout(layout)

            table = QTableWidget()
            table.setStyleSheet("""
                QTableWidget {
                    background-color: #15171c;
                    color: #ffffff;
                    gridline-color: #5371ff;
                }
                QHeaderView::section {
                    background-color: #5371ff;
                    color: #ffffff;
                    padding: 5px;
                    border: none;
                }
            """)
            layout.addWidget(table)

            csv_file = "data/user_data_store.csv"
            if not os.path.exists(csv_file):
                QMessageBox.warning(self, "File Not Found", "User data file not found. Please ensure the file exists at 'data/user_data_store.csv'.")
                return

            df = pd.read_csv(csv_file)
            table.setRowCount(len(df))
            table.setColumnCount(len(df.columns))
            table.setHorizontalHeaderLabels(df.columns)

            for i, row in df.iterrows():
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, j, item)

            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.verticalHeader().setVisible(False)
            dialog.exec_()
        except Exception as e:
            logging.error(f"Error showing user data: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to show user data: {str(e)}")

    def show_daily_logs(self):
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Daily Logs")
            dialog.setGeometry(100, 100, 800, 400)
            dialog.setStyleSheet("background-color: #15171c; color: #ffffff;")

            layout = QVBoxLayout()
            dialog.setLayout(layout)

            table = QTableWidget()
            table.setStyleSheet("""
                QTableWidget {
                    background-color: #15171c;
                    color: #ffffff;
                    gridline-color: #5371ff;
                }
                QHeaderView::section {
                    background-color: #5371ff;
                    color: #ffffff;
                    padding: 5px;
                    border: none;
                }
            """)
            layout.addWidget(table)

            csv_file = "data/logs.csv"
            if not os.path.exists(csv_file):
                QMessageBox.warning(self, "File Not Found", "Logs file not found. Please ensure the file exists at 'data/logs.csv'.")
                return

            df = pd.read_csv(csv_file)
            table.setRowCount(len(df))
            table.setColumnCount(len(df.columns))
            table.setHorizontalHeaderLabels(df.columns)

            for i, row in df.iterrows():
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, j, item)

            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.verticalHeader().setVisible(False)
            dialog.exec_()
        except Exception as e:
            logging.error(f"Error showing daily logs: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to show daily logs: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = UserDashboard()
    dashboard.show()
    sys.exit(app.exec_())