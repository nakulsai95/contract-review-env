# Copyright (c) 2024. All rights reserved.
"""
Contract Review Environment Implementation.

An environment where an AI agent reviews contract clauses,
classifies them, assesses risk, identifies issues, and suggests edits.
"""

import random
from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import ContractReviewAction, ContractReviewObservation
    from ..scenarios import SCENARIOS, CONTEXT_DATA, get_scenarios_by_difficulty
    from ..graders import grade_task_easy, grade_task_medium, grade_task_hard
except ImportError:
    from models import ContractReviewAction, ContractReviewObservation
    from scenarios import SCENARIOS, CONTEXT_DATA, get_scenarios_by_difficulty
    from graders import grade_task_easy, grade_task_medium, grade_task_hard


# Task descriptions shown to the agent
TASK_DESCRIPTIONS = {
    "easy": (
        "TASK: Clause Classification (Easy)\n"
        "Review the contract clause below and classify its type.\n"
        "Choose one of: indemnification, limitation_of_liability, termination, "
        "confidentiality, ip_assignment, non_compete, payment_terms, governing_law, "
        "force_majeure, warranty, data_protection, dispute_resolution.\n"
        "Set risk_level to 'low' (not graded for this task)."
    ),
    "medium": (
        "TASK: Risk Assessment (Medium)\n"
        "Review the contract clause below. You must:\n"
        "1. Classify the clause type\n"
        "2. Assess the risk level (low, medium, or high)\n"
        "3. Identify specific issues/red flags (list of short descriptions)\n"
        "4. Provide an explanation of your assessment\n"
    ),
    "hard": (
        "TASK: Full Contract Review (Hard)\n"
        "Review the contract clause below. You must:\n"
        "1. Classify the clause type\n"
        "2. Assess the risk level (low, medium, or high)\n"
        "3. Identify specific issues/red flags\n"
        "4. Explain the risks and their implications\n"
        "5. Provide a suggested revised clause that addresses the identified issues\n"
    ),
}

# Number of clauses per episode by difficulty
CLAUSES_PER_EPISODE = {
    "easy": 5,
    "medium": 3,
    "hard": 2,
}

# Maximum steps per episode (allows information-gathering before submitting)
MAX_STEPS_PER_EPISODE = {
    "easy": 10,
    "medium": 9,
    "hard": 8,
}


