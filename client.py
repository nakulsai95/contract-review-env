# Copyright (c) 2024. All rights reserved.
"""Contract Review Environment Client."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

try:
    from .models import ContractReviewAction, ContractReviewObservation
except ImportError:
    from models import ContractReviewAction, ContractReviewObservation


class ContractReviewEnv(
    EnvClient[ContractReviewAction, ContractReviewObservation, State]
):
    """
    Client for the Contract Review Environment.

    Example:
        >>> with ContractReviewEnv(base_url="http://localhost:8000") as client:
        ...     result = client.reset(difficulty="easy")
        ...     print(result.observation.clause_text)
        ...
        ...     result = client.step(ContractReviewAction(clause_type="indemnification"))
        ...     print(result.observation.feedback)

    Example with Docker:
        >>> client = ContractReviewEnv.from_docker_image("contract-review-env:latest")
        >>> try:
        ...     result = client.reset(difficulty="medium")
        ...     result = client.step(ContractReviewAction(
        ...         clause_type="termination",
        ...         risk_level="high",
        ...         issues=["no_notice_period"],
        ...         explanation="No notice period is provided."
        ...     ))
        ... finally:
        ...     client.close()
    """

    def _step_payload(self, action: ContractReviewAction) -> Dict:
        return {
            "action_type": action.action_type,
            "clause_type": action.clause_type,
            "risk_level": action.risk_level,
            "issues": action.issues,
            "explanation": action.explanation,
            "suggested_edit": action.suggested_edit,
        }

    def _parse_result(self, payload: Dict) -> StepResult[ContractReviewObservation]:
        obs_data = payload.get("observation", {})
        observation = ContractReviewObservation(
            clause_text=obs_data.get("clause_text", ""),
            clause_id=obs_data.get("clause_id", ""),
            task_description=obs_data.get("task_description", ""),
            difficulty=obs_data.get("difficulty", "easy"),
            feedback=obs_data.get("feedback", ""),
            clauses_remaining=obs_data.get("clauses_remaining", 0),
            context_info=obs_data.get("context_info", ""),
            related_clauses_summary=obs_data.get("related_clauses_summary", ""),
            done=payload.get("done", False),
            reward=payload.get("reward"),
            metadata=obs_data.get("metadata", {}),
        )
        return StepResult(
            observation=observation,
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> State:
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )
