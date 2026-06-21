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
    tool_cards = "\n".join(
        f"""
        <article class="tool-card">
            <div>
                <p class="category">{tool.category}</p>
                <h2>{tool.name}</h2>
                <p>{tool.description}</p>
            </div>
            <form method="post" action="{settings.api_prefix}/jobs/{tool.slug}">
                <button type="submit">Run placeholder</button>
            </form>
        </article>
        """
        for tool in module_registry.list()
    )

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
                font-family: Arial, sans-serif;
                background: #f6f7f9;
                color: #172033;
            }}
            body {{
                margin: 0;
            }}
            main {{
                width: min(1040px, calc(100% - 32px));
                margin: 40px auto;
            }}
            header {{
                margin-bottom: 24px;
            }}
            h1 {{
                margin: 0 0 8px;
                font-size: 32px;
            }}
            .links {{
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
                margin-top: 16px;
            }}
            .links a, button {{
                border: 1px solid #c8d0dc;
                border-radius: 8px;
                background: #ffffff;
                color: #172033;
                padding: 10px 14px;
                text-decoration: none;
                cursor: pointer;
            }}
            .tools {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 16px;
            }}
            .tool-card {{
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                min-height: 180px;
                border: 1px solid #d9dee7;
                border-radius: 8px;
                background: #ffffff;
                padding: 18px;
            }}
            .category {{
                margin: 0 0 8px;
                color: #59657a;
                font-size: 13px;
                text-transform: uppercase;
            }}
            h2 {{
                margin: 0 0 8px;
                font-size: 20px;
            }}
            p {{
                line-height: 1.5;
            }}
        </style>
    </head>
    <body>
        <main>
            <header>
                <h1>{settings.app_name}</h1>
                <p>Local tool platform. Mỗi card bên dưới là một module đã đăng ký trong registry.</p>
                <nav class="links">
                    <a href="/docs">API docs</a>
                    <a href="{settings.api_prefix}/tools">Tools JSON</a>
                    <a href="{settings.api_prefix}/health">Health</a>
                </nav>
            </header>
            <section class="tools">
                {tool_cards}
            </section>
        </main>
    </body>
    </html>
    """
