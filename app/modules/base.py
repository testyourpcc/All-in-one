from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from app.schemas.tool import ToolMetadata


class ToolModule(ABC):
    """Base class for every installable tool module."""

    slug: str
    name: str
    description: str
    category: str = "general"
    scope: str = "common"
    accepts_files: bool = False
    input_extensions: tuple[str, ...] = ()
    output_extension: str | None = None
    output_media_type: str = "application/octet-stream"

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            slug=self.slug,
            name=self.name,
            description=self.description,
            category=self.category,
            scope=self.scope,
            accepts_files=self.accepts_files,
            input_extensions=list(self.input_extensions),
            output_extension=self.output_extension,
        )

    def validate_input_file(self, input_path: Path) -> None:
        if not self.input_extensions:
            return
        suffix = input_path.suffix.lower()
        if suffix not in self.input_extensions:
            accepted = ", ".join(self.input_extensions)
            raise ValueError(f"{self.name} accepts only: {accepted}")

    def run_file(self, input_path: Path, output_dir: Path) -> Path:
        raise NotImplementedError(f"{self.slug} does not support file input yet.")

    @abstractmethod
    def run(self, **kwargs: Any) -> dict[str, Any]:
        """Execute the tool.

        Concrete modules will replace this placeholder behavior with real
        file processing logic.
        """
