
import logging

from openai import OpenAI, RateLimitError

from service.exceptions import ImageModelError


class ProvodImageClient:
    """Клиент генерации изображений через Provod AI."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
    ):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=300.0,
            max_retries=0,
        )
        self.model = model
        self.logger = logging.getLogger(__name__)

    def generate(
        self,
        prompt: str,
        resolution: tuple[int, int],
    ) -> str:
        width, height = resolution

        if width == height:
            size = "1024x1024"
        elif width < height:
            size = "1024x1536"
        else:
            size = "1536x1024"

        try:
            response = self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                response_format="b64_json",
            )

            image_base64 = response.data[0].b64_json

            if not image_base64:
                raise ImageModelError(
                    "Provod AI вернул пустое изображение"
                )

            return image_base64

        
        except RateLimitError as exc:
            self.logger.error(
                "Provod AI rate limit: status=%s, response=%s",
                exc.status_code,
                exc.response.text[:1000],
            )
            raise ImageModelError(
                "Provod AI: превышен лимит запросов или квота"
            ) from exc

        except Exception as exc:
            self.logger.exception(
                "Ошибка генерации изображения через Provod AI"
            )
            raise ImageModelError(
                "Ошибка генерации изображения через Provod AI"
            ) from exc


    def close(self) -> None:
        self.client.close()
