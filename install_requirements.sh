#!/bin/bash

echo "Updating package index..."
sudo apt update

echo "Installing system dependencies..."
sudo apt install -y python3-dev build-essential libasound2-dev portaudio19-dev \
    python3-pyaudio espeak espeak-ng espeak-ng-data libatlas-base-dev libffi-dev \
    libsndfile1 libportaudio2 ffmpeg sox

echo "Creating virtual environment (venv)..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "All done"
