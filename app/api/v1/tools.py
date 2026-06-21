from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.core.config import settings
from app.schemas.tool import ToolListResponse, ToolMetadata
from app.services.file_service import save_upload
from app.services.module_registry import module_registry


router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("", response_model=ToolListResponse)
def list_tools() -> ToolListResponse:
    tools = module_registry.list()
    return ToolListResponse(count=len(tools), tools=tools)


@router.get("/{slug}", response_model=ToolMetadata)
def get_tool(slug: str) -> ToolMetadata:
    module = module_registry.get(slug)
    if module is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return module.metadata()


@router.post("/{slug}/run")
async def run_tool_with_file(slug: str, file: UploadFile = File(...)) -> FileResponse:
    module = module_registry.get(slug)
    if module is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    if not module.accepts_files:
        raise HTTPException(status_code=400, detail="This tool does not accept file uploads yet.")

    try:
        module.validate_input_file(Path(file.filename or "upload"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        input_path = await save_upload(file, settings.upload_dir)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    job_output_dir = settings.output_dir / Path(input_path).stem

    try:
        output_path = module.run_file(input_path, job_output_dir)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    download_name = f"{Path(file.filename or input_path.stem).stem}{module.output_extension or output_path.suffix}"
    return FileResponse(
        path=output_path,
        filename=download_name,
        media_type=module.output_media_type,
    )
