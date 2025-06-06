import cv2
import threading
import numpy as np

class WebcamStream(threading.Thread):
    def __init__(self, eyes_controller, frame_rate=5):
        super().__init__()
        self.eyes_controller = eyes_controller
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FPS, frame_rate)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.running = False
        self.daemon = True

    def run(self):
        self.running = True
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_center_x = x + w // 2
                frame_center_x = frame.shape[1] // 2
                offset = face_center_x - frame_center_x

                # Map offset to angle
                angle = np.interp(offset, [-200, 200], [-90, 90])
                self.eyes_controller.set_eyes_setpoint(angle)

        self.capture.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False