class ContractReviewEnvironment(Environment):
    """
    Contract clause review environment.

    The agent reviews contract clauses across three difficulty levels:
    - Easy: classify clause type only
    - Medium: classify + risk assessment + identify issues
    - Hard: full review with suggested edits

    Each episode presents multiple clauses. The agent receives a reward
    after reviewing each clause, with partial credit for partially correct answers.
    """

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._difficulty = "easy"
        self._clauses = []
        self._current_clause_idx = 0
        self._rewards = []
        self._rng = random.Random(42)
        self._steps_used = 0
        self._max_steps = 10

    def reset(self, seed: int | None = None, **kwargs) -> ContractReviewObservation:
        """Reset the environment with a new set of clauses.

        Args:
            seed: Random seed for reproducibility
            **kwargs: Additional options. Use difficulty="easy"|"medium"|"hard"
        """
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._difficulty = kwargs.get("difficulty", "easy")
        if self._difficulty not in TASK_DESCRIPTIONS:
            self._difficulty = "easy"

        self._rng = random.Random(seed if seed is not None else 42)
        self._rewards = []
        self._current_clause_idx = 0
        self._steps_used = 0
        self._max_steps = MAX_STEPS_PER_EPISODE[self._difficulty]

        # Select clauses for this episode
        available = get_scenarios_by_difficulty(self._difficulty)
        num_clauses = min(CLAUSES_PER_EPISODE[self._difficulty], len(available))
        self._clauses = self._rng.sample(available, num_clauses)

        clause = self._clauses[0]

        return ContractReviewObservation(
            clause_text=clause["clause_text"],
            clause_id=clause["id"],
            task_description=TASK_DESCRIPTIONS[self._difficulty],
            difficulty=self._difficulty,
            feedback="",
            clauses_remaining=len(self._clauses) - 1,
            done=False,
            reward=0.0,
        )

    def _build_context_response(self, clause_id: str, action_type: str) -> str:
        """Build context information string for information-gathering actions."""
        ctx = CONTEXT_DATA.get(clause_id, {})
        if not ctx:
            return "No additional context data available for this clause."

        if action_type == "ask_context":
            return (
                f"Contract Type: {ctx.get('contract_type', 'Unknown')}\n"
                f"Parties: {ctx.get('parties', 'Unknown')}\n"
                f"Contract Value: {ctx.get('contract_value', 'Unknown')}"
            )
        elif action_type == "view_full_contract":
            return (
                f"Contract Type: {ctx.get('contract_type', 'Unknown')}\n"
                f"Other Clauses Summary: {ctx.get('other_clauses_summary', 'No summary available.')}"
            )
        elif action_type == "check_jurisdiction":
            jurisdiction = ctx.get("jurisdiction", "Unknown")
            return (
                f"Jurisdiction: {jurisdiction}\n"
                f"Note: Review clause enforceability under {jurisdiction} law. "
                f"Local regulations and case law may affect interpretation."
            )
        return ""

    def _auto_submit_clause(self, action: ContractReviewAction) -> dict:
        """Grade the current clause using whatever the agent has provided so far."""
        clause = self._clauses[self._current_clause_idx]
        action_dict = {
            "clause_type": action.clause_type,
            "risk_level": action.risk_level,
            "issues": action.issues,
            "explanation": action.explanation,
            "suggested_edit": action.suggested_edit,
        }
        if self._difficulty == "easy":
            return grade_task_easy(action_dict, clause)
        elif self._difficulty == "medium":
            return grade_task_medium(action_dict, clause)
        else:
            return grade_task_hard(action_dict, clause)

    def _make_episode_complete_obs(self, feedback: str, result: dict) -> ContractReviewObservation:
        """Build the final observation when the episode is done."""
        avg_reward = sum(self._rewards) / len(self._rewards) if self._rewards else 0.0
        return ContractReviewObservation(
            clause_text="",
            clause_id="",
            task_description="Episode complete.",
            difficulty=self._difficulty,
            feedback=feedback + f"\n\nEpisode complete. Average score: {avg_reward:.3f}",
            clauses_remaining=0,
            context_info="",
            done=True,
            reward=avg_reward,
            metadata={
                "per_clause_rewards": self._rewards,
                "grading_details": result,
            },
        )

    def step(self, action: ContractReviewAction) -> ContractReviewObservation:
        """Process the agent's action on the current clause.

        Supports multi-turn interaction per clause:
        - 'ask_context': get contract context (type, parties, value)
        - 'view_full_contract': see summary of other clauses
        - 'check_jurisdiction': get jurisdiction-specific notes
        - 'submit_review': submit analysis for grading (default)

        Information-gathering actions cost 1 step but yield 0 reward.
        When the step budget is exhausted, the current action is auto-submitted.

        Args:
            action: The agent's action (information-gathering or review submission)

        Returns:
            Observation with context info, next clause, or episode completion
        """
        self._state.step_count += 1
        self._steps_used += 1

        clause = self._clauses[self._current_clause_idx]
        action_type = getattr(action, "action_type", "submit_review") or "submit_review"
        steps_remaining = self._max_steps - self._steps_used

        # --- Auto-submit on budget exhaustion ---
        if steps_remaining <= 0 and action_type != "submit_review":
            action_type = "submit_review"

        # --- Information-gathering actions ---
        if action_type in ("ask_context", "view_full_contract", "check_jurisdiction"):
            context_info = self._build_context_response(clause["id"], action_type)
            return ContractReviewObservation(
                clause_text=clause["clause_text"],
                clause_id=clause["id"],
                task_description=TASK_DESCRIPTIONS[self._difficulty],
                difficulty=self._difficulty,
                feedback=f"[{action_type}] Information retrieved. Steps remaining: {steps_remaining}",
                clauses_remaining=len(self._clauses) - self._current_clause_idx - 1,
                context_info=context_info,
                done=False,
                reward=0.0,
            )

        # --- Submit review (default) ---
        result = self._auto_submit_clause(action)
        step_reward = result["score"]
        self._rewards.append(step_reward)

        # Build feedback string
        feedback_parts = [f"Score: {step_reward:.2f}"]
        for k, v in result.items():
            if k != "score":
                feedback_parts.append(f"  {k}: {v:.2f}")
        feedback = "\n".join(feedback_parts)

        # Move to next clause
        self._current_clause_idx += 1
        done = self._current_clause_idx >= len(self._clauses)

        # Also end if step budget is fully exhausted
        if steps_remaining <= 0:
            done = True

        if done:
            return self._make_episode_complete_obs(feedback, result)
        else:
            next_clause = self._clauses[self._current_clause_idx]
            return ContractReviewObservation(
                clause_text=next_clause["clause_text"],
                clause_id=next_clause["id"],
                task_description=TASK_DESCRIPTIONS[self._difficulty],
                difficulty=self._difficulty,
                feedback=feedback + f"\nSteps remaining: {steps_remaining}",
                clauses_remaining=len(self._clauses) - self._current_clause_idx - 1,
                context_info="",
                done=False,
                reward=step_reward,
            )

    @property
    def state(self) -> State:
        return self._state
