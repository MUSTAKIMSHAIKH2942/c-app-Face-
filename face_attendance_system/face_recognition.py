import os
import cv2
import pickle
import numpy as np
import csv
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QScrollArea, QMessageBox, QFileDialog, QLineEdit, QDialog, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPainterPath

# Set up paths
haarcascade_path = "haarcascade_frontalface_default.xml"
trainimage_path = "Training_images"
userdetails_path = "UserDetails/users.csv"
attendance_path = "Attendance"

class FaceRecognition:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + haarcascade_path)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.label_names = {}
        self.load_model()

    def load_model(self):
        if os.path.exists("trained_model.yml"):
            self.recognizer.read("trained_model.yml")
            with open("label_names.pkl", "rb") as f:
                self.label_names = pickle.load(f)

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return gray, faces

    def recognize_faces(self, gray, faces):
        recognized_faces = []
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (200, 200))
            label_id, confidence = self.recognizer.predict(face_resized)
            person_name = self.label_names.get(label_id, "Unknown")
            recognized_faces.append((x, y, w, h, person_name, confidence))
        return recognized_faces

    def update_frame(self, frame):
        gray, faces = self.detect_faces(frame)
        recognized_faces = self.recognize_faces(gray, faces)
        for (x, y, w, h, person_name, confidence) in recognized_faces:
            color = (0, 255, 0) if person_name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"{person_name} ({confidence:.2f})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        return frame

class VideoCaptureThread(QThread):
    update_frame_signal = pyqtSignal(QPixmap)

    def __init__(self, camera_index):
        super().__init__()
        self.camera_index = camera_index
        self.face_recognition = FaceRecognition()

    def run(self):
        cap = cv2.VideoCapture(self.camera_index)
        while not self.isInterruptionRequested():
            ret, frame = cap.read()
            if ret:
                frame = self.face_recognition.update_frame(frame)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.update_frame_signal.emit(QPixmap.fromImage(qt_image))
        cap.release()

class DashboardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognition System")
        self.setGeometry(100, 100, 1200, 800)
        self.cameras = []
        self.camera_threads = {}
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.video_grid_layout = QGridLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.video_grid_widget = QWidget()
        self.video_grid_widget.setLayout(self.video_grid_layout)
        self.scroll_area.setWidget(self.video_grid_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.add_camera_button = QPushButton("Add Camera")
        self.add_camera_button.clicked.connect(self.add_camera)
        self.main_layout.addWidget(self.add_camera_button)

    def add_camera(self):
        camera_index = len(self.cameras)
        self.cameras.append(camera_index)
        self.start_camera_thread(camera_index)

    def start_camera_thread(self, camera_index):
        video_widget = QLabel(self)
        video_widget.setAlignment(Qt.AlignCenter)
        video_widget.setStyleSheet("background-color: black;")
        self.video_grid_layout.addWidget(video_widget, len(self.cameras) // 2, len(self.cameras) % 2)

        camera_thread = VideoCaptureThread(camera_index)
        camera_thread.update_frame_signal.connect(video_widget.setPixmap)
        camera_thread.start()
        self.camera_threads[camera_index] = camera_thread

if __name__ == "__main__":
    app = QApplication([])
    window = DashboardApp()
    window.show()
    app.exec_()