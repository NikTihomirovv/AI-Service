import shutil
import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Form

from api.dependencies import get_transcription_service
from api.schemas.transcription import TranscriptionResponse
from service.transcription_service import TranscriptionService


router = APIRouter()


@router.post(
    "/audio/transcribe",
    response_model=TranscriptionResponse,
)
def transcribe_audio(
    file: Annotated[UploadFile, File()],
    service: Annotated[
        TranscriptionService,
        Depends(get_transcription_service),
    ],
    lyrics: Annotated[str | None, Form()] = None,
) -> TranscriptionResponse:
    """Принимает аудиофайл и необязательный текст песни."""

    suffix = Path(file.filename or "").suffix

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            audio_path = Path(temp_dir) / f"audio{suffix}"

            with audio_path.open("wb") as output:
                shutil.copyfileobj(file.file, output)

            words = service.transcribe(
                audio_path=audio_path,
                lyrics=lyrics,
            )
    finally:
        file.file.close()

    return TranscriptionResponse(words=words)