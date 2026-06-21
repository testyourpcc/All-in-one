from pathlib import Path

from docx import Document

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
