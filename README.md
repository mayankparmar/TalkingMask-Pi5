# TalkingMask-Pi5

An AI-powered animatronic mask named "Bob" featuring voice interaction, face tracking, and servo-controlled movement.

## Features

- 🎤 **Voice Interaction** - Speech recognition via Google Speech API
- 🤖 **AI Conversation** - GPT-4, Claude, Gemini, or Codex powered responses
- 👄 **Mouth Synchronisation** - Real-time audio envelope detection
- 👀 **Face Tracking** - Webcam-based eye movement
- 🔧 **Hardware Control** - PCA9685 PWM servo driver
- 🔊 **Text-to-Speech** - Coqui TTS or eSpeak synthesis

## Hardware Requirements

- Raspberry Pi 5
- PCA9685 16-Channel PWM Servo Driver
- 2× Servo Motors (mouth and eyes)
- USB Webcam
- USB Microphone
- Speaker/Audio Output

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/mayankparmar/TalkingMask-Pi5.git
cd TalkingMask-Pi5
```

### 2. Install Dependencies

```bash
chmod +x install_requirements.sh
./install_requirements.sh
```

### 3. Configure

Edit `config.yaml` to set your LLM provider and servo settings.

Set your API key:
```bash
export OPENAI_API_KEY="your-key-here"
```

### 4. Run

```bash
source venv/bin/activate
python3 main.py
```

## Complete Setup Guide

**For detailed setup instructions on a fresh Raspberry Pi 5, see [SETUP.md](SETUP.md)**

The complete guide includes:
- System dependencies installation
- Hardware wiring diagrams
- I2C configuration
- Component testing procedures
- Troubleshooting tips
- Autostart configuration

## Configuration

Choose your LLM provider in `config.yaml`:

```yaml
llm:
  engine: openai  # Options: openai, claude, gemini, codex, local
  model: 4.1
  prompt_file: prompts/system_prompt.txt
```

Supported engines:
- **openai** - OpenAI GPT (requires `OPENAI_API_KEY`)
- **claude** - Anthropic Claude (requires Anthropic CLI)
- **gemini** - Google Gemini (requires Google AI CLI)
- **codex** - OpenAI Codex (requires OpenAI CLI)
- **local** - Local LLM (not yet implemented)

## Project Structure

```
TalkingMask-Pi5/
├── main.py                 # Main entry point
├── config.yaml             # Configuration file
├── requirements.txt        # Python dependencies
├── install_requirements.sh # Automated installer
│
├── config_loader.py        # YAML configuration loader
├── gpt_assistant.py        # LLM interface (multi-provider)
├── voice_assistant.py      # Speech recognition
├── tts_manager.py          # Text-to-speech with sync
├── mouth_controller.py     # Mouth servo control
├── eyes_controller.py      # Eye servo control
├── envelope_monitor.py     # Audio envelope detection
├── cam.py                  # Face detection and tracking
│
└── prompts/
    └── system_prompt.txt   # Bob's personality definition
```

## Credits

**Pi 5 Redesign**: Mayank Parmar
**Pi 3 Software**: Shane Ormonde
**Mechanical Design**: Martin Lynch, Keith Colton
**Architecture**: Dave Powell, Mayank Parmar
**Project Lead**: Paula Kelly
**Ideation**: Damon Berry, Fatema Badmos
**Outreach**: Peterson Jean

## Licence

[Add your licence here]

## Support

For issues or questions, please open an issue on GitHub.

