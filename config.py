
"""
Jarvis AI Assistant - Configuration
Central place for assistant settings and file paths.
"""

import json
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent

# Data files
SETTINGS_FILE = BASE_DIR / "jarvis_settings.json"
MEMORY_FILE = BASE_DIR / "jarvis_memory.json"
HISTORY_FILE = BASE_DIR / "chat_history.json"

# Default assistant configuration
DEFAULT_CONFIG = {
    "assistant_name": "Jarvis",
    "ai_model": "llama3.2",
    "ollama_url": "http://localhost:11434/api/generate",
    "voice_speed": 1.0,
    "theme": "Dark"
}


def load_config():
    """Load settings from JSON or use defaults."""
    config = DEFAULT_CONFIG.copy()

    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                saved_settings = json.load(file)

            if isinstance(saved_settings, dict):
                config.update(saved_settings)

        except (OSError, json.JSONDecodeError) as error:
            print(f"Could not load settings: {error}")

    return config


def save_config(config):
    """Save settings to the JSON configuration file."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4, ensure_ascii=False)
        return True

    except (OSError, TypeError) as error:
        print(f"Could not save settings: {error}")
        return False


# Load configuration when this module is imported
CONFIG = load_config()

ASSISTANT_NAME = CONFIG["assistant_name"]
AI_MODEL = CONFIG["ai_model"]
OLLAMA_URL = CONFIG["ollama_url"]
VOICE_SPEED = CONFIG["voice_speed"]
THEME = CONFIG["theme"]


if __name__ == "__main__":
    print("Jarvis Configuration")
    print("--------------------")
    print(f"Assistant: {ASSISTANT_NAME}")
    print(f"AI Model: {AI_MODEL}")
    print(f"Ollama URL: {OLLAMA_URL}")
    print(f"Voice Speed: {VOICE_SPEED}")
    print(f"Theme: {THEME}")

    if save_config(CONFIG):
        print("\nConfiguration saved successfully!")
