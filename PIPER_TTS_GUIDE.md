# Piper TTS Guide for TalkingMask-Pi5

Complete guide for using Piper TTS on Raspberry Pi 5 with natural-sounding voices.

---

## Installation

```bash
cd ~/TalkingMask-Pi5
source venv/bin/activate
pip install piper-tts
```

---

## Downloading Voice Models

Piper requires downloading voice model files before use. Models are stored in `~/.local/share/piper/`.

### Method 1: Auto-download (Recommended)

```bash
# Install piper-tts command-line tool
pip install piper-tts

# Download a voice automatically
echo "Hello world" | piper --model en_GB-alan-medium --output_file test.wav
```

The first time you use a voice, it will be downloaded automatically.

### Method 2: Manual Download

Download from: https://huggingface.co/rhasspy/piper-voices/tree/main

For each voice, you need TWO files:
- `voice_name.onnx` - The neural network model
- `voice_name.onnx.json` - Configuration file

Place both files in the same directory.

---

## Available Voices

### English (British) - High Quality

| Voice | Gender | Quality | Size | Description |
|-------|--------|---------|------|-------------|
| `en_GB-alan-low` | Male | Low | 18 MB | Alan, British, basic quality |
| `en_GB-alan-medium` | Male | Medium | 63 MB | Alan, British, good quality |
| `en_GB-alba-medium` | Female | Medium | 31 MB | Alba, Scottish accent |
| `en_GB-northern_english_male-medium` | Male | Medium | 31 MB | Northern English accent |
| `en_GB-jenny_dioco-medium` | Female | Medium | 63 MB | Jenny, British, clear voice |
| `en_GB-cori-medium` | Female | Medium | 31 MB | Cori, British accent |
| `en_GB-southern_english_female-low` | Female | Low | 18 MB | Southern English accent |

### English (American) - High Quality

| Voice | Gender | Quality | Size | Description |
|-------|--------|---------|------|-------------|
| `en_US-lessac-low` | Female | Low | 18 MB | Judith Lessac style, basic |
| `en_US-lessac-medium` | Female | Medium | 63 MB | Judith Lessac, good quality |
| `en_US-lessac-high` | Female | High | 96 MB | Judith Lessac, excellent |
| `en_US-libritts-high` | Multiple | High | 94 MB | Various speakers |
| `en_US-amy-low` | Female | Low | 18 MB | Amy, American accent |
| `en_US-amy-medium` | Female | Medium | 63 MB | Amy, good quality |
| `en_US-kathleen-low` | Female | Low | 18 MB | Kathleen, American |
| `en_US-ryan-low` | Male | Low | 18 MB | Ryan, American |
| `en_US-ryan-medium` | Male | Medium | 63 MB | Ryan, good quality |
| `en_US-ryan-high` | Male | High | 96 MB | Ryan, excellent quality |
| `en_US-joe-medium` | Male | Medium | 63 MB | Joe, American accent |
| `en_US-kristin-medium` | Female | Medium | 31 MB | Kristin, clear voice |

### Other English Accents

| Voice | Gender | Quality | Size | Description |
|-------|--------|---------|------|-------------|
| `en_AU-news-medium` | Multiple | Medium | 63 MB | Australian newsreader |
| `en_IN-kumar-medium` | Male | Medium | 31 MB | Indian English accent |

### Recommended for TalkingMask

