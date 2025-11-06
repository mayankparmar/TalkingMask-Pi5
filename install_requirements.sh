#!/bin/bash

echo "Updating package index..."
sudo apt update

echo "Installing system dependencies..."
sudo apt install -y python3-dev build-essential libasound2-dev portaudio19-dev \
    python3-pyaudio espeak espeak-ng espeak-ng-data libatlas-base-dev libffi-dev \
    libsndfile1 libportaudio2 ffmpeg sox \
    i2c-tools python3-smbus swig liblgpio-dev

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Upgrading build tools..."
pip install --upgrade pip wheel setuptools

echo "Installing lgpio from source..."
pip install --no-binary=:all: lgpio

echo "Installing core Python dependencies..."
pip install sounddevice soundfile numpy pyttsx3 PyYAML openai speechrecognition adafruit-circuitpython-servokit

# Try to install TTS (Coqui) - only works on Python < 3.13
echo "Attempting to install Coqui TTS (optional, for neural voices)..."
pip install TTS 2>/dev/null && echo "✓ TTS installed" || echo "⚠ TTS skipped (requires Python < 3.13). Using eSpeak instead."

echo "Verifying lgpio installation..."
python3 -c "import lgpio; print('✓ lgpio installed successfully')" || {
    echo "⚠ Warning: lgpio verification failed!"
    exit 1
}

echo "All done! Virtual environment ready."
echo "To activate: source venv/bin/activate"
