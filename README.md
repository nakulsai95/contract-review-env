---
title: Contract Review Environment
emoji: ⚖️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8000
base_path: /web
tags:
  - openenv
---

# Contract Review Environment

An OpenEnv environment where AI agents review legal contract clauses — classifying clause types, assessing risk, identifying red flags, and suggesting edits. Models a task that legal teams perform daily at every company.

## Why This Matters

Contract review is a $30B+ industry. Junior lawyers spend thousands of hours reviewing standard clauses. An AI agent that can accurately triage contract risk would have immediate real-world value — from startup founders reviewing vendor agreements to legal teams processing M&A due diligence.

## Tasks

### Task 1: Clause Classification (Easy)
- **Objective**: Classify the type of a contract clause
- **Clauses per episode**: 5 (up to 10 steps with info-gathering)
- **Grading**: Exact match = 1.0, related category = 0.3, wrong = 0.0
- **Expected baseline**: ~0.60

### Task 2: Risk Assessment (Medium)
- **Objective**: Classify type + assess risk level + identify issues + explain
- **Clauses per episode**: 3 (up to 9 steps with info-gathering)
- **Grading**: Weighted — classification (25%), risk level (30%), issues found (25%), explanation quality (20%) + jurisdiction bonus
- **Expected baseline**: ~0.83

### Task 3: Full Review with Edits (Hard)
- **Objective**: Complete review including suggested clause revisions
- **Clauses per episode**: 2 (up to 8 steps with info-gathering)
- **Grading**: Weighted — classification (15%), risk (20%), issues (20%), explanation (15%), suggested edit quality (30%) + jurisdiction bonus + dependency bonus
- **Reasoning gate**: Edit score is capped if explanation is weak (can't fix what you don't understand)
- **Expected baseline**: ~0.62

## Dataset

55 curated contract clause scenarios across 17 clause types, organized into 4 contract groups:

- **18 Easy**: Standard/safe clauses (indemnification, termination, confidentiality, etc.)
- **18 Medium**: Clauses with clear red flags (unilateral terms, excessive penalties, overbroad scope)
- **19 Hard**: Subtle/adversarial clauses (poison pills, circular cross-references, nested exceptions that nullify protections, contradictory carveouts)

**17 clause types**: `indemnification`, `limitation_of_liability`, `termination`, `confidentiality`, `ip_assignment`, `non_compete`, `payment_terms`, `governing_law`, `force_majeure`, `warranty`, `data_protection`, `dispute_resolution`, `assignment_and_change_of_control`, `representations_and_warranties`, `audit_rights`, `insurance_requirements`, `most_favored_nation`

### Contract Groups (Multi-Clause Dependencies)

Clauses are grouped into realistic contracts where they interact:

| Contract | Clauses | Dependency Type |
|----------|---------|----------------|
| TechCorp MSA | Indemnification + LoL + Termination | Contradiction: unlimited indemnification vs $100 liability cap |
| CloudSoft SaaS | Confidentiality + Data Protection + IP | Overlap: perpetual confidentiality conflicts with data breach disclaimer |
| Enterprise License | LoL + Termination + Indemnification | Interaction: carveouts swallow cap; termination penalty exceeds cap |
| Consulting Agreement | Non-compete + IP Assignment + Warranty | Compounding: worldwide non-compete + all-IP capture prevents contractor from working |

Agents that identify cross-clause contradictions receive a **dependency bonus** (+0.15).

### Jurisdiction-Specific Scoring

The same clause may be scored differently depending on jurisdiction:

| Jurisdiction | Clause Type | What Earns Bonus |
|---|---|---|
| California | Non-compete | Mentioning CA ban, Business and Professions Code |
| EU/Germany | Data Protection | Referencing GDPR, Article 28, DPA |
| Texas | Indemnification | Express negligence doctrine |
| UK | Data Protection | UK GDPR, ICO, Data Protection Act |
| New York | Non-compete | Reasonable geographic/temporal scope |
| France | Termination | Notice period requirements, Code du travail |