**For Female Voice (Bob's default):**
1. **`en_GB-alba-medium`** - Scottish female, natural and friendly (31 MB)
2. **`en_US-lessac-medium`** - American female, professional (63 MB)
3. **`en_GB-jenny_dioco-medium`** - British female, clear (63 MB)

**For Male Voice:**
1. **`en_GB-alan-medium`** - British male, warm tone (63 MB)
2. **`en_US-ryan-medium`** - American male, clear (63 MB)
3. **`en_US-joe-medium`** - American male, friendly (63 MB)

---

## Quick Test

### Test 1: Using Command Line

```bash
# British female (Alba - Scottish)
echo "Hello, I am Bob the talking mask" | piper \
  --model en_GB-alba-medium \
  --output_file test_alba.wav

# Play the result
aplay test_alba.wav

# American female (Lessac)
echo "Hello, I am Bob the talking mask" | piper \
  --model en_US-lessac-medium \
  --output_file test_lessac.wav

aplay test_lessac.wav
```

### Test 2: Using Python

```python
from piper import PiperVoice
import os

# Download and cache voice (first time only)
voice = PiperVoice.load("en_GB-alba-medium")

# Generate speech to file
with open("output.wav", "wb") as f:
    # Note: synthesize (US spelling), not synthesise
    voice.synthesize("Hello, I am Bob the talking mask", f)

# Play the audio
os.system("aplay output.wav")
```

**Important**: The method is `synthesize` (US spelling), not `synthesise` (UK spelling)!

### Test 3: Try Multiple Voices

```bash
cd ~/TalkingMask-Pi5
source venv/bin/activate

# British female (Alba - Scottish)
python3 << 'EOF'
from piper import PiperVoice

voice = PiperVoice.load("en_GB-alba-medium")
with open("alba.wav", "wb") as f:
    voice.synthesize("Hello, I am Bob the talking mask", f)
print("Generated: alba.wav")
EOF

# American female (Lessac)
python3 << 'EOF'
from piper import PiperVoice

voice = PiperVoice.load("en_US-lessac-medium")
with open("lessac.wav", "wb") as f:
    voice.synthesize("Hello, I am Bob the talking mask", f)
print("Generated: lessac.wav")
EOF

# British male (Alan)
python3 << 'EOF'
from piper import PiperVoice

voice = PiperVoice.load("en_GB-alan-medium")
with open("alan.wav", "wb") as f:
    voice.synthesize("Hello, I am Bob the talking mask", f)
print("Generated: alan.wav")
EOF

# Play all three
aplay alba.wav
sleep 1
aplay lessac.wav
sleep 1
aplay alan.wav
```

---

## Performance on Raspberry Pi 5

| Quality | Size | Speed on Pi 5 | Recommendation |
|---------|------|---------------|----------------|
| Low | ~18 MB | Very fast (5x real-time) | Good for testing |
| Medium | ~31-63 MB | Fast (2-3x real-time) | **Recommended** |
| High | ~96 MB | Moderate (1-2x real-time) | Still usable |

**Medium quality** models are the sweet spot for Pi 5 - excellent voice quality with fast generation.

---

## GPU Warning (Harmless)

You may see this warning - it's safe to ignore on Pi 5:
```
GPU device discovery failed: ReadFileContents Failed to open file: "/sys/class/drm/card1/device/vendor"
```

This just means Piper is using CPU (which is correct for Pi 5).

---

## Voice Model Locations

After downloading, models are stored in:
```
~/.local/share/piper/
  ├── en_GB-alba-medium.onnx
  ├── en_GB-alba-medium.onnx.json
  ├── en_US-lessac-medium.onnx
  ├── en_US-lessac-medium.onnx.json
  └── ...
```

---

## Advanced Usage: Real-time Streaming

For low-latency, chunk-based generation:

```python
from piper import PiperVoice
import sounddevice as sd
import numpy as np

voice = PiperVoice.load("en_GB-alba-medium")

# Generate audio chunks
audio_data = []
for audio_chunk in voice.synthesize_stream_raw("Hello, this is streaming audio"):
    audio_data.extend(audio_chunk)

# Convert to numpy array and play
audio_array = np.array(audio_data, dtype=np.int16)
sd.play(audio_array, voice.config.sample_rate)
sd.wait()
```

---

## Comparison with Other TTS

| Engine | Quality | Speed (Pi 5) | Offline | Python 3.13 |
|--------|---------|--------------|---------|-------------|
| eSpeak | ⭐ | ⚡⚡⚡⚡⚡ | ✅ | ✅ |
| Piper | ⭐⭐⭐⭐ | ⚡⚡⚡⚡ | ✅ | ✅ |
| Coqui TTS | ⭐⭐⭐⭐ | ⚡⚡ | ✅ | ❌ |
| gTTS | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | ❌ | ✅ |
| Bark | ⭐⭐⭐⭐⭐ | ⚡ | ✅ | ✅ |

**Piper** offers the best balance for real-time embedded systems.

---

## Full Voice List

For the complete list of all available voices (100+ languages):
https://github.com/rhasspy/piper/blob/master/VOICES.md

Or explore voices at:
https://rhasspy.github.io/piper-samples/

---

## Troubleshooting

### Voice file not found

Make sure both files are downloaded:
```bash
ls ~/.local/share/piper/en_GB-alba-medium*
# Should show:
# en_GB-alba-medium.onnx
# en_GB-alba-medium.onnx.json
```

### Slow generation

- Use `medium` quality instead of `high`
- Ensure Pi 5 is not thermally throttling
- Close other applications

### Audio playback issues

Test with system audio first:
```bash
speaker-test -t wav -c 2
```

---

## Next Steps

To integrate Piper into TalkingMask, you would:
1. Choose a voice (e.g., `en_GB-alba-medium`)
2. Add `piper` option to `config.yaml`
3. Update `tts_manager.py` to support Piper engine
4. Test with full system

Would you like me to implement Piper TTS integration into your TalkingMask code?
