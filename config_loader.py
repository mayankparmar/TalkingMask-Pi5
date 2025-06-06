import yaml

def load_config(path="config.yaml"):
    with open(path, 'r') as file:
        config = yaml.safe_load(file)

    # Basic validation (can be expanded)
    assert "mouth" in config
    assert "envelope" in config
    assert "tts" in config
    assert "llm" in config

    return config
