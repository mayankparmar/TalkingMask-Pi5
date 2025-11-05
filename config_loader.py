"""Configuration loader for TalkingMask system."""

import yaml


def load_config(path="config.yaml"):
    """
    Load and validate YAML configuration file.

    Args:
        path: Path to config.yaml file

    Returns:
        Dictionary containing configuration settings
    """
    with open(path, 'r') as file:
        config = yaml.safe_load(file)

    # Validate required sections
    required = ["mouth", "eyes", "mic", "envelope", "tts", "llm"]
    for section in required:
        assert section in config, f"Missing required config section: {section}"

    return config
