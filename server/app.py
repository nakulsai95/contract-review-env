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


def main(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
