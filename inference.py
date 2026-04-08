"""
Inference Script for Contract Review Environment
===================================
MANDATORY
- Before submitting, ensure the following variables are defined in your environment configuration:
    API_BASE_URL   The API endpoint for the LLM.
    MODEL_NAME     The model identifier to use for inference.
    HF_TOKEN       Your Hugging Face / API key.
    LOCAL_IMAGE_NAME The name of the local image to use for the environment if you are using from_docker_image()

- Defaults are set only for API_BASE_URL and MODEL_NAME
    API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

- The inference script must be named `inference.py` and placed in the root directory of the project
- Participants must use OpenAI Client for all LLM calls using above variables

STDOUT FORMAT
- The script must emit exactly three line types to stdout, in this order:

    [START] task=<task_name> env=<benchmark> model=<model_name>
    [STEP]  step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
    [END]   success=<true|false> steps=<n> score=<score> rewards=<r1,r2,...,rn>

  Rules:
    - One [START] line at episode begin.
    - One [STEP] line per step, immediately after env.step() returns.
    - One [END] line after env.close(), always emitted (even on exception).
    - reward and rewards are formatted to 2 decimal places.
    - done and success are lowercase booleans: true or false.
    - error is the raw last_action_error string, or null if none.
    - Each task should return score in [0, 1]
"""

import asyncio
import json
import os
import textwrap
from typing import Any, Dict, List, Optional

from openai import OpenAI

from models import ContractReviewAction, ContractReviewObservation
from client import ContractReviewEnv

IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME") or os.getenv("IMAGE_NAME")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
BENCHMARK = "contract_review_env"
TEMPERATURE = 0.3
MAX_TOKENS = 1024


