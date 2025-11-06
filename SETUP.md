# TalkingMask-Pi5 Setup Guide

Complete setup instructions for running TalkingMask on a fresh Raspberry Pi 5.

---

## Table of Contents

1. [Initial Raspberry Pi Setup](#1-initial-raspberry-pi-setup)
2. [System Dependencies](#2-system-dependencies)
3. [Hardware Setup](#3-hardware-setup)
4. [Clone Repository](#4-clone-repository)
5. [Python Environment](#5-python-environment)
6. [Configuration](#6-configuration)
7. [Testing](#7-testing)
8. [Running TalkingMask](#8-running-talkingmask)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Initial Raspberry Pi Setup

### Flash Raspberry Pi OS

1. Download **Raspberry Pi Imager**: https://www.raspberrypi.com/software/
2. Flash **Raspberry Pi OS (64-bit)** to your microSD card
3. Enable SSH (optional): Create empty file named `ssh` in boot partition
4. Configure Wi-Fi (optional): Create `wpa_supplicant.conf` in boot partition

### First Boot

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install basic tools
sudo apt install -y git vim curl wget build-essential
```

---

## 2. System Dependencies

### Install Required System Packages

```bash
# Audio libraries
sudo apt install -y libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0

# OpenCV dependencies
sudo apt install -y python3-opencv libopencv-dev

# eSpeak TTS engine
sudo apt install -y espeak espeak-data

# FFmpeg and SoX (audio processing)
sudo apt install -y ffmpeg sox libsox-fmt-all

# Python development headers
sudo apt install -y python3-dev python3-pip python3-venv

# I2C tools (for PCA9685)
sudo apt install -y i2c-tools python3-smbus

# GPIO library build dependencies (required for Raspberry Pi 5)
sudo apt install -y swig liblgpio-dev
```

### Enable I2C Interface

The PCA9685 servo controller uses I2C communication:

```bash
# Enable I2C
sudo raspi-config
# Navigate to: Interface Options -> I2C -> Enable

# Verify I2C is enabled
ls /dev/i2c*
# Should show: /dev/i2c-1 (or similar)

# Reboot to apply changes
sudo reboot
```

---

## 3. Hardware Setup

### Components Required

- **Raspberry Pi 5**
- **PCA9685 16-Channel PWM Servo Driver**
- **2x Servo Motors** (for mouth and eyes)
- **USB Webcam**
- **USB Microphone** (or USB audio adapter with mic)
- **Speaker/Audio Output**
- **Power Supply** (5V 5A recommended for Pi 5)

### Hardware Connections

#### PCA9685 to Raspberry Pi 5

Connect via I2C:

```
PCA9685         Raspberry Pi 5
---------------------------------
VCC      →      5V (Pin 2 or 4)
GND      →      GND (Pin 6)
SDA      →      GPIO 2 (Pin 3)
SCL      →      GPIO 3 (Pin 5)
```

#### Servos to PCA9685

Default configuration:
- **Mouth Servo** → Channel 0
- **Eyes Servo** → Channel 1

Connect servo wires:
- Brown/Black → GND
- Red → VCC (5V)
- Orange/Yellow → Signal (channel pin)

⚠️ **Important**: Power the PCA9685 servos with external 5V supply if using multiple or high-torque servos.

#### Verify I2C Connection

```bash
# Scan for I2C devices (PCA9685 default address: 0x40)
sudo i2cdetect -y 1

# Should show:
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 00:          -- -- -- -- -- -- -- -- -- -- -- -- --
# ...
# 40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
```

#### USB Devices

```bash
# Plug in webcam and microphone, then verify:
lsusb

# Check video devices
ls /dev/video*

# Check audio devices
arecord -l    # List recording devices
aplay -l      # List playback devices
```

---

## 4. Clone Repository

### Option A: Clone from Main Branch

```bash
cd ~
git clone https://github.com/mayankparmar/TalkingMask-Pi5.git
cd TalkingMask-Pi5
```

### Option B: Clone Feature Branch with Latest Updates

```bash
cd ~
git clone https://github.com/mayankparmar/TalkingMask-Pi5.git
cd TalkingMask-Pi5
git fetch origin
git checkout claude/explore-codebase-011CUqCqhRcLYJeRF1NxdnD2
```

---

## 5. Python Environment

### Automated Installation (Recommended)

```bash
cd ~/TalkingMask-Pi5

# Make installer executable
chmod +x install_requirements.sh

# Run installer (creates venv and installs packages)
./install_requirements.sh
```

### Manual Installation (Alternative)

```bash
cd ~/TalkingMask-Pi5

# Install system packages first (including lgpio build dependencies)
sudo apt install -y i2c-tools python3-smbus swig liblgpio-dev

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade build tools
pip install --upgrade pip wheel setuptools

# Install lgpio from source (required for Pi 5)
pip install --no-binary=:all: lgpio

# Install other Python packages
pip install sounddevice soundfile pyaudio numpy pyttsx3 PyYAML openai \
            speechrecognition adafruit-circuitpython-servokit

# Verify lgpio works
python3 -c "import lgpio; print('lgpio OK')"
```

### Required Python Packages

From `requirements.txt`:
- `sounddevice` - Real-time audio I/O
- `soundfile` - WAV file handling
- `pyaudio` - Audio recording and playback
- `numpy` - Numerical operations
- `pyttsx3` - Alternative TTS engine
- `PyYAML` - Configuration parsing
- `openai` - OpenAI GPT API client
- `speechrecognition` - Google Speech API
- `lgpio` - GPIO library for Raspberry Pi 5
- `adafruit-circuitpython-servokit` - PCA9685 servo control
- `TTS` - Coqui neural TTS (optional, requires Python < 3.13)
- `opencv-python` - Computer vision (may need system package instead)

**Note on Python Version:**
- Python 3.13+: Use `espeak` for TTS (Coqui TTS not yet supported)
- Python 3.9-3.11: Can use either `coqui` or `espeak` for TTS
- Python < 3.9: Not tested

---

## 6. Configuration

### Set Environment Variables

#### For OpenAI (default LLM)

```bash
# Add to ~/.bashrc or ~/.profile
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### For Claude

```bash
# Install Anthropic CLI
pip install anthropic

# Set API key
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### For Gemini

```bash
# Install Google AI SDK
pip install google-generativeai

# Set API key
echo 'export GOOGLE_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Edit config.yaml

```bash
cd ~/TalkingMask-Pi5
nano config.yaml
```

Key settings to verify:

```yaml
mouth:
  closed_angle: 90      # Adjust based on your servo
  open_angle: 140       # Adjust based on your servo
  channel: 0            # PCA9685 channel for mouth

eyes:
  channel: 1            # PCA9685 channel for eyes
  min_angle: 45         # Adjust for your servo range
  max_angle: 120        # Adjust for your servo range

mic:
  device_index: 0       # Change if needed (see Testing section)

tts:
  engine: espeak        # Options: 'espeak' or 'coqui'
  voice: female         # Options: 'female' or 'male'

llm:
  engine: openai        # Options: 'openai', 'claude', 'gemini', 'codex'
  model: 4.1            # For OpenAI: GPT-4 version
```

### Customise System Prompt

Edit Bob's personality and behaviour:

```bash
nano prompts/system_prompt.txt
```

---

## 7. Testing

### Test Individual Components

#### Test I2C and PCA9685

```bash
# Verify PCA9685 is detected
sudo i2cdetect -y 1

# Should show 0x40
```

#### Test Servos

```bash
source venv/bin/activate
python3 << EOF
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

# Test mouth servo (channel 0)
print("Testing mouth servo...")
kit.servo[0].angle = 90   # Closed
import time
time.sleep(1)
kit.servo[0].angle = 140  # Open
time.sleep(1)
kit.servo[0].angle = 90   # Closed

# Test eyes servo (channel 1)
print("Testing eyes servo...")
kit.servo[1].angle = 45   # Left
time.sleep(1)
kit.servo[1].angle = 120  # Right
time.sleep(1)
kit.servo[1].angle = 80   # Centre

print("Servo test complete!")
EOF
```

#### Test Microphone

```bash
# List audio input devices
python3 << EOF
import speech_recognition as sr
for idx, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{idx}: {name}")
EOF

# Record and play back test
arecord -d 3 -f cd test.wav
aplay test.wav
```

#### Test Camera

```bash
# Test webcam capture
python3 << EOF
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    print(f"Camera working! Resolution: {frame.shape[1]}x{frame.shape[0]}")
else:
    print("Camera not detected!")
cap.release()
EOF
```

#### Test TTS

```bash
source venv/bin/activate

# Test eSpeak
espeak "Hello, I am Bob the talking mask"

# Test via Python
python3 coqui_test.py  # If file exists
```

#### Test Speech Recognition

```bash
source venv/bin/activate
python3 << EOF
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something...")
    audio = r.listen(source, timeout=5)
try:
    text = r.recognize_google(audio)
    print(f"You said: {text}")
except:
    print("Could not understand audio")
EOF
```

---

## 8. Running TalkingMask

### Start the System

```bash
cd ~/TalkingMask-Pi5
source venv/bin/activate
python3 main.py
```

### What Should Happen

1. All modules initialise
2. Camera starts face tracking
3. System prints: "Starting conversation loop..."
4. System listens for speech via microphone
5. Detected speech is sent to LLM (OpenAI/Claude/Gemini)
6. Response is synthesised to speech
7. Mouth moves in sync with speech
8. Eyes track detected faces

### Stop the System

Press `Ctrl+C` to gracefully shut down all threads.

---

## 9. Troubleshooting

### ModuleNotFoundError: No module named 'lgpio'

**This is common on Raspberry Pi 5.** The Adafruit Blinka library requires lgpio.

**Solution: Build lgpio from source with proper dependencies**

```bash
# Install required system packages
sudo apt install -y swig liblgpio-dev

# Activate virtual environment
cd ~/TalkingMask-Pi5
source venv/bin/activate

# Upgrade build tools
pip install --upgrade pip wheel setuptools

# Install lgpio from source (not prebuilt binary)
pip install --no-binary=:all: lgpio

# Verify
python3 -c "import lgpio; print('Success!')"
```

**Why this works:**
- `swig` - Required to generate Python bindings
- `liblgpio-dev` - Development headers for lgpio library
- `--no-binary=:all:` - Forces pip to build from source instead of using incompatible prebuilt wheels

### ERROR: No matching distribution found for TTS

**This happens on Python 3.13+.** Coqui TTS doesn't support Python 3.13 yet.

**Solution: Use eSpeak instead**

```bash
# In config.yaml, change:
tts:
  engine: espeak  # Change from 'coqui' to 'espeak'
  voice: female

# eSpeak is already installed via system packages
# Just run the system normally
python3 main.py
```

**Alternative: Use Python 3.11**

If you need neural TTS (Coqui):

```bash
# Install Python 3.11 (if available)
sudo apt install python3.11 python3.11-venv

# Recreate venv with Python 3.11
cd ~/TalkingMask-Pi5
rm -rf venv
python3.11 -m venv --system-site-packages venv
source venv/bin/activate

# Install dependencies including TTS
pip install sounddevice soundfile numpy pyttsx3 PyYAML openai \
            speechrecognition adafruit-circuitpython-servokit TTS
```

### PCA9685 Not Detected

```bash
# Check I2C is enabled
ls /dev/i2c*

# Check wiring
sudo i2cdetect -y 1

# If no device at 0x40, check physical connections
```

### Servo Not Moving

- Verify power supply to PCA9685 (5V/2A minimum)
- Check servo channel numbers in config.yaml
- Test with servo test script (see Testing section)
- Verify angle ranges are within servo limits (0-180°)

### Microphone Not Working

```bash
# Find correct device index
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"

# Update config.yaml with correct device_index
```

### Camera Not Working

```bash
# Check camera is detected
ls /dev/video*

# Try different camera index
python3 -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### OpenAI API Errors

```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### TTS Not Working (eSpeak)

```bash
# Test eSpeak directly
espeak "test"

# If not working, reinstall
sudo apt install --reinstall espeak
```

### Audio Output Issues

```bash
# Check ALSA configuration
amixer

# Set default audio device
sudo raspi-config
# Navigate to: System Options -> Audio

# Test audio output
speaker-test -c2 -t wav
```

### Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

### Permission Errors (I2C)

```bash
# Add user to i2c group
sudo usermod -a -G i2c $USER

# Reboot
sudo reboot
```

---

## Running on Startup (Optional)

To run TalkingMask automatically on boot:

```bash
# Create systemd service
sudo nano /etc/systemd/system/talkingmask.service
```

Add:

```ini
[Unit]
Description=TalkingMask Animatronic System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/TalkingMask-Pi5
ExecStart=/home/pi/TalkingMask-Pi5/venv/bin/python3 /home/pi/TalkingMask-Pi5/main.py
Restart=on-failure
RestartSec=10
Environment="OPENAI_API_KEY=your-key-here"

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable talkingmask.service
sudo systemctl start talkingmask.service

# Check status
sudo systemctl status talkingmask.service

# View logs
sudo journalctl -u talkingmask.service -f
```

---

## Additional Resources

- **Raspberry Pi Documentation**: https://www.raspberrypi.com/documentation/
- **PCA9685 Guide**: https://learn.adafruit.com/16-channel-pwm-servo-driver
- **OpenAI API**: https://platform.openai.com/docs
- **Anthropic Claude**: https://docs.anthropic.com
- **Google Gemini**: https://ai.google.dev/docs

---

## Support

For issues or questions:
- Repository: https://github.com/mayankparmar/TalkingMask-Pi5
- Create an issue with hardware specs and error logs

---

**Last Updated**: 2025-01-05
**Raspberry Pi OS Version**: Bookworm (64-bit)
**Python Version**: 3.11+
