# Copyright (c) 2024. All rights reserved.
"""
FastAPI application for the Contract Review Environment.

Endpoints:
    - POST /reset: Reset the environment
    - POST /step: Execute an action
    - GET /state: Get current environment state
    - GET /schema: Get action/observation schemas
    - WS /ws: WebSocket endpoint for persistent sessions
"""

try:
    from openenv.core.env_server.http_server import create_app
except Exception as e:
    raise ImportError(
        "openenv is required. Install with: pip install openenv-core"
    ) from e

try:
    from ..models import ContractReviewAction, ContractReviewObservation
    from .contract_review_environment import ContractReviewEnvironment
except (ImportError, ModuleNotFoundError):
    from models import ContractReviewAction, ContractReviewObservation
    from server.contract_review_environment import ContractReviewEnvironment


app = create_app(
    ContractReviewEnvironment,
    ContractReviewAction,
    ContractReviewObservation,
    env_name="contract_review_env",
    max_concurrent_envs=1,
)


from fastapi.responses import HTMLResponse


LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contract Review Environment</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               background: #0f172a; color: #e2e8f0; line-height: 1.6; padding: 2rem; }
        .container { max-width: 900px; margin: 0 auto; }
        h1 { font-size: 2rem; margin-bottom: 0.5rem; color: #f8fafc; }
        .badge { display: inline-block; background: #22c55e; color: #000; padding: 2px 10px;
                 border-radius: 12px; font-size: 0.8rem; font-weight: 600; margin-left: 8px; }
        .subtitle { color: #94a3b8; margin-bottom: 2rem; }
        .card { background: #1e293b; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;
                border: 1px solid #334155; }
        .card h2 { font-size: 1.1rem; color: #60a5fa; margin-bottom: 0.75rem; }
        .endpoint { display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;
                    font-family: 'Courier New', monospace; font-size: 0.9rem; }
        .method { padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.75rem; }
        .get { background: #166534; color: #4ade80; }
        .post { background: #854d0e; color: #fbbf24; }
        .ws { background: #581c87; color: #c084fc; }
        .path { color: #f8fafc; }
        .desc { color: #94a3b8; font-size: 0.85rem; margin-left: 60px; margin-bottom: 0.75rem; }
        pre { background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 1rem;
              overflow-x: auto; font-size: 0.85rem; color: #e2e8f0; margin: 0.5rem 0; }
        .key { color: #60a5fa; }
        .str { color: #4ade80; }
        .num { color: #fbbf24; }
        .tasks { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1rem 0; }
        .task { background: #0f172a; border-radius: 8px; padding: 1rem; border: 1px solid #334155; }
        .task h3 { font-size: 0.95rem; margin-bottom: 0.5rem; }
        .easy { border-left: 3px solid #4ade80; }
        .medium { border-left: 3px solid #fbbf24; }
        .hard { border-left: 3px solid #f87171; }
        a { color: #60a5fa; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .stats { display: flex; gap: 2rem; margin: 1rem 0; flex-wrap: wrap; }
        .stat { text-align: center; }
        .stat-num { font-size: 1.5rem; font-weight: 700; color: #f8fafc; }
        .stat-label { font-size: 0.8rem; color: #94a3b8; }
        .try-btn { display: inline-block; background: #3b82f6; color: white; padding: 6px 16px;
                   border-radius: 6px; font-size: 0.85rem; margin-top: 0.5rem; }
        .try-btn:hover { background: #2563eb; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Contract Review Environment <span class="badge">RUNNING</span></h1>
        <p class="subtitle">OpenEnv environment for AI-powered legal contract clause review</p>

        <div class="stats">
            <div class="stat"><div class="stat-num">55</div><div class="stat-label">Scenarios</div></div>
            <div class="stat"><div class="stat-num">17</div><div class="stat-label">Clause Types</div></div>
            <div class="stat"><div class="stat-num">3</div><div class="stat-label">Difficulty Levels</div></div>
            <div class="stat"><div class="stat-num">4</div><div class="stat-label">Action Types</div></div>
        </div>

        <div class="card">
            <h2>API Endpoints</h2>
            <div class="endpoint"><span class="method get">GET</span> <span class="path">/health</span></div>
            <div class="desc">Health check &mdash; returns {"status": "healthy"}</div>

            <div class="endpoint"><span class="method get">GET</span> <span class="path">/metadata</span></div>
            <div class="desc">Environment name and description</div>

            <div class="endpoint"><span class="method get">GET</span> <span class="path">/schema</span></div>
            <div class="desc">Action, observation, and state JSON schemas</div>

            <div class="endpoint"><span class="method post">POST</span> <span class="path">/reset</span></div>
            <div class="desc">Start a new episode &mdash; returns first clause</div>

            <div class="endpoint"><span class="method post">POST</span> <span class="path">/step</span></div>
            <div class="desc">Submit an action &mdash; returns observation + reward</div>

            <div class="endpoint"><span class="method get">GET</span> <span class="path">/state</span></div>
            <div class="desc">Current episode state (episode_id, step_count)</div>

            <div class="endpoint"><span class="method ws">WS</span> <span class="path">/ws</span></div>
            <div class="desc">WebSocket for stateful agent sessions (used by inference.py)</div>

            <a href="/docs" class="try-btn">Interactive API Docs (Swagger)</a>
        </div>

        <div class="card">
            <h2>Tasks</h2>
            <div class="tasks">
                <div class="task easy">
                    <h3>Easy: Classification</h3>
                    <p style="font-size:0.85rem;color:#94a3b8">Classify clause type<br>5 clauses/episode<br>Baseline: ~0.85</p>
                </div>
                <div class="task medium">
                    <h3>Medium: Risk Assessment</h3>
                    <p style="font-size:0.85rem;color:#94a3b8">Type + risk + issues<br>3 clauses/episode<br>Baseline: ~0.55</p>
                </div>
                <div class="task hard">
                    <h3>Hard: Full Review</h3>
                    <p style="font-size:0.85rem;color:#94a3b8">Full review + edits<br>2 clauses/episode<br>Baseline: ~0.40</p>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Quick Start</h2>
<pre><span class="key">POST</span> /reset
{
  <span class="str">"difficulty"</span>: <span class="str">"medium"</span>,
  <span class="str">"seed"</span>: <span class="num">42</span>
}

<span class="key">POST</span> /step
{
  <span class="str">"action"</span>: {
    <span class="str">"action_type"</span>: <span class="str">"submit_review"</span>,
    <span class="str">"clause_type"</span>: <span class="str">"indemnification"</span>,
    <span class="str">"risk_level"</span>: <span class="str">"high"</span>,
    <span class="str">"issues"</span>: [<span class="str">"unilateral"</span>, <span class="str">"no cap"</span>],
    <span class="str">"explanation"</span>: <span class="str">"One-sided indemnification..."</span>,
    <span class="str">"suggested_edit"</span>: <span class="str">"Add mutual indemnification..."</span>
  }
}</pre>
        </div>

        <div class="card">
            <h2>Multi-Turn Actions</h2>
            <p style="font-size:0.9rem;color:#94a3b8;margin-bottom:0.75rem">
                Before submitting a review, gather context:
            </p>
<pre><span class="str">"ask_context"</span>      &rarr; Contract type, parties, value
<span class="str">"view_full_contract"</span> &rarr; Summary of other clauses
<span class="str">"check_jurisdiction"</span> &rarr; Jurisdiction &amp; enforceability notes
<span class="str">"submit_review"</span>     &rarr; Submit analysis (graded)</pre>
        </div>

        <div class="card" style="border-color:#334155">
            <h2>Links</h2>
            <p><a href="/docs">Interactive API Docs (Swagger UI)</a></p>
            <p><a href="/schema">JSON Schemas</a></p>
            <p><a href="/health">Health Check</a></p>
        </div>
    </div>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    return LANDING_PAGE


def main(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
