import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

AVATAR_MAX_SIZE = 2 * 1024 * 1024  # 2 Mb
RESUME_MAX_SIZE = 5 * 1024 * 1024  # 5 Mb
ALLOWED_AVATAR_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_RESUME_TYPES = {"application/pdf"}

AVATAR_DIR = Path("uploads") / "avatars"
RESUME_DIR = Path("uploads") / "resumes"


async def save_upload(
    file: UploadFile,
    directory: Path,
    allowed_types: set[str],
    max_size: int,
) -> str:
    """Validate and save an uploaded file.

    Returns the unique filename.
    """
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {file.content_type}",
        )
    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE, detail="File too large"
        )
    ext = Path(file.filename or "").suffix.lower()
    unique_name = f"{uuid.uuid4()}{ext}"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / unique_name).write_bytes(contents)
    return unique_name


def delete_file(directory: Path, filename: str) -> None:
    """Delete a file if it exists."""
    path = directory / filename
    if path.exists():
        path.unlink()
