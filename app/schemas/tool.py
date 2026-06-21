from pydantic import BaseModel


class ToolMetadata(BaseModel):
    slug: str
    name: str
    description: str
    category: str


class ToolListResponse(BaseModel):
    count: int
    tools: list[ToolMetadata]
