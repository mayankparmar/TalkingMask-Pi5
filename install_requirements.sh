#!/bin/bash

echo "Updating package index..."
sudo apt update

echo "Installing system dependencies..."
sudo apt install -y python3-dev build-essential libasound2-dev portaudio19-dev \
    python3-pyaudio espeak espeak-ng espeak-ng-data libatlas-base-dev libffi-dev \
    libsndfile1 libportaudio2 ffmpeg sox flac \
    i2c-tools python3-smbus swig liblgpio-dev

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Upgrading build tools..."
pip install --upgrade pip wheel setuptools

echo "Installing lgpio from source..."
pip install --no-binary=:all: lgpio

echo "Installing core Python dependencies..."
pip install sounddevice soundfile pyaudio numpy pyttsx3 PyYAML openai speechrecognition adafruit-circuitpython-servokit opencv-python piper-tts

# Try to install TTS (Coqui) - only works on Python < 3.13
echo ""
echo "Attempting to install Coqui TTS (optional)..."
pip install TTS 2>/dev/null && echo "✓ Coqui TTS installed successfully" || echo "⚠ Coqui TTS skipped (requires Python < 3.13)"
echo ""
echo "✓ Piper TTS installed (default TTS engine)"
echo "  Download voices to models/piper/ directory"
echo "  See PIPER_TTS_GUIDE.md for voice options and download instructions"

echo "Verifying lgpio installation..."
python3 -c "import lgpio; print('✓ lgpio installed successfully')" || {
    echo "⚠ Warning: lgpio verification failed!"
    exit 1
}

echo ""
echo "========================================"
echo "Downloading Piper TTS Voice Models"
echo "========================================"
echo ""

VOICE_DIR="models/piper"
mkdir -p "$VOICE_DIR"

echo "Downloading 3 high-quality voices to: $VOICE_DIR"
echo "Total size: ~157 MB"
echo ""

cd "$VOICE_DIR"

# Alba - Scottish female (medium) - DEFAULT
echo "[1/3] Downloading en_GB-alba-medium (Scottish female, 31MB)..."
wget -q --show-progress https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx
wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json
ln -sf en_GB-alba-medium.onnx.json en_GB-alba-medium.json
echo "✓ Alba (Scottish female) downloaded"
echo ""

# Alan - British male (medium)
echo "[2/3] Downloading en_GB-alan-medium (British male, 63MB)..."
wget -q --show-progress https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/medium/en_GB-alan-medium.onnx
wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/medium/en_GB-alan-medium.onnx.json
ln -sf en_GB-alan-medium.onnx.json en_GB-alan-medium.json
echo "✓ Alan (British male) downloaded"
echo ""

# Lessac - American female (medium)
echo "[3/3] Downloading en_US-lessac-medium (American female, 63MB)..."
wget -q --show-progress https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
ln -sf en_US-lessac-medium.onnx.json en_US-lessac-medium.json
echo "✓ Lessac (American female) downloaded"
echo ""

cd ~/TalkingMask-Pi5

echo "========================================"
echo "✓ Installation Complete!"
echo "========================================"
echo ""
echo "All dependencies installed:"
echo "  ✓ System packages"
echo "  ✓ Python packages (including piper-tts)"
echo "  ✓ Piper TTS voices (3 voices in models/piper/)"
echo "  ✓ lgpio verified"
echo ""
echo "Default voice: en_GB-alba-medium (Scottish female)"
echo ""
echo "To run TalkingMask:"
echo "  1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'"
echo "  2. Activate virtual environment: source venv/bin/activate"
echo "  3. Run: python3 main.py"
echo ""
echo "See README.md for more information."
echo ""
