# File Tool Local

Backend local cho web gom nhiều tool xử lý file. Mỗi tool là một module riêng kế thừa `ToolModule`, được đăng ký qua `ModuleRegistry` để sau này thêm tool mới mà không phải sửa nhiều nơi.

## Stack

- FastAPI
- Module-based/OOP tool architecture
- Local storage: `storage/uploads`, `storage/outputs`, `storage/temp`
- Docker Compose để chạy local

## Chạy local bằng Docker

```powershell
docker compose up --build
```

Sau đó mở:

- Trang local: http://localhost:8000
- API docs: http://localhost:8000/docs
- Danh sách tool: http://localhost:8000/api/v1/tools
- Health check: http://localhost:8000/api/v1/health

## Chạy local bằng Python

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Thêm tool mới

1. Tạo file module mới trong `app/modules`.
2. Tạo class kế thừa `ToolModule`.
3. Khai báo `slug`, `name`, `description`, `category`.
4. Implement method `run`.
5. Đăng ký class trong `create_default_registry` ở `app/services/module_registry.py`.

Ví dụ endpoint sau khi đăng ký:

```text
GET  /api/v1/tools/{slug}
POST /api/v1/jobs/{slug}
```

## Cấu trúc

```text
app/
  api/v1/        API routes
  core/          Config và app bootstrap helpers
  jobs/          Queue/worker hooks cho giai đoạn sau
  modules/       Các tool xử lý file
  schemas/       Pydantic response/request models
  services/      Registry, storage, file services
  utils/         Helper functions
storage/         File runtime local
tests/           Unit/API tests
docker/          Docker config mở rộng
scripts/         Maintenance scripts
```
