import sys
import os
import pytest

# Ensure the parent package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from graders import (
    grade_classification,
    grade_risk_assessment,
    grade_issues,
    grade_explanation,
    grade_suggested_edit,
    grade_task_easy,
    grade_task_medium,
    grade_task_hard,
)
from scenarios import SCENARIOS


class TestClassification:
    def test_exact_match(self):
        assert grade_classification("indemnification", "indemnification") == 1.0

    def test_related_category_partial_credit(self):
        assert grade_classification("indemnification", "limitation_of_liability") == 0.3

    def test_wrong_category(self):
        assert grade_classification("termination", "confidentiality") == 0.0

    def test_case_insensitive(self):
        assert grade_classification("INDEMNIFICATION", "indemnification") == 1.0


class TestRiskAssessment:
    def test_exact_match(self):
        assert grade_risk_assessment("high", "high") == 1.0

    def test_off_by_one(self):
        assert grade_risk_assessment("medium", "high") == 0.4

    def test_off_by_two(self):
        assert grade_risk_assessment("low", "high") == 0.0


class TestIssues:
    def test_no_issues_correct(self):
        assert grade_issues([], []) == 1.0

    def test_no_issues_but_hallucinated(self):
        score = grade_issues(["fake_issue"], [])
        assert score < 1.0

    def test_all_found(self):
        truth = ["unilateral_indemnification", "unlimited_scope"]
        action = ["unilateral_indemnification", "unlimited_scope"]
        assert grade_issues(action, truth) > 0.8

    def test_partial_found(self):
        truth = ["unilateral_indemnification", "unlimited_scope", "no_cap"]
        action = ["unilateral_indemnification"]
        score = grade_issues(action, truth)
        assert 0.2 < score < 1.0  # partial credit, less than perfect


class TestExplanation:
    def test_empty_explanation(self):
        assert grade_explanation("", "some explanation", []) == 0.0

    def test_good_explanation(self):
        gt = "One-sided indemnification shifting all risk to contractor"
        action = (
            "This clause is one-sided, shifting disproportionate risk to "
            "the contractor through the indemnification terms"
        )
        score = grade_explanation(action, gt, ["unilateral"])
        assert score > 0.3


class TestSuggestedEdit:
    def test_no_edit_needed_none_given(self):
        assert grade_suggested_edit(None, None, []) == 1.0

    def test_edit_needed_but_missing(self):
        assert grade_suggested_edit(None, "revised text", ["issue1"]) == 0.0


class TestEndToEnd:
    def test_perfect_easy_scores_1(self):
        for s in SCENARIOS:
            if s["difficulty"] != "easy":
                continue
            result = grade_task_easy({"clause_type": s["clause_type"]}, s)
            assert result["score"] == 1.0, f"Perfect answer for {s['id']} should score 1.0"

    def test_wrong_easy_scores_low(self):
        result = grade_task_easy({"clause_type": "wrong_type"}, SCENARIOS[0])
        assert result["score"] < 0.5

    def test_all_scenarios_gradeable(self):
        for s in SCENARIOS:
            perfect = {
                "clause_type": s["clause_type"],
                "risk_level": s["risk_level"],
                "issues": s["issues"],
                "explanation": s["explanation"],
                "suggested_edit": s.get("suggested_edit"),
            }
            if s["difficulty"] == "easy":
                r = grade_task_easy(perfect, s)
            elif s["difficulty"] == "medium":
                r = grade_task_medium(perfect, s)
            else:
                r = grade_task_hard(perfect, s)
            assert r["score"] > 0, f"{s['id']} should score > 0 with perfect answers"
