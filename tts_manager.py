import os
import tempfile
import numpy as np
import soundfile as sf
import sounddevice as sd
import subprocess

class TTSManager:
    def __init__(self, config, mouth_controller):
        self.engine_type = config["tts"]["engine"]
        self.voice_variant = config["tts"]["voice"]
        self.mouth = mouth_controller

        if self.engine_type == "coqui":
            from TTS.api import TTS
            model_name = {
                "female": "tts_models/en/ljspeech/tacotron2-DDC",
                "male": "tts_models/en/vctk/vits"
            }.get(self.voice_variant, "tts_models/en/ljspeech/tacotron2-DDC")
            self.tts = TTS(model_name=model_name)
        elif self.engine_type == "espeak":
            pass  # will use subprocess
        else:
            raise ValueError("Unsupported TTS engine.")

    def speak(self, text):
        if self.engine_type == "coqui":
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                self.tts.tts_to_file(text=text, file_path=f.name)
                self._play_and_sync(f.name)
                os.remove(f.name)

        elif self.engine_type == "espeak":
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                wav_path = f.name
            if self.voice_variant == "female":
                self.v_code = "f3"
            else:
                self.v_code = "m3"
            voice = f"en+{self.v_code}"
            subprocess.run(["espeak", "-v", voice, "-w", wav_path, text])
            self._play_and_sync(wav_path)
            os.remove(wav_path)

    def _play_and_sync(self, wav_file):
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

            # Envelope detection (RMS per chunk)
            rms = np.sqrt(np.mean(chunk ** 2))
            normalized = np.clip((rms - 0.005) / (0.1 - 0.005), 0.0, 1.0)
            self.mouth.update_envelope(normalized)

            i = end

        i = 0
        with sd.OutputStream(channels=1, samplerate=fs, callback=callback, blocksize=blocksize):
            sd.sleep(int(len(data) / fs * 1000))

        self.mouth.update_envelope(0.0)  # reset after speech
