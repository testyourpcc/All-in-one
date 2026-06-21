from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "File Tool Local" in response.text
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
    assert data["count"] == 5
    assert {tool["slug"] for tool in data["tools"]} == {
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


def test_run_placeholder_job() -> None:
    response = client.post("/api/v1/jobs/pdf-merge")

    assert response.status_code == 200
    assert response.json()["result"]["status"] == "not_implemented"
