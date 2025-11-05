"""Webcam face detection for eye tracking."""

import cv2
import threading
import numpy as np


class WebcamStream(threading.Thread):
    """Captures webcam video and tracks faces to control eye servo."""

    def __init__(self, eyes_controller, frame_rate=5):
        """
        Initialise webcam stream with face detection.

        Args:
            eyes_controller: EyesController instance to update with face position
            frame_rate: Target frame rate for video capture (default: 5 FPS)
        """
        super().__init__()
        self.eyes_controller = eyes_controller
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FPS, frame_rate)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.running = False
        self.daemon = True

    def run(self):
        """Main thread loop: detect faces and update eye servo position."""
        self.running = True
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                continue

            # Detect faces using Haar Cascade
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=5)

            if len(faces) > 0:
                # Track the first detected face
                x, y, w, h = faces[0]
                face_centre_x = x + w // 2
                frame_centre_x = frame.shape[1] // 2
                offset = face_centre_x - frame_centre_x

                # Map horizontal offset to servo angle
                angle = np.interp(offset, [-200, 200], [-90, 90])
                self.eyes_controller.set_eyes_setpoint(angle)

        self.capture.release()
        cv2.destroyAllWindows()

    def stop(self):
        """Stop the webcam stream."""
        self.running = False
