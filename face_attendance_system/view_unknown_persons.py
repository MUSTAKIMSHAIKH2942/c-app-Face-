import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class UnknownPersonsViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unknown Persons Data")
        self.setGeometry(150, 150, 600, 500)
        self.setStyleSheet("background-color: white;")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Unknown Persons Log")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.title_label)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.list_widget)

        self.load_unknown_persons()

        self.setLayout(layout)

    def load_unknown_persons(self):
        folder_path = "unknown_persons/"  # Adjust folder path if necessary
        if not os.path.exists(folder_path):
            QMessageBox.warning(self, "No Data", "Unknown persons folder does not exist.")
            return

        images = sorted(os.listdir(folder_path), reverse=True)  # Latest images first
        if not images:
            QMessageBox.information(self, "No Records", "No unknown persons detected.")
            return

        for img_file in images:
            if img_file.endswith((".png", ".jpg", ".jpeg")):
                timestamp = img_file.replace("unknown_", "").replace(".jpg", "").replace(".png", "").replace(".jpeg", "")
                formatted_time = f"Timestamp: {timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[9:11]}:{timestamp[11:13]}:{timestamp[13:]}"
                
                item = QListWidgetItem(formatted_time)
                item.setTextAlignment(Qt.AlignCenter)

                self.list_widget.addItem(item)

    def show_viewer(self):
        self.show()


def view_unknown_persons(self):
    self.viewer = UnknownPersonsViewer()
    self.viewer.show()
