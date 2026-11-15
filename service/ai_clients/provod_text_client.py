
import logging

from openai import OpenAI, OpenAIError

from service.exceptions import TextModelError


class ProvodTextClient:
    """Клиент генерации текста через Provod AI."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
    ) -> None:
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=300.0,
            max_retries=0,
        )
        self.model = model
        self.logger = logging.getLogger(__name__)

    def generate(self, prompt: str) -> str:
        """Генерирует текст через Provod AI."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.7,
            )

            result = response.choices[0].message.content

            if not result or not result.strip():
                raise TextModelError(
                    "Provod AI вернул пустой текст"
                )

            return result

        except OpenAIError as exc:
            self.logger.exception(
                "Ошибка генерации текста через Provod AI"
            )
            raise TextModelError(
                "Ошибка генерации текста через Provod AI"
            ) from exc

    def close(self) -> None:
        """Закрывает HTTP-клиент."""
        self.client.close()
