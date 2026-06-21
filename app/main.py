from html import escape
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.api.v1 import health, jobs, tools
from app.core.config import ensure_storage_dirs, settings
from app.services.module_registry import module_registry

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(tools.router, prefix=settings.api_prefix)
app.include_router(jobs.router, prefix=settings.api_prefix)


@app.on_event("startup")
def on_startup() -> None:
    ensure_storage_dirs()


STYLE = """
:root {
    color-scheme: light;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #f4f7fb;
    color: #172033;
}
* {
    box-sizing: border-box;
}
body {
    margin: 0;
    min-height: 100vh;
    background:
        radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 32rem),
        linear-gradient(180deg, #f8fafc 0%, #eef3f8 100%);
}
main {
    width: min(1180px, calc(100% - 32px));
    margin: 0 auto;
    padding: 32px 0 48px;
}
.hero {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: end;
    gap: 24px;
    padding: 32px 0 24px;
    border-bottom: 1px solid #dbe3ef;
}
.hero-kicker {
    margin: 0 0 10px;
    color: #2563eb;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
h1 {
    margin: 0;
    max-width: 800px;
    font-size: clamp(34px, 5vw, 56px);
    line-height: 1.02;
}
.hero-copy {
    max-width: 720px;
    margin: 16px 0 0;
    color: #526071;
    font-size: 17px;
    line-height: 1.6;
}
.links, .tabs {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 20px;
}
.links a, .tab, button, .back-link {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 40px;
    border: 1px solid #c8d3e1;
    border-radius: 8px;
    background: #ffffff;
    color: #172033;
    padding: 10px 14px;
    font: inherit;
    font-weight: 650;
    text-decoration: none;
    cursor: pointer;
}
.links a:first-child {
    border-color: #2563eb;
    background: #2563eb;
    color: #ffffff;
}
.tab {
    min-width: 190px;
    justify-content: flex-start;
    gap: 10px;
    padding: 14px 16px;
}
.tab.active {
    border-color: #2563eb;
    background: #eaf1ff;
    color: #1d4ed8;
}
.tab strong {
    display: block;
}
.tab span {
    display: block;
    margin-top: 2px;
    color: #66758a;
    font-size: 12px;
}
.section-label {
    margin: 28px 0 14px;
    color: #66758a;
    font-size: 13px;
    font-weight: 750;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.tool-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 14px;
}
.tool-card, .tool-panel {
    border: 1px solid #dbe3ef;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.9);
    padding: 18px;
}
.tool-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 210px;
    border-left: 4px solid var(--accent);
    color: inherit;
    text-decoration: none;
}
.tool-card:hover {
    border-color: color-mix(in srgb, var(--accent), white 48%);
    background: #ffffff;
}
.tool-topline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    color: #66758a;
    font-size: 12px;
    font-weight: 700;
}
.pill {
    border-radius: 999px;
    background: color-mix(in srgb, var(--accent), white 90%);
    color: var(--accent);
    padding: 5px 9px;
}
h2 {
    margin: 0;
    font-size: 28px;
}
h3 {
    margin: 18px 0 8px;
    font-size: 20px;
}
.tool-card p, .tool-panel p {
    color: #526071;
    line-height: 1.55;
}
.open-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 22px;
    color: var(--accent);
    font-weight: 750;
}
.tool-layout {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 320px;
    gap: 18px;
    margin-top: 22px;
}
.tool-panel form {
    display: grid;
    gap: 14px;
    margin-top: 18px;
}
.tool-panel label {
    display: grid;
    gap: 8px;
    color: #526071;
    font-weight: 700;
}
input[type="file"] {
    width: 100%;
    min-height: 44px;
    border: 1px dashed #9fb1ca;
    border-radius: 8px;
    background: #ffffff;
    color: #526071;
    padding: 9px;
    font: inherit;
}
button {
    border-color: #2563eb;
    background: #2563eb;
    color: #ffffff;
}
.meta-list {
    display: grid;
    gap: 10px;
    margin: 0;
}
.meta-list div {
    display: grid;
    gap: 3px;
    border-bottom: 1px solid #edf1f7;
    padding-bottom: 10px;
}
.meta-list dt {
    color: #66758a;
    font-size: 12px;
    font-weight: 750;
    text-transform: uppercase;
}
.meta-list dd {
    margin: 0;
}
.empty {
    border: 1px dashed #b7c3d3;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.72);
    padding: 24px;
    color: #526071;
}
@media (max-width: 820px) {
    main {
        width: min(100% - 24px, 1180px);
        padding-top: 18px;
    }
    .hero, .tool-layout {
        grid-template-columns: 1fr;
    }
    .tab {
        width: 100%;
    }
}
"""


GROUPS = {
    "common": {
        "title": "Tool dung chung",
        "subtitle": "Cac tool co the dung ngay cho xu ly file hang ngay.",
    },
    "custom": {
        "title": "Tool rieng cua toi",
        "subtitle": "Khong gian cho workflow rieng, automation rieng va cac module noi bo.",
    },
}


CATEGORY_ACCENTS = {
    "word": "#2563eb",
    "excel": "#16803c",
    "pdf": "#b45309",
    "general": "#4f46e5",
}


