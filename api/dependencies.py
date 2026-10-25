
from collections.abc import Iterator

from fastapi import Depends

from config.loader import load_config
from service.ai_clients.ollama_client import OllamaClient
from service.ai_clients.pollinations_client import PollinationsClient
from service.generation_service import (
    TextGenerationService,
    ImageGenerationService,
)
from service.ai_clients.whisper_client import WhisperClient
from service.transcription_service import TranscriptionService
from functools import lru_cache


@lru_cache(maxsize=1)
def get_whisper_client() -> WhisperClient:
    """Возвращает единственный экземпляр WhisperClient."""

    config = load_config()
    return WhisperClient(config.whisper)


def get_text_generation_service() -> Iterator[TextGenerationService]:
    """Создаёт сервис генерации текста."""

    config = load_config()
    client = OllamaClient(config.ollama)

    try:
        yield TextGenerationService(client)
    finally:
        client.close()


def get_image_generation_service() -> Iterator[ImageGenerationService]:
    """Создаёт сервис генерации изображений."""

    config = load_config()
    client = PollinationsClient(config.pollinations)

    try:
        yield ImageGenerationService(client)
    finally:
        client.close()


def get_transcription_service() -> TranscriptionService:
    """Создаёт сервис распознавания с общей моделью Whisper."""

    client = get_whisper_client()

    return TranscriptionService(client)
