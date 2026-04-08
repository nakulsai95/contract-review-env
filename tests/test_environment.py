import sys
import os
import pytest

# Ensure the parent package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from server.contract_review_environment import ContractReviewEnvironment
from models import ContractReviewAction
from scenarios import SCENARIOS


class TestEnvironment:
    def test_reset_easy(self):
        env = ContractReviewEnvironment()
        obs = env.reset(seed=42, difficulty="easy")
        assert obs.difficulty == "easy"
        assert obs.clause_text != ""
        assert obs.clauses_remaining > 0
        assert obs.done is False

    def test_reset_medium(self):
        env = ContractReviewEnvironment()
        obs = env.reset(seed=42, difficulty="medium")
        assert obs.difficulty == "medium"

    def test_reset_hard(self):
        env = ContractReviewEnvironment()
        obs = env.reset(seed=42, difficulty="hard")
        assert obs.difficulty == "hard"

    def test_full_easy_episode(self):
        env = ContractReviewEnvironment()
        obs = env.reset(seed=42, difficulty="easy")
        steps = 0
        while not obs.done:
            action = ContractReviewAction(clause_type="indemnification")
            obs = env.step(action)
            steps += 1
        assert steps == 5
        assert obs.done is True
        assert obs.reward > 0.0
        assert obs.reward < 1.0

    def test_full_medium_episode(self):
        env = ContractReviewEnvironment()
        obs = env.reset(seed=42, difficulty="medium")
        steps = 0
        while not obs.done:
            action = ContractReviewAction(
                clause_type="confidentiality",
                risk_level="high",
                issues=["overbroad"],
                explanation="Overbroad scope.",
            )
            obs = env.step(action)
            steps += 1
        assert steps == 3
        assert obs.done is True
        assert obs.reward > 0.0
        assert obs.reward < 1.0

    def test_full_hard_episode(self):
        env = ContractReviewEnvironment()
        obs = env.reset(seed=42, difficulty="hard")
        steps = 0
        while not obs.done:
            action = ContractReviewAction(
                action_type="submit_review",
                clause_type="indemnification",
                risk_level="medium",
                issues=["asymmetric caps"],
                explanation="Hidden imbalance in caps.",
                suggested_edit="Make caps symmetric.",
            )
            obs = env.step(action)
            steps += 1
        assert steps == 2
        assert obs.done is True
        assert obs.reward > 0.0
        assert obs.reward < 1.0

    def test_reproducibility(self):
        env1 = ContractReviewEnvironment()
        obs1 = env1.reset(seed=123, difficulty="easy")

        env2 = ContractReviewEnvironment()
        obs2 = env2.reset(seed=123, difficulty="easy")

        assert obs1.clause_id == obs2.clause_id
        assert obs1.clause_text == obs2.clause_text

    def test_state_tracking(self):
        env = ContractReviewEnvironment()
        env.reset(seed=42, difficulty="easy")
        assert env.state.step_count == 0

        env.step(ContractReviewAction(clause_type="indemnification"))
        assert env.state.step_count == 1

    def test_invalid_difficulty_defaults_to_easy(self):
        env = ContractReviewEnvironment()
        obs = env.reset(seed=42, difficulty="impossible")
        assert obs.difficulty == "easy"


