from pydantic import BaseModel, Field


class ToolMetadata(BaseModel):
    slug: str
    name: str
    description: str
    category: str
    accepts_files: bool = False
    input_extensions: list[str] = Field(default_factory=list)
    output_extension: str | None = None


class ToolListResponse(BaseModel):
    count: int
    tools: list[ToolMetadata]
