"""Text-to-speech manager with mouth synchronisation."""

import os
import tempfile
import numpy as np
import soundfile as sf
import sounddevice as sd
import subprocess


class TTSManager:
    """Generates speech from text and synchronises mouth movement with audio."""

    def __init__(self, config, mouth_controller):
        """
        Initialise TTS manager with selected engine.

        Args:
            config: Configuration dictionary containing TTS settings
            mouth_controller: MouthController instance for synchronisation
        """
        self.engine_type = config["tts"]["engine"]
        self.voice_variant = config["tts"]["voice"]
        self.mouth = mouth_controller

        if self.engine_type == "coqui":
            try:
                from TTS.api import TTS
                model_name = {
                    "female": "tts_models/en/ljspeech/tacotron2-DDC",
                    "male": "tts_models/en/vctk/vits"
                }.get(self.voice_variant, "tts_models/en/ljspeech/tacotron2-DDC")
                self.tts = TTS(model_name=model_name)
            except ImportError:
                raise ImportError(
                    "Coqui TTS not installed. Either:\n"
                    "1. Install TTS: pip install TTS (requires Python < 3.13)\n"
                    "2. Change config.yaml tts.engine to 'espeak'"
                )
        elif self.engine_type == "espeak":
            pass  # Uses subprocess for synthesis
        else:
            raise ValueError("Unsupported TTS engine.")

    def speak(self, text):
        """
        Synthesise text to speech and play with mouth sync.

        Args:
            text: Text to convert to speech
        """
        if self.engine_type == "coqui":
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                self.tts.tts_to_file(text=text, file_path=f.name)
                self._play_and_sync(f.name)
                os.remove(f.name)

        elif self.engine_type == "espeak":
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                wav_path = f.name
            voice_code = "f3" if self.voice_variant == "female" else "m3"
            voice = f"en+{voice_code}"
            subprocess.run(["espeak", "-v", voice, "-w", wav_path, text])
            self._play_and_sync(wav_path)
            os.remove(wav_path)

    def _play_and_sync(self, wav_file):
        """
        Play audio file whilst synchronising mouth movement with envelope.

        Args:
            wav_file: Path to WAV file to play
        """
        data, fs = sf.read(wav_file, dtype='float32')
        blocksize = 1024

        def callback(outdata, frames, time_info, status):
            nonlocal data, i
            if status:
                print("Stream status:", status)

            end = i + frames
            chunk = data[i:end]
            if len(chunk) < frames:
                outdata[:len(chunk)] = chunk.reshape(-1, 1)
                outdata[len(chunk):] = 0
                raise sd.CallbackStop()
            else:
                outdata[:] = chunk.reshape(-1, 1)

            # Calculate audio envelope (RMS) and normalise to 0-1
            rms = np.sqrt(np.mean(chunk ** 2))
            normalised = np.clip((rms - 0.005) / (0.1 - 0.005), 0.0, 1.0)
            self.mouth.update_envelope(normalised)

            i = end

        i = 0
        with sd.OutputStream(channels=1, samplerate=fs, callback=callback, blocksize=blocksize):
            sd.sleep(int(len(data) / fs * 1000))

        self.mouth.update_envelope(0.0)  # Close mouth after speech
