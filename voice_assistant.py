"""Speech recognition using Google Speech API."""

import speech_recognition as sr


class VoiceAssistant:
    """Captures and transcribes user speech via microphone."""

    def __init__(self, config):
        """
        Initialise voice assistant with microphone configuration.

        Args:
            config: Configuration dictionary containing microphone settings
        """
        self.recognizer = sr.Recognizer()
        self.listen_timeout = config.get("mic", {}).get("listen_timeout", 5)
        self.phrase_timeout = config.get("mic", {}).get("phrase_timeout", 5)
        self.device_index = config.get("mic", {}).get("device_index", 0)

    def listen(self):
        """
        Listen for user speech and convert to text.

        Returns:
            Lowercase transcribed text, or empty string if recognition fails
        """
        try:
            with sr.Microphone(device_index=self.device_index) as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(
                    source,
                    timeout=self.listen_timeout,
                    phrase_time_limit=self.phrase_timeout
                )
                text = self.recognizer.recognize_google(audio)
                return text.lower()
        except sr.WaitTimeoutError:
            print("No speech detected.")
        except sr.UnknownValueError:
            print("Could not understand.")
        except Exception as e:
            print("Recognition error:", e)
        return ""
