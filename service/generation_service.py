
import logging
import time

from service.ai_clients.ai_client_protocols import (
    TextModelClientProtocol,
    ImageModelClientProtocol,
)


logger = logging.getLogger(__name__)


class TextGenerationService:
    """Сервис генерации текста."""

    def __init__(self, client: TextModelClientProtocol):
        self.client = client

    def generate(self, prompt: str) -> str:
        """Генерирует текст через выбранную модель."""

        start = time.perf_counter()

        logger.info("Начало генерации текста")

        try:
            result = self.client.generate(prompt)
        except Exception:
            logger.exception("Генерация текста завершилась ошибкой")
            raise

        duration = time.perf_counter() - start

        logger.info(
            "Генерация текста завершена за %.2f сек.",
            duration,
        )

        return result


class ImageGenerationService:
    """Сервис генерации изображений."""

    def __init__(self, client: ImageModelClientProtocol):
        self.client = client

    def generate(
        self,
        prompt: str,
        resolution: tuple[int, int],
    ) -> str:
        """Генерирует изображение через выбранную модель."""

        start = time.perf_counter()

        logger.info(
            "Начало генерации изображения: %sx%s",
            resolution[0],
            resolution[1],
        )

        try:
            result = self.client.generate(prompt, resolution)
        except Exception:
            logger.exception("Генерация изображения завершилась ошибкой")
            raise

        duration = time.perf_counter() - start

        logger.info(
            "Генерация изображения завершена за %.2f сек.",
            duration,
        )

        return result
