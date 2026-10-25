
import os
from pathlib import Path

import yaml

from config.dataclasses import (
    AppConfig,
    OllamaConfig,
    PollinationsConfig,
    WhisperConfig,
)


CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


def load_config() -> AppConfig:
    """Загружает конфигурацию приложения."""

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    ollama_data = data["ollama"].copy()

    ollama_data["base_url"] = os.getenv(
        "OLLAMA_BASE_URL",
        ollama_data["base_url"],
    )

    return AppConfig(
        ollama=OllamaConfig(**ollama_data),
        pollinations=PollinationsConfig(**data["pollinations"]),
        whisper=WhisperConfig(**data["whisper"]),
    )
