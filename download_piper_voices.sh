#!/bin/bash

# Piper TTS Voice Downloader for TalkingMask-Pi5
# Downloads recommended voice models from Hugging Face
#
# NOTE: This script is now integrated into install_requirements.sh
# You only need to run this if you want to download additional voices
# or re-download voices that were deleted.

VOICE_DIR="models/piper"
mkdir -p "$VOICE_DIR"

echo "========================================"
echo "Piper TTS Voice Downloader"
echo "========================================"
echo ""
echo "Downloading recommended voices to: $VOICE_DIR"
echo ""

cd "$VOICE_DIR"

# Alba - Scottish female (medium) - RECOMMENDED
echo "1. Downloading en_GB-alba-medium (Scottish female, 31MB)..."
wget -q --show-progress https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx
wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json

# Create symlinks (some versions of piper look for .json instead of .onnx.json)
ln -sf en_GB-alba-medium.onnx.json en_GB-alba-medium.json

echo ""

# Alan - British male (medium)
echo "2. Downloading en_GB-alan-medium (British male, 63MB)..."
wget -q --show-progress https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/medium/en_GB-alan-medium.onnx
wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/medium/en_GB-alan-medium.onnx.json
ln -sf en_GB-alan-medium.onnx.json en_GB-alan-medium.json

echo ""

# Lessac - American female (medium)
echo "3. Downloading en_US-lessac-medium (American female, 63MB)..."
wget -q --show-progress https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
ln -sf en_US-lessac-medium.onnx.json en_US-lessac-medium.json

echo ""
echo "========================================"
echo "✓ Downloaded 3 voices successfully!"
echo "========================================"
echo ""
echo "Voices installed in: $(pwd)"
echo ""
echo "Default voice (configured in config.yaml):"
echo "  en_GB-alba-medium - Scottish female"
echo ""
echo "To change voice, edit config.yaml:"
echo "  tts:"
echo "    engine: piper"
echo "    voice: en_GB-alba-medium    # Change this"
echo ""
echo "Test voice with:"
echo "  cd ~/TalkingMask-Pi5"
echo "  source venv/bin/activate"
echo "  python3 main.py"
echo ""
