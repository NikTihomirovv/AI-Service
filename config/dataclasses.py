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
class AppConfig:
    """Общая конфигурация AI-Service."""

    ollama: OllamaConfig
    pollinations: PollinationsConfig