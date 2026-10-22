
import base64
import logging
from urllib.parse import quote

import requests

from config.dataclasses import PollinationsConfig
from service.exceptions import ImageModelError


class PollinationsClient:
    """Клиент для генерации изображений через Pollinations."""

    def __init__(self, config: PollinationsConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()


    def close(self) -> None:
        """Закрывает HTTP-сессию."""
        self.session.close()


    def check_model(self) -> bool:
        """Проверяет доступность сервиса Pollinations."""

        url = self.config.base_url.rstrip("/")

        try:
            response = self.session.head(
                url,
                timeout=self.config.timeout,
            )
            response.raise_for_status()

            return True

        except requests.RequestException as exc:
            self.logger.exception(
                "Ошибка проверки доступности Pollinations"
            )
            raise ImageModelError(
                "Ошибка подключения к Pollinations"
            ) from exc


    def generate(
        self,
        prompt: str,
        resolution: tuple[int, int],
    ) -> str:
        """Генерирует изображение и возвращает Base64."""

        width, height = resolution

        url = (
            f"{self.config.base_url.rstrip('/')}"
            f"/prompt/{quote(prompt, safe='')}"
        )
        params = {
            "width": width,
            "height": height,
            "nologo": "true",
        }

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.config.timeout,
            )
            response.raise_for_status()

            content_type = response.headers.get(
                "Content-Type", ""
            ).lower()

            if not content_type.startswith("image/"):
                raise ImageModelError(
                    "Pollinations вернул данные, не являющиеся изображением"
                )

            if not response.content:
                raise ImageModelError(
                    "Pollinations вернул пустое изображение"
                )

            return base64.b64encode(
                response.content
            ).decode("utf-8")

        except requests.RequestException as exc:
            self.logger.exception(
                "Ошибка генерации изображения через Pollinations"
            )
            raise ImageModelError(
                "Ошибка при генерации изображения через Pollinations"
            ) from exc
