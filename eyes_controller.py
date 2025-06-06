import threading
import time
from adafruit_servokit import ServoKit

class EyesController(threading.Thread):
    def __init__(self, config):
        super().__init__()
        self.channel = config["eyes"]["channel"]
        self.min_angle = config["eyes"]["min_angle"]
        self.max_angle = config["eyes"]["max_angle"]
        self.smoothing = config["eyes"].get("smoothing", 0.3)

        self.kit = ServoKit(channels=16)
        self._stop_event = threading.Event()
        self._target_angle = 0
        self._current_angle = 0

        self.daemon = True

    def set_eyes_setpoint(self, angle):
        self._target_angle = max(self.min_angle, min(self.max_angle, angle))

    def run(self):
        while not self._stop_event.is_set():
            self._current_angle += self.smoothing * (self._target_angle - self._current_angle)
            self.kit.servo[self.channel].angle = self._current_angle
            time.sleep(0.05)

    def stop(self):
        self._stop_event.set()
        self.kit.servo[self.channel].angle = None
