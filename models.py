# Copyright (c) 2024. All rights reserved.
# Data models for the Contract Review Environment.

from typing import List, Optional

from openenv.core.env_server.types import Action, Observation
from pydantic import Field


class ContractReviewAction(Action):
    """Action for the Contract Review environment.

    The agent submits its analysis of a contract clause, including
    classification, risk assessment, identified issues, and optionally
    a suggested edit.
    """

    action_type: str = Field(
        default="submit_review",
        description=(
            "Action type: 'submit_review' (submit analysis), 'ask_context' "
            "(request surrounding contract context), 'view_full_contract' "
            "(view other clauses in the contract), 'check_jurisdiction' "
            "(check applicable jurisdiction info)"
        ),
    )
    clause_type: str = Field(
        default="",
        description=(
            "The type of contract clause. One of: indemnification, "
            "limitation_of_liability, termination, confidentiality, "
            "ip_assignment, non_compete, payment_terms, governing_law, "
            "force_majeure, warranty, data_protection, dispute_resolution. "
            "Required for submit_review actions."
        ),
    )
    risk_level: str = Field(
        default="low",
        description="Risk assessment: low, medium, or high",
    )
    issues: List[str] = Field(
        default_factory=list,
        description="List of identified issues/red flags in the clause",
    )
    explanation: str = Field(
        default="",
        description="Explanation of the risk assessment and identified issues",
    )
    suggested_edit: Optional[str] = Field(
        default=None,
        description="Suggested revised clause text to address the issues (hard task only)",
    )


class ContractReviewObservation(Observation):
    """Observation from the Contract Review environment."""

    clause_text: str = Field(default="", description="The contract clause to review")
    clause_id: str = Field(default="", description="Unique identifier for this clause")
    task_description: str = Field(
        default="", description="Description of what the agent should do"
    )
    difficulty: str = Field(
        default="easy", description="Task difficulty: easy, medium, or hard"
    )
    feedback: str = Field(
        default="", description="Feedback from the grader on the last action"
    )
    clauses_remaining: int = Field(
        default=0, description="Number of clauses remaining in this episode"
    )
    context_info: str = Field(
        default="",
        description=(
            "Additional context about the contract (populated by "
            "ask_context/view_full_contract/check_jurisdiction actions)"
        ),
    )
