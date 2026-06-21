from fastapi import APIRouter, HTTPException

from app.schemas.tool import ToolListResponse, ToolMetadata
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
