"""Mouth servo controller with audio envelope synchronisation."""

import threading
import time
from adafruit_servokit import ServoKit


class MouthController(threading.Thread):
    """Controls mouth servo via PCA9685, synchronising with audio envelope."""

    def __init__(self, config):
        """
        Initialise mouth controller with servo configuration.

        Args:
            config: Configuration dictionary containing mouth servo settings
        """
        super().__init__()
        self.channel = config["mouth"]["channel"]
        self.closed_angle = config["mouth"]["closed_angle"]
        self.open_angle = config["mouth"]["open_angle"]
        self.direction = config["mouth"]["open_direction"]
        self.smoothing = config["mouth"].get("smoothing", 0.2)

        self.kit = ServoKit(channels=16)  # PCA9685 PWM controller
        self._stop_event = threading.Event()
        self._target_envelope = 0.0
        self._current_angle = self.closed_angle

        self.daemon = True

    def update_envelope(self, value):
        """
        Update target envelope value from audio signal.

        Args:
            value: Normalised envelope value (0.0 to 1.0)
        """
        self._target_envelope = max(0.0, min(1.0, value))

    def stop(self):
        """Stop the controller thread and release servo."""
        self._stop_event.set()
        self.kit.servo[self.channel].angle = None

    def run(self):
        """Main thread loop: smoothly update servo angle based on envelope."""
        while not self._stop_event.is_set():
            target_angle = self._envelope_to_angle(self._target_envelope)
            # Exponential moving average for smooth motion
            self._current_angle += self.smoothing * (target_angle - self._current_angle)
            self.kit.servo[self.channel].angle = self._current_angle
            time.sleep(0.05)

    def _envelope_to_angle(self, envelope):
        """
        Map envelope value (0-1) to servo angle range.

        Args:
            envelope: Normalised audio envelope (0.0 = closed, 1.0 = open)

        Returns:
            Servo angle in degrees
        """
        if self.direction == "positive":
            return self.closed_angle + envelope * (self.open_angle - self.closed_angle)
        else:
            return self.closed_angle - envelope * (self.closed_angle - self.open_angle)
