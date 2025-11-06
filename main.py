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
import speech_recognition as sr
import time


def detect_microphone():
    """
    Automatically detect and select the correct microphone.
    Looks for devices with 'Logitech' or 'Webcam' in the name.

    Returns:
        int: Device index of the detected microphone, or None if not found
    """
    print("Detecting microphone devices...")

    microphones = sr.Microphone.list_microphone_names()

    # Display all available microphones
    print(f"\nAvailable audio input devices ({len(microphones)} found):")
    for idx, name in enumerate(microphones):
        print(f"  [{idx}] {name}")

    # Search for Logitech or Webcam devices
    print("\nSearching for Logitech or Webcam microphones...")

    for idx, name in enumerate(microphones):
        name_lower = name.lower()
        if 'logitech' in name_lower or 'webcam' in name_lower:
            print(f"✓ Found suitable microphone: [{idx}] {name}")
            return idx

    print("⚠ No Logitech or Webcam microphone found.")
    print("  Will use default microphone from config.yaml")
    return None


def main():
    """Initialise and run the TalkingMask system."""
    config = load_config()

    # Auto-detect microphone
    detected_mic = detect_microphone()
    if detected_mic is not None:
        config["mic"]["device_index"] = detected_mic
        print(f"\nUsing microphone device index: {detected_mic}")
    else:
        print(f"\nUsing configured microphone device index: {config['mic']['device_index']}")

    print("\nInitialising TalkingMask components...")

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
        print("\n" + "="*50)
        print("TalkingMask is ready!")
        print("="*50)
        print("Starting conversation loop...\n")

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
        print("\n\nStopped by user.")
    finally:
        # Clean shutdown of all threads
        print("Shutting down...")
        envelope.stop()
        mouth.stop()
        eyes.stop()
        cam.stop()
        print("✓ TalkingMask stopped cleanly.")


if __name__ == "__main__":
    main()
