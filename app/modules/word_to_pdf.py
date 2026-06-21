import shutil
import subprocess
from pathlib import Path
from typing import Any

from app.modules.base import ToolModule


class WordToPdfModule(ToolModule):
    slug = "word-to-pdf"
    name = "Word to PDF"
    description = "Convert .doc or .docx documents into PDF files."
    category = "word"
    accepts_files = True
    input_extensions = (".doc", ".docx")
    output_extension = ".pdf"
    output_media_type = "application/pdf"

    def run_file(self, input_path: Path, output_dir: Path) -> Path:
        self.validate_input_file(input_path)
        if shutil.which("libreoffice") is None:
            raise RuntimeError("LibreOffice is not installed in this environment.")

        output_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(output_dir),
                str(input_path),
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )

        output_path = output_dir / f"{input_path.stem}.pdf"
        if not output_path.exists():
            raise RuntimeError("Word to PDF conversion did not produce an output file.")
        return output_path

    def run(self, **kwargs: Any) -> dict[str, Any]:
        return {
            "status": "requires_file",
            "tool": self.slug,
            "message": "Upload a .doc or .docx file to convert it to PDF.",
        }
