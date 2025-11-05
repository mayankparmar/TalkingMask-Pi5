#!/bin/bash

echo "Updating package index..."
sudo apt update

echo "Installing system dependencies..."
sudo apt install -y python3-dev build-essential libasound2-dev portaudio19-dev \
    python3-pyaudio espeak espeak-ng espeak-ng-data libatlas-base-dev libffi-dev \
    libsndfile1 libportaudio2 ffmpeg sox \
    i2c-tools python3-smbus lgpio python3-lgpio

echo "Creating virtual environment with system site packages..."
python3 -m venv --system-site-packages venv
source venv/bin/activate

echo "Installing Python packages..."
pip install --upgrade pip

# Install packages individually, skipping lgpio (using system package)
echo "Installing Python dependencies (using system lgpio)..."
pip install sounddevice soundfile numpy pyttsx3 PyYAML openai speechrecognition adafruit-circuitpython-servokit

# Try to install TTS (Coqui) - only works on Python < 3.13
echo "Attempting to install Coqui TTS (optional, for neural voices)..."
pip install TTS 2>/dev/null && echo "✓ TTS installed" || echo "⚠ TTS skipped (requires Python < 3.13). Using eSpeak instead."

echo "Verifying lgpio installation..."
python3 -c "import lgpio; print('✓ lgpio is accessible from system packages')" || {
    echo "⚠ Warning: lgpio not found. Installing via pip..."
    sudo apt install -y swig
    pip install lgpio
}

echo "All done! Virtual environment ready."
echo "To activate: source venv/bin/activate"
