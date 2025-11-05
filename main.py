"""
TalkingMask-Pi5 - Main entry point for Bob the animatronic mask.
Orchestrates voice interaction, GPT responses, servo control, and face tracking.
"""

from config_loader import load_config
from gpt_assistant import GPTAssistant
from voice_assistant import VoiceAssistant
from tts_manager import TTSManager
from envelope_monitor import EnvelopeMonitor
from mouth_controller import MouthController
from eyes_controller import EyesController
from cam import WebcamStream
import time


def main():
    """Initialise and run the TalkingMask system."""
    config = load_config()

    # Initialise modules
    gpt = GPTAssistant(config)
    voice = VoiceAssistant(config)
    mouth = MouthController(config)
    tts = TTSManager(config, mouth_controller=mouth)
    envelope = EnvelopeMonitor(config)
    eyes = EyesController(config)
    cam = WebcamStream(eyes_controller=eyes)

    # Start background threads
    envelope.start()
    mouth.start()
    eyes.start()
    cam.start()

    try:
        print("Starting conversation loop...")
        while True:
            spoken = voice.listen()
            if spoken:
                print(f"You said: {spoken}")
                reply = gpt.ask(spoken)
                print(f"Replying: {reply}")
                tts.speak(reply)
            else:
                print("No input detected.")
                tts.speak("Can you repeat that?")

            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        # Clean shutdown of all threads
        envelope.stop()
        mouth.stop()
        eyes.stop()
        cam.stop()


if __name__ == "__main__":
    main()