class TestScoreClamping:
    """Ensure scores are strictly in (0, 1) — never 0.0 or 1.0."""

    def test_perfect_answers_not_exactly_1(self):
        for diff in ["easy", "medium", "hard"]:
            env = ContractReviewEnvironment()
            obs = env.reset(seed=42, difficulty=diff)
            while not obs.done:
                s = next((sc for sc in SCENARIOS if sc["id"] == obs.clause_id), None)
                if s:
                    action = ContractReviewAction(
                        action_type="submit_review",
                        clause_type=s["clause_type"],
                        risk_level=s["risk_level"],
                        issues=s["issues"],
                        explanation=s["explanation"],
                        suggested_edit=s.get("suggested_edit"),
                    )
                else:
                    action = ContractReviewAction(clause_type="wrong")
                obs = env.step(action)
            assert obs.reward < 1.0, f"{diff}: score is exactly 1.0"
            assert obs.reward > 0.0, f"{diff}: score is exactly 0.0"

    def test_terrible_answers_not_exactly_0(self):
        for diff in ["easy", "medium", "hard"]:
            env = ContractReviewEnvironment()
            obs = env.reset(seed=42, difficulty=diff)
            while not obs.done:
                action = ContractReviewAction(clause_type="wrong", risk_level="wrong")
                obs = env.step(action)
            assert obs.reward > 0.0, f"{diff}: score is exactly 0.0"
            assert obs.reward < 1.0, f"{diff}: score is exactly 1.0"


class TestMultiTurnActions:
    """Test info-gathering actions."""

    def test_ask_context(self):
        env = ContractReviewEnvironment()
        obs = env.reset(seed=42, difficulty="hard")
        action = ContractReviewAction(action_type="ask_context")
        obs = env.step(action)
        assert obs.done is False
        assert obs.reward == 0.0
        assert obs.context_info != ""
        assert "Contract Type" in obs.context_info

    def test_check_jurisdiction(self):
        env = ContractReviewEnvironment()
        obs = env.reset(seed=42, difficulty="hard")
        action = ContractReviewAction(action_type="check_jurisdiction")
        obs = env.step(action)
        assert obs.done is False
        assert obs.reward == 0.0
        assert obs.context_info != ""
        assert "Jurisdiction" in obs.context_info

    def test_view_full_contract(self):
        env = ContractReviewEnvironment()
        obs = env.reset(seed=42, difficulty="hard")
        action = ContractReviewAction(action_type="view_full_contract")
        obs = env.step(action)
        assert obs.done is False
        assert obs.reward == 0.0
        assert obs.context_info != ""

    def test_info_then_submit(self):
        """Info gathering followed by review should work."""
        env = ContractReviewEnvironment()
        obs = env.reset(seed=42, difficulty="hard")
        # Gather info
        obs = env.step(ContractReviewAction(action_type="ask_context"))
        assert obs.done is False
        # Submit review
        obs = env.step(ContractReviewAction(
            action_type="submit_review",
            clause_type="confidentiality",
            risk_level="medium",
            issues=["missing exclusion"],
            explanation="Missing prior knowledge exclusion.",
        ))
        assert obs.reward > 0.0
        assert env.state.step_count == 2

    def test_clause_text_preserved_during_info_gathering(self):
        """Clause text should remain the same during info gathering."""
        env = ContractReviewEnvironment()
        obs = env.reset(seed=42, difficulty="hard")
        original_clause = obs.clause_text
        original_id = obs.clause_id

        obs = env.step(ContractReviewAction(action_type="ask_context"))
        assert obs.clause_text == original_clause
        assert obs.clause_id == original_id


class TestStepWithoutReset:
    """Test guard against step() without reset()."""

    def test_step_without_reset_returns_error(self):
        env = ContractReviewEnvironment()
        obs = env.step(ContractReviewAction(clause_type="test"))
        assert obs.done is True
        assert obs.reward == 0.0
        assert "Error" in obs.feedback


class TestAllScenariosPlayable:
    """Test that all 55 scenarios can be played through."""

    def test_all_difficulties_complete(self):
        for diff in ["easy", "medium", "hard"]:
            for seed in [1, 42, 100, 999]:
                env = ContractReviewEnvironment()
                obs = env.reset(seed=seed, difficulty=diff)
                steps = 0
                while not obs.done and steps < 20:
                    action = ContractReviewAction(
                        action_type="submit_review",
                        clause_type="indemnification",
                    )
                    obs = env.step(action)
                    steps += 1
                assert obs.done is True, f"{diff} seed={seed} did not complete"
                assert obs.reward > 0.0
                assert obs.reward < 1.0
