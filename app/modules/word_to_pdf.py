import shutil
import subprocess
import os
from pathlib import Path
from typing import Any
from uuid import uuid4

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
        libreoffice = shutil.which("libreoffice") or shutil.which("soffice")
        if libreoffice is None:
            raise RuntimeError("LibreOffice is not installed in this environment.")

        output_dir.mkdir(parents=True, exist_ok=True)
        profile_dir = output_dir / f"lo-profile-{uuid4().hex}"
        profile_dir.mkdir(parents=True, exist_ok=True)
        before = {path.resolve() for path in output_dir.glob("*.pdf")}
        env = os.environ.copy()
        env["HOME"] = str(profile_dir.resolve())

        result = subprocess.run(
            [
                libreoffice,
                "--headless",
                "--nologo",
                "--nofirststartwizard",
                f"-env:UserInstallation=file://{profile_dir.resolve().as_posix()}",
                "--convert-to",
                "pdf:writer_pdf_Export",
                "--outdir",
                str(output_dir),
                str(input_path),
            ],
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
        shutil.rmtree(profile_dir, ignore_errors=True)

        output_path = output_dir / f"{input_path.stem}.pdf"
        if output_path.exists():
            return output_path

        generated = [
            path for path in output_dir.glob("*.pdf")
            if path.resolve() not in before
        ]
        if generated:
            return max(generated, key=lambda path: path.stat().st_mtime)

        files = ", ".join(path.name for path in output_dir.iterdir())
        detail = " ".join(
            part.strip()
            for part in (result.stdout, result.stderr)
            if part and part.strip()
        )
        if result.returncode != 0:
            raise RuntimeError(f"LibreOffice failed with exit code {result.returncode}. {detail}")
        raise RuntimeError(
            "Word to PDF conversion did not produce an output file."
            f" LibreOffice output: {detail or 'empty'}."
            f" Output directory files: {files or 'none'}."
        )

    def run(self, **kwargs: Any) -> dict[str, Any]:
        return {
            "status": "requires_file",
            "tool": self.slug,
            "message": "Upload a .doc or .docx file to convert it to PDF.",
        }
