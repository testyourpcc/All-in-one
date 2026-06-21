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

## CI/CD GitHub Actions + Azure

Workflow nằm ở `.github/workflows/ci-cd.yml`.

Luồng chạy:

1. Pull request hoặc push: cài dependency và chạy `pytest`.
2. Push vào `main`: build Docker image và push lên GitHub Container Registry.
3. Push vào `main`: deploy image lên Azure Web App for Containers nếu đã cấu hình secrets.

Repository secrets cần tạo trong GitHub:

- `AZURE_WEBAPP_NAME`: tên Azure Web App.
- `AZURE_WEBAPP_PUBLISH_PROFILE`: nội dung file publish profile tải từ Azure Portal.

Nếu chưa có secrets, workflow vẫn chạy test/build image; bước Azure deploy sẽ được skip bằng notice.

Azure Web App nên được tạo ở chế độ Linux container, port app là `8000`.
Trong Azure App Service, thêm app setting `WEBSITES_PORT=8000` nếu container không tự nhận đúng port.

## Tool đã có

- Word to PDF: upload `.doc` hoặc `.docx`, trả về `.pdf`.
- PDF to Word: upload `.pdf`, trả về `.docx`.
- PDF merge/split/compress: đã có module placeholder để triển khai tiếp.
- Word/Excel batch edit: đã có module placeholder để triển khai tiếp.

`Word to PDF` chạy bằng LibreOffice headless trong Docker image. `PDF to Word` dùng thư viện `pdf2docx`, phù hợp cho tài liệu phổ thông nhưng chất lượng layout vẫn phụ thuộc cấu trúc file PDF đầu vào.

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
