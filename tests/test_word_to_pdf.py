from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from docx import Document
import pytest

from app.modules.word_to_pdf import WordToPdfModule


def test_word_to_pdf_creates_pdf(tmp_path: Path) -> None:
    input_path = tmp_path / "sample.docx"
    output_dir = tmp_path / "output"

    document = Document()
    document.add_paragraph("Word to PDF conversion check")
    document.save(input_path)

    output_path = WordToPdfModule().run_file(input_path, output_dir)

    assert output_path.suffix == ".pdf"
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_word_to_pdf_reports_unreadable_source(tmp_path: Path) -> None:
    input_path = tmp_path / "broken.docx"
    input_path.write_bytes(b"not a word file")

    fake_result = SimpleNamespace(
        returncode=0,
        stdout="",
        stderr="Error: source file could not be loaded",
    )

    with patch("app.modules.word_to_pdf.shutil.which", return_value="/usr/bin/libreoffice"):
        with patch("app.modules.word_to_pdf.subprocess.run", return_value=fake_result):
            with pytest.raises(ValueError, match="could not open this file"):
                WordToPdfModule().run_file(input_path, tmp_path / "output")
