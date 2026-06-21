from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


def safe_upload_name(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    return f"{uuid4().hex}{suffix}"


async def save_upload(upload: UploadFile, upload_dir: Path) -> Path:
    upload_dir.mkdir(parents=True, exist_ok=True)
    output_path = upload_dir / safe_upload_name(upload.filename or "upload")
    content = await upload.read()
    if not content:
        raise ValueError("Uploaded file is empty.")
    output_path.write_bytes(content)
    return output_path
