# Copyright (c) 2024. All rights reserved.
# Grading logic for Contract Review tasks.

from difflib import SequenceMatcher
from typing import Any, Dict, List, Set


def _normalize(text: str) -> str:
    """Normalize text for comparison."""
    return text.strip().lower().replace("_", " ").replace("-", " ")


def _tfidf_similarity(text_a: str, text_b: str) -> float:
    """Compute TF-IDF cosine similarity between two texts."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
        return float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
    except ImportError:
        return _keyword_overlap(text_a, text_b)


def _keyword_overlap(text_a: str, text_b: str) -> float:
    """Compute keyword overlap ratio between two texts."""
    if not text_a or not text_b:
        return 0.0
    words_a = set(_normalize(text_a).split())
    words_b = set(_normalize(text_b).split())
    # Remove common stopwords
    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "shall",
        "should", "may", "might", "must", "can", "could", "to", "of", "in",
        "for", "on", "with", "at", "by", "from", "as", "into", "through",
        "during", "before", "after", "and", "but", "or", "nor", "not", "no",
        "so", "if", "than", "that", "this", "it", "its", "any", "all", "each",
        "such", "other", "which", "who", "whom",
    }
    words_a -= stopwords
    words_b -= stopwords
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    return len(intersection) / max(len(words_a), len(words_b))


def _text_similarity(text_a: str, text_b: str) -> float:
    """Compute text similarity using SequenceMatcher."""
    if not text_a or not text_b:
        return 0.0
    return SequenceMatcher(None, _normalize(text_a), _normalize(text_b)).ratio()


def grade_classification(
    action_type: str,
    ground_truth_type: str,
) -> float:
    """Grade clause type classification (0.0 - 1.0)."""
    if _normalize(action_type) == _normalize(ground_truth_type):
        return 1.0
    # Partial credit for related types
    related_groups = [
        {"indemnification", "limitation of liability", "warranty"},
        {"termination", "force majeure"},
        {"confidentiality", "data protection"},
        {"non compete", "ip assignment"},
    ]
    norm_action = _normalize(action_type)
    norm_truth = _normalize(ground_truth_type)
    for group in related_groups:
        if norm_action in group and norm_truth in group:
            return 0.3
    return 0.0


def grade_risk_assessment(
    action_risk: str,
    ground_truth_risk: str,
) -> float:
    """Grade risk level assessment (0.0 - 1.0)."""
    levels = {"low": 0, "medium": 1, "high": 2}
    action_level = levels.get(_normalize(action_risk), -1)
    truth_level = levels.get(_normalize(ground_truth_risk), -1)
    if action_level == -1:
        return 0.0
    if action_level == truth_level:
        return 1.0
    diff = abs(action_level - truth_level)
    if diff == 1:
        return 0.4
    return 0.0


def grade_issues(
    action_issues: List[str],
    ground_truth_issues: List[str],
) -> float:
    """Grade identified issues (0.0 - 1.0).

    Uses fuzzy matching to allow for different phrasings.
    """
    if not ground_truth_issues:
        # No issues to find — reward for not hallucinating issues
        if not action_issues:
            return 1.0
        return max(0.0, 1.0 - len(action_issues) * 0.2)

    if not action_issues:
        return 0.0

    norm_truth: List[str] = [_normalize(i) for i in ground_truth_issues]
    norm_action: List[str] = [_normalize(i) for i in action_issues]

    # For each ground truth issue, find best matching action issue
    matched = 0
    for truth_issue in norm_truth:
        best_score = 0.0
        for action_issue in norm_action:
            # Check keyword overlap and text similarity
            kw_score = _keyword_overlap(truth_issue, action_issue)
            sim_score = _text_similarity(truth_issue, action_issue)
            score = max(kw_score, sim_score)
            best_score = max(best_score, score)
        if best_score >= 0.3:
            matched += 1

    recall = matched / len(norm_truth)

    # Penalize excessive false positives
    false_positive_penalty = max(0, len(action_issues) - len(ground_truth_issues) - 1) * 0.1

    base_score = max(0.0, min(1.0, recall - false_positive_penalty))

    # Issue specificity bonus: reward detailed descriptions (>3 words each)
    if norm_action:
        specific_count = sum(1 for issue in norm_action if len(issue.split()) > 3)
        specificity_ratio = specific_count / len(norm_action)
        specificity_bonus = specificity_ratio * 0.1
        base_score = min(1.0, base_score + specificity_bonus)

    return base_score


def grade_explanation(
    action_explanation: str,
    ground_truth_explanation: str,
    ground_truth_issues: List[str],
) -> float:
    """Grade the quality of the explanation (0.0 - 1.0).

    Checks for:
    - Relevance (keyword overlap with ground truth)
    - Substantiveness (length)
    - Coverage of key issues
    """
    if not action_explanation:
        return 0.0

    score = 0.0

    # Relevance: similarity to ground truth explanation (TF-IDF with keyword fallback)
    relevance = _tfidf_similarity(action_explanation, ground_truth_explanation)
    score += relevance * 0.5

    # Substantiveness: reasonable length
    word_count = len(action_explanation.split())
    if word_count >= 20:
        score += 0.2
    elif word_count >= 10:
        score += 0.1

    # Coverage: mentions key issue terms
    if ground_truth_issues:
        issues_mentioned = 0
        for issue in ground_truth_issues:
            issue_words = set(_normalize(issue).split())
            explanation_words = set(_normalize(action_explanation).split())
            if issue_words & explanation_words:
                issues_mentioned += 1
        coverage = issues_mentioned / len(ground_truth_issues)
        score += coverage * 0.3

    return min(1.0, score)


def grade_suggested_edit(
    action_edit: str | None,
    ground_truth_edit: str | None,
    ground_truth_issues: List[str],
) -> float:
    """Grade the suggested edit (0.0 - 1.0).

    Checks for:
    - Presence of edit when issues exist
    - Similarity to ground truth edit
    - Whether it addresses the identified issues
    """
    if not ground_truth_issues or ground_truth_edit is None:
        # No issues, no edit needed
        if action_edit is None or action_edit.strip() == "":
            return 1.0
        return 0.7  # Minor penalty for unnecessary edit

    if not action_edit or action_edit.strip() == "":
        return 0.0

    score = 0.0

    # Similarity to ground truth edit (TF-IDF with keyword fallback)
    similarity = _tfidf_similarity(action_edit, ground_truth_edit)
    score += similarity * 0.5

    # Text similarity (captures structural changes)
    text_sim = _text_similarity(action_edit, ground_truth_edit)
    score += text_sim * 0.3

    # Addresses issues: check if edit contains issue-related keywords
    if ground_truth_issues:
        issues_addressed = 0
        for issue in ground_truth_issues:
            issue_words = set(_normalize(issue).split())
            edit_words = set(_normalize(action_edit).split())
            if issue_words & edit_words:
                issues_addressed += 1
        coverage = issues_addressed / len(ground_truth_issues)
        score += coverage * 0.2

    return min(1.0, score)


JURISDICTION_RULES = {
    ("non_compete", "california"): ["unenforceable", "banned", "void", "business and professions code"],
    ("non_compete", "new york"): ["reasonable", "geographic", "temporal"],
    ("data_protection", "eu"): ["gdpr", "data protection regulation", "article 28"],
    ("data_protection", "uk"): ["uk gdpr", "ico", "data protection act"],
    ("limitation_of_liability", "eu"): ["consumer", "personal injury", "cannot exclude"],
    ("indemnification", "texas"): ["express negligence", "conspicuous"],
    ("confidentiality", "california"): ["trade secret", "utsa", "defend trade secrets act"],
    ("termination", "france"): ["notice period", "indemnité", "code du travail"],
}


def grade_jurisdiction_awareness(
    action_explanation: str,
    action_edit: str | None,
    jurisdiction: str,
    clause_type: str,
) -> float:
    """Grade jurisdiction-specific awareness (bonus 0.0 - 0.15).

    Checks if the agent's explanation or edit references jurisdiction-specific
    considerations relevant to the clause type.
    """
    if not jurisdiction or not clause_type:
        return 0.0

    combined_text = _normalize(action_explanation or "")
    if action_edit:
        combined_text += " " + _normalize(action_edit)

    if not combined_text.strip():
        return 0.0

    norm_clause = _normalize(clause_type)
    norm_jurisdiction = jurisdiction.lower()

    total_bonus = 0.0
    matched_any_rule = False

    for (rule_clause, rule_jurisdiction), keywords in JURISDICTION_RULES.items():
        if norm_clause != _normalize(rule_clause):
            continue
        if rule_jurisdiction not in norm_jurisdiction:
            continue
        matched_any_rule = True
        matched_keywords = sum(1 for kw in keywords if kw in combined_text)
        if matched_keywords > 0:
            total_bonus = (matched_keywords / len(keywords)) * 0.15

    if not matched_any_rule:
        return 0.0

    return min(0.15, total_bonus)


def grade_dependency_awareness(
    action_explanation: str,
    action_edit: str | None,
    dependencies: list,
) -> float:
    """Grade cross-clause dependency awareness (bonus 0.0 - 0.15).

    Checks if the agent's explanation or suggested edit mentions keywords
    related to the cross-clause dependencies defined in CONTRACT_GROUPS.
    Each dependency contributes equally to the bonus.
    """
    if not dependencies:
        return 0.0

    combined_text = _normalize(action_explanation or "")
    if action_edit:
        combined_text += " " + _normalize(action_edit)

    if not combined_text.strip():
        return 0.0

    per_dep_weight = 0.15 / len(dependencies)
    total_bonus = 0.0

    for dep in dependencies:
        keywords = dep.get("keywords", [])
        if not keywords:
            continue
        matched = sum(1 for kw in keywords if kw.lower() in combined_text)
        if matched > 0:
            ratio = min(1.0, matched / len(keywords))
            total_bonus += ratio * per_dep_weight

    return min(0.15, total_bonus)


def grade_task_easy(
    action: Dict[str, Any],
    ground_truth: Dict[str, Any],
) -> Dict[str, float]:
    """Grade easy task: classification only.

    Returns dict with component scores and final score.
    """
    classification_score = grade_classification(
        action.get("clause_type", ""),
        ground_truth["clause_type"],
    )
    return {
        "classification": classification_score,
        "score": classification_score,
    }


def grade_task_medium(
    action: Dict[str, Any],
    ground_truth: Dict[str, Any],
    jurisdiction: str | None = None,
) -> Dict[str, float]:
    """Grade medium task: classification + risk + issues.

    Weights: classification=0.25, risk=0.30, issues=0.25, explanation=0.20
    Plus optional jurisdiction awareness bonus (0.0 - 0.15).
    """
    classification_score = grade_classification(
        action.get("clause_type", ""),
        ground_truth["clause_type"],
    )
    risk_score = grade_risk_assessment(
        action.get("risk_level", ""),
        ground_truth["risk_level"],
    )
    issues_score = grade_issues(
        action.get("issues", []),
        ground_truth["issues"],
    )
    explanation_score = grade_explanation(
        action.get("explanation", ""),
        ground_truth["explanation"],
        ground_truth["issues"],
    )

    final = (
        classification_score * 0.25
        + risk_score * 0.30
        + issues_score * 0.25
        + explanation_score * 0.20
    )

    jurisdiction_bonus = 0.0
    if jurisdiction:
        jurisdiction_bonus = grade_jurisdiction_awareness(
            action.get("explanation", ""),
            action.get("suggested_edit"),
            jurisdiction,
            ground_truth["clause_type"],
        )
        final = min(0.99, final + jurisdiction_bonus)

    return {
        "classification": classification_score,
        "risk": risk_score,
        "issues": issues_score,
        "explanation": explanation_score,
        "jurisdiction_bonus": jurisdiction_bonus,
        "score": final,
    }


def grade_task_hard(
    action: Dict[str, Any],
    ground_truth: Dict[str, Any],
    jurisdiction: str | None = None,
    dependencies: list | None = None,
) -> Dict[str, float]:
    """Grade hard task: full review with suggested edit.

    Weights: classification=0.15, risk=0.20, issues=0.20,
             explanation=0.15, suggested_edit=0.30
    Plus optional jurisdiction awareness bonus (0.0 - 0.15).
    Plus optional dependency awareness bonus (0.0 - 0.15).
    """
    classification_score = grade_classification(
        action.get("clause_type", ""),
        ground_truth["clause_type"],
    )
    risk_score = grade_risk_assessment(
        action.get("risk_level", ""),
        ground_truth["risk_level"],
    )
    issues_score = grade_issues(
        action.get("issues", []),
        ground_truth["issues"],
    )
    explanation_score = grade_explanation(
        action.get("explanation", ""),
        ground_truth["explanation"],
        ground_truth["issues"],
    )
    edit_score = grade_suggested_edit(
        action.get("suggested_edit"),
        ground_truth.get("suggested_edit"),
        ground_truth["issues"],
    )

    # Reasoning gate: cap edit score if explanation is weak
    # Can't write a good edit without understanding the problem
    if explanation_score < 0.2:
        edit_score = min(edit_score, 0.5)

    final = (
        classification_score * 0.15
        + risk_score * 0.20
        + issues_score * 0.20
        + explanation_score * 0.15
        + edit_score * 0.30
    )

    jurisdiction_bonus = 0.0
    if jurisdiction:
        jurisdiction_bonus = grade_jurisdiction_awareness(
            action.get("explanation", ""),
            action.get("suggested_edit"),
            jurisdiction,
            ground_truth["clause_type"],
        )
        final = min(0.99, final + jurisdiction_bonus)

    dependency_bonus = 0.0
    if dependencies:
        dependency_bonus = grade_dependency_awareness(
            action.get("explanation", ""),
            action.get("suggested_edit"),
            dependencies,
        )
        final = min(0.99, final + dependency_bonus)

    return {
        "classification": classification_score,
        "risk": risk_score,
        "issues": issues_score,
        "explanation": explanation_score,
        "suggested_edit": edit_score,
        "jurisdiction_bonus": jurisdiction_bonus,
        "dependency_bonus": dependency_bonus,
        "score": final,
    }
