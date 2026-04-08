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
    grade_jurisdiction_awareness,
    grade_dependency_awareness,
)
from scenarios import SCENARIOS, CONTRACT_GROUPS, get_contract_group_for_clause


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


class TestJurisdictionAwareness:
    def test_california_noncompete_bonus(self):
        score = grade_jurisdiction_awareness(
            "This non-compete is unenforceable in California where such clauses are banned.",
            None,
            "California, USA",
            "non_compete",
        )
        assert score > 0.0

    def test_no_jurisdiction_awareness(self):
        score = grade_jurisdiction_awareness(
            "This clause has issues.",
            None,
            "California, USA",
            "non_compete",
        )
        assert score == 0.0

    def test_gdpr_awareness(self):
        score = grade_jurisdiction_awareness(
            "Under GDPR Article 28, the data protection regulation requires controller authorization.",
            None,
            "Germany, EU",
            "data_protection",
        )
        assert score > 0.0

    def test_no_matching_jurisdiction(self):
        score = grade_jurisdiction_awareness(
            "GDPR applies here.",
            None,
            "Tokyo, Japan",
            "data_protection",
        )
        assert score == 0.0

    def test_jurisdiction_bonus_in_medium_task(self):
        s = SCENARIOS[10]  # medium scenario
        result_without = grade_task_medium(
            {"clause_type": s["clause_type"], "risk_level": s["risk_level"],
             "issues": s["issues"], "explanation": "Generic explanation.",
             "suggested_edit": None},
            s,
        )
        result_with = grade_task_medium(
            {"clause_type": s["clause_type"], "risk_level": s["risk_level"],
             "issues": s["issues"],
             "explanation": "This indemnification under Texas law requires express negligence doctrine compliance.",
             "suggested_edit": None},
            s,
            jurisdiction="Texas, USA",
        )
        # With jurisdiction awareness should score at least as high
        assert result_with["score"] >= result_without["score"]

    def test_max_bonus_capped(self):
        score = grade_jurisdiction_awareness(
            "banned unenforceable void Business and Professions Code",
            "banned unenforceable void",
            "California, USA",
            "non_compete",
        )
        assert score <= 0.15


class TestDependencyAwareness:
    def test_dependency_bonus_with_keywords(self):
        deps = CONTRACT_GROUPS["contract_A"]["dependencies"]
        score = grade_dependency_awareness(
            "The indemnification clause contradicts the liability cap. These are inconsistent.",
            None,
            deps,
        )
        assert score > 0.0

    def test_no_dependency_awareness(self):
        deps = CONTRACT_GROUPS["contract_A"]["dependencies"]
        score = grade_dependency_awareness(
            "This clause looks fine.",
            None,
            deps,
        )
        assert score == 0.0

    def test_no_dependencies(self):
        score = grade_dependency_awareness(
            "Great explanation.",
            None,
            [],
        )
        assert score == 0.0

    def test_dependency_none(self):
        score = grade_dependency_awareness(
            "Great explanation.",
            None,
            None,
        )
        assert score == 0.0

    def test_contract_group_lookup(self):
        group = get_contract_group_for_clause("clause_011")
        assert group is not None
        assert "clause_011" in group["clauses"]

    def test_no_contract_group(self):
        group = get_contract_group_for_clause("clause_001")
        assert group is None

    def test_max_bonus_capped(self):
        deps = CONTRACT_GROUPS["contract_C"]["dependencies"]
        score = grade_dependency_awareness(
            "The carveout override makes the indemnification cap meaningless. "
            "The termination penalty exceeds the liability cap. "
            "These clauses swallow each other.",
            "Align all caps and remove contradictory carveouts.",
            deps,
        )
        assert score <= 0.15
