from abc import ABC, abstractmethod
from typing import Any

from app.schemas.tool import ToolMetadata


class ToolModule(ABC):
    """Base class for every installable tool module."""

    slug: str
    name: str
    description: str
    category: str = "general"

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            slug=self.slug,
            name=self.name,
            description=self.description,
            category=self.category,
        )

    @abstractmethod
    def run(self, **kwargs: Any) -> dict[str, Any]:
        """Execute the tool.

        Concrete modules will replace this placeholder behavior with real
        file processing logic.
        """
