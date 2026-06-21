from typing import Any

from app.modules.base import ToolModule


class ExcelBatchEditModule(ToolModule):
    slug = "excel-batch-edit"
    name = "Excel Batch Edit"
    description = "Apply batch edits to Excel files."
    category = "excel"
    scope = "custom"

    def run(self, **kwargs: Any) -> dict[str, Any]:
        return {
            "status": "not_implemented",
            "tool": self.slug,
            "message": "Excel batch editing will be added here.",
        }
