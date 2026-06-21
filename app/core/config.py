from pathlib import Path


class Settings:
    app_name = "File Tool Local"
    api_prefix = "/api/v1"
    storage_dir = Path("storage")
    upload_dir = storage_dir / "uploads"
    output_dir = storage_dir / "outputs"
    temp_dir = storage_dir / "temp"


settings = Settings()


def ensure_storage_dirs() -> None:
    for path in (settings.upload_dir, settings.output_dir, settings.temp_dir):
        path.mkdir(parents=True, exist_ok=True)
