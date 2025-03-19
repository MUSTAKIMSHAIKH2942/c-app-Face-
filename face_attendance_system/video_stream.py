import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from face_recognition import FaceRecognition

class VideoStream(QThread):
    update_frame_signal = pyqtSignal(QPixmap)

    def __init__(self, camera_index, parent=None):
        super().__init__(parent)
        self.camera_index = camera_index
        self.running = True
        self.face_recognition = FaceRecognition()

    def run(self):
        cap = cv2.VideoCapture(self.camera_index)
        while self.running:
            ret, frame = cap.read()
            if ret:
                # Apply face recognition
                frame = self.face_recognition.update_frame_with_recognition(frame)

                # Convert frame to QPixmap for display
                height, width, channels = frame.shape
                bytes_per_line = channels * width
                qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
                pixmap = QPixmap.fromImage(qt_image)

                # Emit the updated frame
                self.update_frame_signal.emit(pixmap.scaled(640, 480, Qt.KeepAspectRatio))
            else:
                break
        cap.release()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        

