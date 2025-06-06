import os
import tempfile
import subprocess
import pyttsx3

class TTSManager:
    def __init__(self, config):
        self.engine_type = config["tts"]["engine"]
        self.voice_variant = config["tts"]["voice"]
        self.tts = None

        if self.engine_type == "pyttsx3":
            self.tts = pyttsx3.init()
            self._set_pyttsx3_voice()
        elif self.engine_type == "espeak":
            pass  # Will use subprocess
        else:
            raise ValueError(f"Unsupported TTS engine: {self.engine_type}")

    def _set_pyttsx3_voice(self):
        # You can use this if you want to map f3/f7 to pyttsx3 voices (limited support)
        voices = self.tts.getProperty('voices')
        for v in voices:
            if self.voice_variant.lower() in v.id.lower():
                self.tts.setProperty('voice', v.id)
                return

    def speak(self, text):
        if self.engine_type == "pyttsx3":
            self.tts.say(text)
            self.tts.runAndWait()

        elif self.engine_type == "espeak":
            # Dynamically build voice string: en+f3 or en+f7 etc.
            if self.voice_variant == "female":
                self.v_code = "f3"
            else:
                self.v_code = "m3"
            voice = f"en+{self.v_code}"
            try:
                subprocess.run(["espeak", "-v", voice, text])
            except Exception as e:
                print("espeak subprocess error:", e)

