
import logging

import requests

from config.dataclasses import OllamaConfig
from service.exceptions import TextModelError


class OllamaClient:
    """Клиент для взаимодействия с локальными моделями Ollama."""

    def __init__(self, config: OllamaConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()


    def close(self) -> None:
        """Закрывает HTTP-сессию."""
        self.session.close()


    def check_model(self) -> bool:
        """Проверяет наличие выбранной модели в Ollama."""

        url = f"{self.config.base_url.rstrip('/')}/api/tags"

        try:
            response = self.session.get(
                url,
                timeout=self.config.connect_timeout,
            )
            response.raise_for_status()

            models = response.json().get("models", [])

            return any(
                model.get("name") == self.config.name
                for model in models
            )

        except (requests.RequestException, ValueError, TypeError, AttributeError) as exc:
            self.logger.exception(
                "Ошибка проверки модели Ollama: %s",
                self.config.name,
            )
            raise TextModelError(
                "Ошибка при проверке доступности модели Ollama"
            ) from exc


    def generate(self, prompt: str) -> str:
        """Генерирует текст с помощью Ollama."""

        url = f"{self.config.base_url.rstrip('/')}/api/generate"

        payload = {
            "model": self.config.name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
                "num_predict": self.config.max_tokens,
            },
        }

        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=(
                    self.config.connect_timeout,
                    self.config.read_timeout,
                ),
            )
            response.raise_for_status()

            data = response.json()
            answer = data.get("response")

            if not isinstance(answer, str):
                raise TextModelError(
                    "Ollama вернула некорректный ответ"
                )

            return answer

        except (requests.RequestException, ValueError, TypeError, AttributeError) as exc:
            self.logger.exception(
                "Ошибка генерации текста через Ollama"
            )
            raise TextModelError(
                "Ошибка при генерации текста через Ollama"
            ) from exc