SYSTEM_PROMPTS = {
    "easy": textwrap.dedent("""\
        You are a legal contract analyst. You will be shown a contract clause.
        Your job is to classify the clause type.

        Valid clause types: indemnification, limitation_of_liability, termination,
        confidentiality, ip_assignment, non_compete, payment_terms, governing_law,
        force_majeure, warranty, data_protection, dispute_resolution.

        Respond with ONLY a JSON object (no markdown, no explanation):
        {"clause_type": "<type>", "risk_level": "low", "issues": [], "explanation": "", "suggested_edit": null}
    """),
    "medium": textwrap.dedent("""\
        You are a senior legal contract analyst. You will be shown a contract clause.
        Your job is to:
        1. Classify the clause type
        2. Assess the risk level (low, medium, or high)
        3. Identify specific issues or red flags
        4. Explain your assessment

        Valid clause types: indemnification, limitation_of_liability, termination,
        confidentiality, ip_assignment, non_compete, payment_terms, governing_law,
        force_majeure, warranty, data_protection, dispute_resolution.

        Risk levels: low (standard/balanced terms), medium (some concerning elements),
        high (significantly unfavorable or potentially unenforceable terms).

        Respond with ONLY a JSON object (no markdown, no explanation outside the JSON):
        {
            "clause_type": "<type>",
            "risk_level": "<low|medium|high>",
            "issues": ["<issue1>", "<issue2>"],
            "explanation": "<your analysis>",
            "suggested_edit": null
        }
    """),
    "hard": textwrap.dedent("""\
        You are a senior legal contract review attorney. You will be shown a contract clause.
        Your job is to perform a complete review:
        1. Classify the clause type
        2. Assess the risk level (low, medium, or high)
        3. Identify ALL specific issues or red flags
        4. Explain the risks and their legal implications
        5. Provide a revised version of the clause that addresses the identified issues

        Valid clause types: indemnification, limitation_of_liability, termination,
        confidentiality, ip_assignment, non_compete, payment_terms, governing_law,
        force_majeure, warranty, data_protection, dispute_resolution.

        Risk levels: low (standard/balanced terms), medium (some concerning elements),
        high (significantly unfavorable or potentially unenforceable terms).

        For the suggested_edit: rewrite the clause to fix the identified issues while
        maintaining the original intent. Make it balanced and enforceable.

        Respond with ONLY a JSON object (no markdown, no explanation outside the JSON):
        {
            "clause_type": "<type>",
            "risk_level": "<low|medium|high>",
            "issues": ["<issue1>", "<issue2>"],
            "explanation": "<detailed legal analysis>",
            "suggested_edit": "<revised clause text>"
        }
    """),
}


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    # Truncate action for logging
    action_short = action[:80].replace("\n", " ") if action else ""
    print(
        f"[STEP] step={step} action={action_short} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


def parse_llm_response(text: str) -> Dict[str, Any]:
    """Parse the LLM's JSON response, handling common formatting issues."""
    text = text.strip()
    # Remove markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from the text
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
    # Fallback
    return {
        "clause_type": "indemnification",
        "risk_level": "low",
        "issues": [],
        "explanation": "",
        "suggested_edit": None,
    }


def get_model_response(
    client: OpenAI,
    system_prompt: str,
    clause_text: str,
    feedback: str = "",
) -> Dict[str, Any]:
    """Call the LLM and parse its response."""
    user_content = f"Review this contract clause:\n\n{clause_text}"
    if feedback:
        user_content += f"\n\nFeedback from previous clause: {feedback}"

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        text = (completion.choices[0].message.content or "").strip()
        return parse_llm_response(text)
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return {
            "clause_type": "indemnification",
            "risk_level": "low",
            "issues": [],
            "explanation": "",
            "suggested_edit": None,
        }


async def run_task(difficulty: str) -> float:
    """Run a single task (easy/medium/hard) and return the score."""
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    if IMAGE_NAME:
        env = await ContractReviewEnv.from_docker_image(IMAGE_NAME)
    else:
        env = ContractReviewEnv(base_url=os.getenv("ENV_BASE_URL", "http://localhost:8000"))

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False
    task_name = f"contract-review-{difficulty}"

    log_start(task=task_name, env=BENCHMARK, model=MODEL_NAME)

    try:
        result = await env.reset(difficulty=difficulty, seed=42)
        obs = result.observation
        system_prompt = SYSTEM_PROMPTS[difficulty]
        feedback = ""

        while not result.done:
            # For hard tasks, gather context before first review of each clause
            if difficulty == "hard" and obs.clause_text and not obs.context_info:
                # Ask for contract context first
                context_action = ContractReviewAction(action_type="ask_context")
                result = await env.step(context_action)
                obs = result.observation
                steps_taken += 1
                log_step(
                    step=steps_taken,
                    action="ask_context",
                    reward=0.0,
                    done=result.done,
                    error=None,
                )
                rewards.append(0.0)
                if result.done:
                    break

                # Check jurisdiction
                juris_action = ContractReviewAction(action_type="check_jurisdiction")
                result = await env.step(juris_action)
                obs = result.observation
                steps_taken += 1
                log_step(
                    step=steps_taken,
                    action="check_jurisdiction",
                    reward=0.0,
                    done=result.done,
                    error=None,
                )
                rewards.append(0.0)
                if result.done:
                    break

            # Build enhanced prompt with context if available
            extra_context = ""
            if obs.context_info:
                extra_context = f"\n\nContract context:\n{obs.context_info}"

            # Get LLM's analysis
            parsed = get_model_response(
                client,
                system_prompt,
                obs.clause_text + extra_context,
                feedback,
            )

            # Build action
            action = ContractReviewAction(
                action_type="submit_review",
                clause_type=parsed.get("clause_type", "indemnification"),
                risk_level=parsed.get("risk_level", "low"),
                issues=parsed.get("issues", []),
                explanation=parsed.get("explanation", ""),
                suggested_edit=parsed.get("suggested_edit"),
            )

            # Step
            result = await env.step(action)
            obs = result.observation

            reward = result.reward or 0.0
            done = result.done
            rewards.append(reward)
            steps_taken += 1

            action_summary = f"type={parsed.get('clause_type', '?')},risk={parsed.get('risk_level', '?')}"
            log_step(
                step=steps_taken,
                action=action_summary,
                reward=reward,
                done=done,
                error=None,
            )

            feedback = obs.feedback

        # Final score is the last reward (which is the average for the episode)
        score = rewards[-1] if rewards else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score >= 0.3

    except Exception as e:
        print(f"[DEBUG] Error during {difficulty} task: {e}", flush=True)
    finally:
        try:
            await env.close()
        except Exception as e:
            print(f"[DEBUG] env.close() error: {e}", flush=True)
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

    return score


async def main() -> None:
    """Run all three tasks and report scores."""
    tasks = ["easy", "medium", "hard"]
    scores = {}

    for difficulty in tasks:
        print(f"\n{'='*60}", flush=True)
        print(f"Running {difficulty.upper()} task...", flush=True)
        print(f"{'='*60}", flush=True)
        scores[difficulty] = await run_task(difficulty)

    # Summary
    print(f"\n{'='*60}", flush=True)
    print("SUMMARY", flush=True)
    print(f"{'='*60}", flush=True)
    for difficulty, s in scores.items():
        print(f"  {difficulty:8s}: {s:.3f}", flush=True)
    avg = sum(scores.values()) / len(scores) if scores else 0.0
    print(f"  {'average':8s}: {avg:.3f}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
