import sys
import os
import pytest

# Ensure the parent package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from server.contract_review_environment import ContractReviewEnvironment
from models import ContractReviewAction


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
        assert obs.reward >= 0.0
        assert obs.reward <= 1.0

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
