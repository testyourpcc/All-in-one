from fastapi import APIRouter, HTTPException

from app.schemas.job import JobRunResponse
from app.services.module_registry import module_registry


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/{tool_slug}", response_model=JobRunResponse)
def create_job(tool_slug: str) -> JobRunResponse:
    module = module_registry.get(tool_slug)
    if module is None:
        raise HTTPException(status_code=404, detail="Tool not found")

    result = module.run()
    return JobRunResponse(tool=tool_slug, result=result)
