"""Software-based audio envelope monitor using PulseAudio."""

import sounddevice as sd
import numpy as np
import threading
import time


class EnvelopeMonitor(threading.Thread):
    """Monitors system audio output and calculates envelope for alternative mouth sync."""

    def __init__(self, config):
        """
        Initialise envelope monitor with threshold configuration.

        Args:
            config: Configuration dictionary containing envelope thresholds
        """
        super().__init__()
        self.min_env = config["envelope"]["min_threshold"]
        self.max_env = config["envelope"]["max_threshold"]
        self._envelope = 0.0
        self._stop_event = threading.Event()
        self.device_index = self._find_monitor_device()
        self.lock = threading.Lock()
        self.daemon = True

    def get_envelope(self):
        """
        Get current envelope value (thread-safe).

        Returns:
            Normalised envelope value (0.0 to 1.0)
        """
        with self.lock:
            return self._envelope

    def _find_monitor_device(self):
        """
        Locate PulseAudio monitor device for system audio capture.

        Returns:
            Device index for PulseAudio monitor

        Raises:
            RuntimeError: If no PulseAudio monitor found
        """
        devices = sd.query_devices()
        for idx, dev in enumerate(devices):
            if 'pulse' in dev['name'].lower():
                return idx
        raise RuntimeError("No PulseAudio monitor source found.")

    def _callback(self, indata, frames, time_info, status):
        """Audio stream callback: calculate and normalise RMS envelope."""
        if status:
            print("Stream status:", status)
        rms = np.sqrt(np.mean(indata ** 2))
        normalised = np.clip((rms - self.min_env) / (self.max_env - self.min_env), 0.0, 1.0)
        with self.lock:
            self._envelope = normalised

    def stop(self):
        """Stop the monitor thread."""
        self._stop_event.set()

    def run(self):
        """Main thread loop: capture audio and update envelope continuously."""
        with sd.InputStream(
            device=self.device_index,
            channels=1,
            callback=self._callback,
            samplerate=44100,
            blocksize=1024
        ):
            while not self._stop_event.is_set():
                time.sleep(0.05)
