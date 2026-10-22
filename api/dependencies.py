
from collections.abc import Iterator

from fastapi import Depends

from config.loader import load_config
from service.ai_clients.ollama_client import OllamaClient
from service.ai_clients.pollinations_client import PollinationsClient
from service.generation_service import (
    TextGenerationService,
    ImageGenerationService,
)


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
