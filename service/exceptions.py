class TextModelError(Exception):
    """Ошибка при генерации текста."""


class ImageModelError(Exception):
    """Ошибка при генерации изображения."""


class AudioTranscriptionError(Exception):
    """Ошибка при распознавании аудио."""