from dataclasses import dataclass


@dataclass(frozen=True)
class OllamaConfig:
    """Настройки клиента Ollama."""

    name: str
    base_url: str
    stream: bool
    temperature: float
    top_p: float
    max_tokens: int
    connect_timeout: int
    read_timeout: int


@dataclass(frozen=True)
class PollinationsConfig:
    """Настройки клиента Pollinations."""

    name: str
    base_url: str
    timeout: int


@dataclass(frozen=True)
class WhisperConfig:
    """Настройки модели распознавания аудио."""

    name: str
    device: str
    compute_type: str
    language: str | None
    beam_size: int


@dataclass(frozen=True)
class AppConfig:
    """Общая конфигурация AI-Service."""

    ollama: OllamaConfig
    pollinations: PollinationsConfig
    whisper: WhisperConfig