def page_shell(title: str, body: str) -> str:
    return f"""
    <!doctype html>
    <html lang="vi">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{escape(title)}</title>
        <style>{STYLE}</style>
    </head>
    <body>
        <main>{body}</main>
    </body>
    </html>
    """


def tool_accent(tool: Any) -> str:
    return CATEGORY_ACCENTS.get(tool.category, CATEGORY_ACCENTS["general"])


def render_tabs(active_scope: str) -> str:
    tabs = []
    for scope, config in GROUPS.items():
        active = " active" if scope == active_scope else ""
        tabs.append(
            f"""
            <a class="tab{active}" href="/?scope={scope}">
                <span class="pill">{'Common' if scope == 'common' else 'Mine'}</span>
                <span>
                    <strong>{config["title"]}</strong>
                    <span>{config["subtitle"]}</span>
                </span>
            </a>
            """
        )
    return "\n".join(tabs)


def render_tool_card(tool: Any) -> str:
    accent = tool_accent(tool)
    return f"""
    <a class="tool-card" href="/tools/{escape(tool.slug)}" style="--accent: {accent}">
        <div>
            <div class="tool-topline">
                <span>{escape(tool.slug)}</span>
                <span class="pill">{escape(tool.category)}</span>
            </div>
            <h3>{escape(tool.name)}</h3>
            <p>{escape(tool.description)}</p>
        </div>
        <div class="open-row">
            <span>Open tool</span>
            <span>-></span>
        </div>
    </a>
    """


@app.get("/", response_class=HTMLResponse)
def home(scope: str = "common") -> str:
    active_scope = scope if scope in GROUPS else "common"
    scoped_tools = [
        tool for tool in module_registry.list()
        if tool.scope == active_scope
    ]
    cards = "\n".join(render_tool_card(tool) for tool in scoped_tools)
    if not cards:
        cards = """
        <div class="empty">
            Chua co tool nao trong nhom nay. Khi them module moi, no se xuat hien o day.
        </div>
        """

    body = f"""
    <header class="hero">
        <div>
            <p class="hero-kicker">File Tool Platform</p>
            <h1>{GROUPS[active_scope]["title"]}</h1>
            <p class="hero-copy">{GROUPS[active_scope]["subtitle"]} Trang nay chi hien thi danh sach tool; bam vao tung tool de mo man hinh su dung rieng.</p>
            <nav class="links">
                <a href="/docs">API docs</a>
                <a href="{settings.api_prefix}/tools">Tools JSON</a>
                <a href="{settings.api_prefix}/health">Health</a>
            </nav>
        </div>
    </header>
    <nav class="tabs" aria-label="Tool groups">
        {render_tabs(active_scope)}
    </nav>
    <p class="section-label">Available tools</p>
    <section class="tool-grid">
        {cards}
    </section>
    """
    return page_shell(settings.app_name, body)


def render_tool_action(tool: Any) -> str:
    if tool.accepts_files:
        accept = ",".join(tool.input_extensions)
        return f"""
        <form method="post" action="{settings.api_prefix}/tools/{escape(tool.slug)}/run" enctype="multipart/form-data">
            <label>
                <span>Upload input file</span>
                <input type="file" name="file" accept="{escape(accept)}" required>
            </label>
            <button type="submit">Convert and download</button>
        </form>
        """

    return f"""
    <form method="post" action="{settings.api_prefix}/jobs/{escape(tool.slug)}">
        <button type="submit">Run preview</button>
    </form>
    <p>Tool nay dang la placeholder. Module xu ly thuc te se duoc gan vao sau.</p>
    """


@app.get("/tools/{slug}", response_class=HTMLResponse)
def tool_detail(slug: str) -> str:
    tool = module_registry.get(slug)
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")

    metadata = tool.metadata()
    accent = tool_accent(metadata)
    extensions = ", ".join(metadata.input_extensions) or "No file upload yet"
    output = metadata.output_extension or "Not configured"
    body = f"""
    <a class="back-link" href="/?scope={escape(metadata.scope)}">Back to {GROUPS.get(metadata.scope, GROUPS["common"])["title"]}</a>
    <header class="hero">
        <div>
            <p class="hero-kicker">{escape(metadata.category)} / {escape(metadata.scope)}</p>
            <h1>{escape(metadata.name)}</h1>
            <p class="hero-copy">{escape(metadata.description)}</p>
        </div>
    </header>
    <section class="tool-layout" style="--accent: {accent}">
        <article class="tool-panel">
            <h2>Use this tool</h2>
            {render_tool_action(metadata)}
        </article>
        <aside class="tool-panel">
            <h2>Tool info</h2>
            <dl class="meta-list">
                <div>
                    <dt>Slug</dt>
                    <dd>{escape(metadata.slug)}</dd>
                </div>
                <div>
                    <dt>Group</dt>
                    <dd>{escape(GROUPS.get(metadata.scope, GROUPS["common"])["title"])}</dd>
                </div>
                <div>
                    <dt>Category</dt>
                    <dd>{escape(metadata.category)}</dd>
                </div>
                <div>
                    <dt>Input</dt>
                    <dd>{escape(extensions)}</dd>
                </div>
                <div>
                    <dt>Output</dt>
                    <dd>{escape(output)}</dd>
                </div>
            </dl>
        </aside>
    </section>
    """
    return page_shell(f"{metadata.name} - {settings.app_name}", body)
