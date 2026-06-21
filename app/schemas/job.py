from typing import Any

from pydantic import BaseModel


class JobRunResponse(BaseModel):
    tool: str
    result: dict[str, Any]
