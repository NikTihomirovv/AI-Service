
import os
from collections.abc import Iterator
from functools import lru_cache

from fastapi import Depends

from config.loader import load_config
from service.ai_clients.ollama_client import OllamaClient
from service.ai_clients.pollinations_client import PollinationsClient
from service.ai_clients.provod_image_client import ProvodImageClient
from service.ai_clients.whisper_client import WhisperClient
from service.generation_service import (ImageGenerationService,
                                        TextGenerationService)
from service.transcription_service import TranscriptionService
from service.ai_clients.provod_text_client import ProvodTextClient

@lru_cache(maxsize=1)
def get_whisper_client() -> WhisperClient:
    """Возвращает единственный экземпляр WhisperClient."""

    config = load_config()
    return WhisperClient(config.whisper)



def get_text_generation_service() -> Iterator[TextGenerationService]:
    """Выбирает провайдера генерации текста."""

    config = load_config()

    if config.text_provider == "provod":
        client = ProvodTextClient(
            api_key=os.environ["PROVOD_API_KEY"],
            base_url=config.provod.base_url,
            model=config.provod.text_model,
        )

    elif config.text_provider == "ollama":
        client = OllamaClient(config.ollama)

    else:
        raise ValueError(
            f"Неизвестный текстовый провайдер: "
            f"{config.text_provider}"
        )

    try:
        yield TextGenerationService(client)
    finally:
        client.close()



def get_image_generation_service() -> Iterator[ImageGenerationService]:
    """Выбирает провайдера генерации изображений."""

    config = load_config()

    if config.image_provider == "provod":
        client = ProvodImageClient(
            api_key=os.environ["PROVOD_API_KEY"],
            base_url=config.provod.base_url,
            model=config.provod.model,
        )

    elif config.image_provider == "pollinations":
        client = PollinationsClient(config.pollinations)

    else:
        raise ValueError(
            f"Неизвестный провайдер: {config.image_provider}"
        )

    try:
        yield ImageGenerationService(client)
    finally:
        client.close()



def get_transcription_service() -> TranscriptionService:
    """Создаёт сервис распознавания с общей моделью Whisper."""

    client = get_whisper_client()

    return TranscriptionService(client)
