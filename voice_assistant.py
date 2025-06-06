import speech_recognition as sr
import time

class VoiceAssistant:
    def __init__(self, config):
        self.recognizer = sr.Recognizer()
        self.listen_timeout = config.get("mic", {}).get("listen_timeout", 5)
        self.phrase_timeout = config.get("mic", {}).get("phrase_timeout", 5)
        self.device_index = config.get("mic", {}).get("device_index", 0)


    def _get_default_microphone(self):
        try:
            for idx, name in enumerate(sr.Microphone.list_microphone_names()):
                if "usb" in name.lower() or "mic" in name.lower():
                    return idx
        except Exception as e:
            print("Microphone detection failed:", e)
        return None

    def listen(self):
        try:
            with sr.Microphone(device_index=self.device_index) as source:
                print("?? Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=self.listen_timeout, phrase_time_limit=self.phrase_timeout)
                text = self.recognizer.recognize_google(audio)
                return text.lower()
        except sr.WaitTimeoutError:
            print("No speech detected.")
        except sr.UnknownValueError:
            print("Could not understand.")
        except Exception as e:
            print("Recognition error:", e)
        return ""
