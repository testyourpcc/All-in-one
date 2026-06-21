from app.modules.base import ToolModule
from app.modules.excel_batch_edit import ExcelBatchEditModule
from app.modules.pdf_compress import PdfCompressModule
from app.modules.pdf_merge import PdfMergeModule
from app.modules.pdf_split import PdfSplitModule
from app.modules.word_batch_edit import WordBatchEditModule
from app.schemas.tool import ToolMetadata


class ModuleRegistry:
    def __init__(self) -> None:
        self._modules: dict[str, ToolModule] = {}

    def register(self, module: ToolModule) -> None:
        if module.slug in self._modules:
            raise ValueError(f"Tool module already registered: {module.slug}")
        self._modules[module.slug] = module

    def get(self, slug: str) -> ToolModule | None:
        return self._modules.get(slug)

    def list(self) -> list[ToolMetadata]:
        return [module.metadata() for module in self._modules.values()]


def create_default_registry() -> ModuleRegistry:
    registry = ModuleRegistry()
    registry.register(PdfMergeModule())
    registry.register(PdfSplitModule())
    registry.register(PdfCompressModule())
    registry.register(ExcelBatchEditModule())
    registry.register(WordBatchEditModule())
    return registry


module_registry = create_default_registry()
