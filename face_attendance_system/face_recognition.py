import cv2
import os
import numpy as np

face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return frame

def train_faces():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = "dataset/"
    faces, ids = [], []

    for file in os.listdir(path):
        img = cv2.imread(f"{path}/{file}", cv2.IMREAD_GRAYSCALE)
        faces.append(img)
        ids.append(int(file.split("_")[0]))

    recognizer.train(faces, np.array(ids))
    recognizer.save("models/trained_face_model.yml")
