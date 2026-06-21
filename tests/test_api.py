from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "File Tool Local" in response.text
    assert "Word tools" in response.text
    assert "Excel tools" in response.text
    assert "word-to-pdf" in response.text
    assert "pdf-to-word" in response.text
    assert "pdf-merge" in response.text


def test_health_check() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "file-tool-local",
    }


def test_list_tools() -> None:
    response = client.get("/api/v1/tools")

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 7
    assert {tool["slug"] for tool in data["tools"]} == {
        "word-to-pdf",
        "pdf-to-word",
        "pdf-merge",
        "pdf-split",
        "pdf-compress",
        "excel-batch-edit",
        "word-batch-edit",
    }


def test_get_tool() -> None:
    response = client.get("/api/v1/tools/pdf-merge")

    assert response.status_code == 200
    assert response.json()["slug"] == "pdf-merge"


def test_get_file_conversion_tool_metadata() -> None:
    response = client.get("/api/v1/tools/word-to-pdf")

    assert response.status_code == 200
    data = response.json()
    assert data["accepts_files"] is True
    assert data["input_extensions"] == [".doc", ".docx"]
    assert data["output_extension"] == ".pdf"


def test_conversion_tool_rejects_wrong_extension() -> None:
    response = client.post(
        "/api/v1/tools/word-to-pdf/run",
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 400


def test_run_placeholder_job() -> None:
    response = client.post("/api/v1/jobs/pdf-merge")

    assert response.status_code == 200
    assert response.json()["result"]["status"] == "not_implemented"
