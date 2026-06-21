from typing import Any

from app.modules.base import ToolModule


class PdfMergeModule(ToolModule):
    slug = "pdf-merge"
    name = "Merge PDF"
    description = "Merge multiple PDF files into one output file."
    category = "pdf"

    def run(self, **kwargs: Any) -> dict[str, Any]:
        return {
            "status": "not_implemented",
            "tool": self.slug,
            "message": "PDF merge processing will be added here.",
        }
