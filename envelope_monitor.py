import sounddevice as sd
import numpy as np
import threading
import time
import subprocess

class EnvelopeMonitor(threading.Thread):
    def __init__(self, config):
        super().__init__()
        self.min_env = config["envelope"]["min_threshold"]
        self.max_env = config["envelope"]["max_threshold"]
        self._envelope = 0.0
        self._stop_event = threading.Event()
        self.device_index = self._find_monitor_device()
        self.lock = threading.Lock()
        self.daemon = True

    def get_envelope(self):
        with self.lock:
            return self._envelope

    def _find_monitor_device(self):
        devices = sd.query_devices()
        for idx, dev in enumerate(devices):
            if 'pulse' in dev['name'].lower():
                return idx
        raise RuntimeError("No PulseAudio monitor source found.")

    def _callback(self, indata, frames, time_info, status):
        if status:
            print("Stream status:", status)
        rms = np.sqrt(np.mean(indata ** 2))
        normalized = np.clip((rms - self.min_env) / (self.max_env - self.min_env), 0.0, 1.0)
        with self.lock:
            self._envelope = normalized

    def stop(self):
        self._stop_event.set()

    def run(self):
        with sd.InputStream(device=self.device_index, channels=1,
                            callback=self._callback, samplerate=44100, blocksize=1024):
            while not self._stop_event.is_set():
                time.sleep(0.05)