Agents that demonstrate jurisdiction awareness receive a **jurisdiction bonus** (+0.15).

## Action Space

```python
class ContractReviewAction(Action):
    action_type: str        # "submit_review", "ask_context", "view_full_contract", "check_jurisdiction"
    clause_type: str        # One of 17 clause types
    risk_level: str         # "low", "medium", or "high"
    issues: List[str]       # List of identified red flags
    explanation: str        # Analysis of risks and implications
    suggested_edit: str     # Revised clause text (hard task)
```

### Multi-Turn Actions

Before submitting a review, the agent can gather information:

| Action | What it returns | Cost |
|--------|----------------|------|
| `ask_context` | Contract type, parties, contract value | 1 step, 0 reward |
| `view_full_contract` | Summary of other clauses + cross-clause dependencies | 1 step, 0 reward |
| `check_jurisdiction` | Applicable jurisdiction and enforceability notes | 1 step, 0 reward |
| `submit_review` | Graded analysis with reward | 1 step, scored |

This models real-world contract review where lawyers check context before analyzing a clause.

## Observation Space

```python
class ContractReviewObservation(Observation):
    clause_text: str              # The contract clause to review
    clause_id: str                # Unique clause identifier
    task_description: str         # Instructions for the current task
    difficulty: str               # "easy", "medium", or "hard"
    feedback: str                 # Grader feedback from previous step
    clauses_remaining: int        # Clauses left in this episode
    context_info: str             # Context from info-gathering actions
    related_clauses_summary: str  # Cross-clause dependency hints
```

## Reward Design

Rewards are computed per-clause and averaged across the episode:

- **Classification**: Exact match (1.0), related category (0.3), wrong (0.0)
- **Risk level**: Exact (1.0), off-by-one (0.4), off-by-two (0.0)
- **Issues**: Fuzzy matching with recall-based scoring, penalty for false positives, bonus for specificity
- **Explanation**: TF-IDF semantic similarity to ground truth + coverage of key issues + substantiveness
- **Suggested edit**: TF-IDF similarity to reference edit + issue coverage + structural quality
- **Reasoning gate**: Edit score capped at 0.5 if explanation score < 0.2
- **Jurisdiction bonus**: +0.15 for mentioning jurisdiction-specific legal rules
- **Dependency bonus**: +0.15 for identifying cross-clause contradictions/interactions

All rewards are clamped to (0.01, 0.99). Partial progress is always rewarded — no sparse binary signals.

## Setup & Usage

### Prerequisites

```bash
pip install openenv-core[core] fastapi uvicorn openai scikit-learn
```

### Run locally

```bash
cd contract_review_env
uvicorn server.app:app --host 0.0.0.0 --port 8000
```

### Run with Docker

```bash
cd contract_review_env/server
docker build -t contract-review-env .
docker run -p 8000:8000 contract-review-env
```

### Run inference

```bash
export HF_TOKEN=your_hf_token
export API_BASE_URL=https://router.huggingface.co/v1
export MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
python inference.py
```

### Run tests

```bash
cd contract_review_env
python -m pytest tests/ -v
```

### Validate

```bash
cd contract_review_env
openenv validate
```

## Baseline Scores

| Task | Difficulty | Model | Score |
|------|-----------|-------|-------|
| Clause Classification | Easy | Qwen2.5-72B-Instruct | 0.600 |
| Risk Assessment | Medium | Qwen2.5-72B-Instruct | 0.834 |
| Full Review | Hard | Qwen2.5-72B-Instruct | 0.620 |
| **Average** | | | **0.685** |

## Scenario Sources

Clause patterns inspired by:
- SEC EDGAR public filings (10-K, 8-K exhibits with vendor/service agreements)
- CUAD (Contract Understanding Atticus Dataset) clause type taxonomy
- Open-source contract templates (Bonterms, CommonPaper, Y Combinator SAFE)
- Published legal scholarship on contract risk analysis

All scenarios are original compositions — no verbatim copies from any source.

## License

BSD-3-Clause
