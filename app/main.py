from collections import defaultdict
from html import escape
from typing import Any

from fastapi import FastAPI
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


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    tools_by_category: dict[str, list[Any]] = defaultdict(list)
    for tool in module_registry.list():
        tools_by_category[tool.category].append(tool)

    group_config = {
        "word": {
            "title": "Word tools",
            "eyebrow": "Documents",
            "summary": "Batch editing and document automation tools for Word files.",
            "accent": "#2563eb",
            "badge": "W",
        },
        "excel": {
            "title": "Excel tools",
            "eyebrow": "Spreadsheets",
            "summary": "Fast utilities for spreadsheet cleanup and repeatable Excel edits.",
            "accent": "#16803c",
            "badge": "X",
        },
        "pdf": {
            "title": "PDF utilities",
            "eyebrow": "Files",
            "summary": "Merge, split, and compress PDF files from one dashboard.",
            "accent": "#b45309",
            "badge": "P",
        },
    }

    def render_tool_card(tool: Any, accent: str) -> str:
        return f"""
        <article class="tool-card" style="--accent: {accent}">
            <div>
                <div class="tool-topline">
                    <span class="status-dot"></span>
                    <span>{escape(tool.slug)}</span>
                </div>
                <h3>{escape(tool.name)}</h3>
                <p>{escape(tool.description)}</p>
            </div>
            <form method="post" action="{settings.api_prefix}/jobs/{escape(tool.slug)}">
                <button type="submit">Run preview</button>
            </form>
        </article>
        """

    def render_group(category: str, featured: bool = False) -> str:
        category_tools = tools_by_category.get(category, [])
        if not category_tools:
            return ""

        config = group_config[category]
        cards = "\n".join(
            render_tool_card(tool, config["accent"])
            for tool in category_tools
        )
        class_name = "tool-group featured" if featured else "tool-group"
        return f"""
        <section class="{class_name}" style="--accent: {config["accent"]}">
            <div class="group-heading">
                <span class="group-badge">{config["badge"]}</span>
                <div>
                    <p>{config["eyebrow"]}</p>
                    <h2>{config["title"]}</h2>
                    <span>{config["summary"]}</span>
                </div>
            </div>
            <div class="tool-grid">
                {cards}
            </div>
        </section>
        """

    office_groups = "\n".join(
        render_group(category, featured=True)
        for category in ("word", "excel")
    )
    pdf_group = render_group("pdf")
    installed_count = len(module_registry.list())

    return f"""
    <!doctype html>
    <html lang="vi">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{settings.app_name}</title>
        <style>
            :root {{
                color-scheme: light;
                font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                background: #f4f7fb;
                color: #172033;
            }}
            * {{
                box-sizing: border-box;
            }}
            body {{
                margin: 0;
                min-height: 100vh;
                background:
                    radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 32rem),
                    linear-gradient(180deg, #f8fafc 0%, #eef3f8 100%);
            }}
            main {{
                width: min(1180px, calc(100% - 32px));
                margin: 0 auto;
                padding: 32px 0 48px;
            }}
            .hero {{
                display: grid;
                grid-template-columns: 1fr auto;
                align-items: end;
                gap: 24px;
                padding: 32px 0 26px;
                border-bottom: 1px solid #dbe3ef;
            }}
            .hero-kicker {{
                margin: 0 0 10px;
                color: #2563eb;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }}
            h1 {{
                margin: 0;
                max-width: 760px;
                font-size: clamp(34px, 5vw, 56px);
                line-height: 1.02;
            }}
            .hero-copy {{
                max-width: 680px;
                margin: 16px 0 0;
                color: #526071;
                font-size: 17px;
                line-height: 1.6;
            }}
            .stats {{
                display: grid;
                gap: 10px;
                min-width: 190px;
            }}
            .stat-card {{
                border: 1px solid #dbe3ef;
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.82);
                padding: 16px;
            }}
            .stat-card strong {{
                display: block;
                font-size: 30px;
                line-height: 1;
            }}
            .stat-card span {{
                display: block;
                margin-top: 6px;
                color: #66758a;
                font-size: 13px;
            }}
            .links {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-top: 20px;
            }}
            .links a, button {{
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
            }}
            .links a:first-child {{
                border-color: #2563eb;
                background: #2563eb;
                color: #ffffff;
            }}
            .section-label {{
                margin: 28px 0 14px;
                color: #66758a;
                font-size: 13px;
                font-weight: 750;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }}
            .office-grid {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 18px;
            }}
            .tool-group {{
                border: 1px solid #dbe3ef;
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.88);
                padding: 18px;
            }}
            .tool-group.featured {{
                min-height: 320px;
            }}
            .group-heading {{
                display: flex;
                gap: 14px;
                align-items: flex-start;
                margin-bottom: 16px;
            }}
            .group-badge {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 44px;
                height: 44px;
                border-radius: 8px;
                background: color-mix(in srgb, var(--accent), white 86%);
                color: var(--accent);
                font-size: 20px;
                font-weight: 800;
            }}
            .group-heading p {{
                margin: 0 0 3px;
                color: var(--accent);
                font-size: 12px;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }}
            .group-heading h2 {{
                margin: 0 0 6px;
                font-size: 24px;
            }}
            .group-heading span {{
                color: #66758a;
                line-height: 1.5;
            }}
            .tool-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
                gap: 12px;
            }}
            .tool-card {{
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                min-height: 180px;
                border: 1px solid #dbe3ef;
                border-left: 4px solid var(--accent);
                border-radius: 8px;
                background: #ffffff;
                padding: 16px;
            }}
            .tool-topline {{
                display: flex;
                align-items: center;
                gap: 7px;
                color: #66758a;
                font-size: 12px;
                font-weight: 700;
            }}
            .status-dot {{
                width: 8px;
                height: 8px;
                border-radius: 999px;
                background: var(--accent);
            }}
            h3 {{
                margin: 14px 0 8px;
                font-size: 19px;
            }}
            .tool-card p {{
                margin: 0;
                color: #526071;
                line-height: 1.5;
            }}
            .tool-card form {{
                margin-top: 18px;
            }}
            .tool-card button {{
                width: 100%;
                border-color: color-mix(in srgb, var(--accent), white 62%);
                color: var(--accent);
                background: color-mix(in srgb, var(--accent), white 94%);
            }}
            .secondary {{
                margin-top: 18px;
            }}
            @media (max-width: 780px) {{
                main {{
                    width: min(100% - 24px, 1180px);
                    padding-top: 18px;
                }}
                .hero {{
                    grid-template-columns: 1fr;
                    padding-top: 18px;
                }}
                .stats {{
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }}
                .office-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <main>
            <header class="hero">
                <div>
                    <p class="hero-kicker">File Tool Platform</p>
                    <h1>Chon tool, upload file, va xu ly nhanh tren web.</h1>
                    <p class="hero-copy">Dashboard nay gom cac module thanh nhom Word va Excel de sau nay them tool moi gon hon. API van san sang cho workflow tu dong va tich hop frontend rieng.</p>
                    <nav class="links">
                        <a href="/docs">API docs</a>
                        <a href="{settings.api_prefix}/tools">Tools JSON</a>
                        <a href="{settings.api_prefix}/health">Health</a>
                    </nav>
                </div>
                <aside class="stats" aria-label="Installed tool summary">
                    <div class="stat-card">
                        <strong>{installed_count}</strong>
                        <span>Installed tools</span>
                    </div>
                    <div class="stat-card">
                        <strong>2</strong>
                        <span>Main office groups</span>
                    </div>
                </aside>
            </header>

            <p class="section-label">Office groups</p>
            <div class="office-grid">
                {office_groups}
            </div>

            <div class="secondary">
                <p class="section-label">Other file tools</p>
                {pdf_group}
            </div>
        </main>
    </body>
    </html>
    """
