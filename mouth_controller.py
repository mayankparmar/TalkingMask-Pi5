import threading
import time
from adafruit_servokit import ServoKit

class MouthController(threading.Thread):
    def __init__(self, config):
        super().__init__()
        self.channel = config["mouth"]["channel"]
        self.closed_angle = config["mouth"]["closed_angle"]
        self.open_angle = config["mouth"]["open_angle"]
        self.direction = config["mouth"]["open_direction"]
        self.smoothing = config["mouth"].get("smoothing", 0.2)

        self.kit = ServoKit(channels=16)
        self._stop_event = threading.Event()
        self._target_envelope = 0.0
        self._current_angle = self.closed_angle

        self.daemon = True  # optional: exits with main thread

    def update_envelope(self, value):
        self._target_envelope = max(0.0, min(1.0, value))  # clamp

    def stop(self):
        self._stop_event.set()
        self.kit.servo[self.channel].angle = None

    def run(self):
        while not self._stop_event.is_set():
            # Smooth transition using exponential moving average
            target_angle = self._envelope_to_angle(self._target_envelope)
            self._current_angle += self.smoothing * (target_angle - self._current_angle)
            self.kit.servo[self.channel].angle = self._current_angle
            time.sleep(0.05)

    def _envelope_to_angle(self, envelope):
        # Map [0, 1] envelope to angle span
        if self.direction == "positive":
            return self.closed_angle + envelope * (self.open_angle - self.closed_angle)
        else:
            return self.closed_angle - envelope * (self.closed_angle - self.open_angle)
