from pathlib import Path
from typing import Any

from pdf2docx import Converter

from app.modules.base import ToolModule


class PdfToWordModule(ToolModule):
    slug = "pdf-to-word"
    name = "PDF to Word"
    description = "Convert PDF files into editable .docx documents."
    category = "word"
    accepts_files = True
    input_extensions = (".pdf",)
    output_extension = ".docx"
    output_media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    def run_file(self, input_path: Path, output_dir: Path) -> Path:
        self.validate_input_file(input_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{input_path.stem}.docx"

        converter = Converter(str(input_path))
        try:
            converter.convert(str(output_path), start=0, end=None)
        finally:
            converter.close()

        if not output_path.exists():
            raise RuntimeError("PDF to Word conversion did not produce an output file.")
        return output_path

    def run(self, **kwargs: Any) -> dict[str, Any]:
        return {
            "status": "requires_file",
            "tool": self.slug,
            "message": "Upload a .pdf file to convert it to Word.",
        }
