from pydantic import BaseModel
from typing import List, Optional
from agents.strategy import AnswerStrategy
from openai import OpenAI
from langchain_openai import ChatOpenAI

class VerificationResult(BaseModel):
    is_valid: bool
    coverage_score: float
    issues: List[str]
    suggested_fix: Optional[str] = None


def rule_based_verification(answer: str, answer_strategy: AnswerStrategy) -> List[str]:
    """
    Checks if the generated answer has any of the following issues:
    -Empty
    -Too short
    -No proof
    -Final answer missing
    """
    issues = []

    if not answer or len(answer.strip()) == 0:
        issues.append("Answer is empty.")

    if answer_strategy.strategy == "multi_step_explanation":
        if len(answer.split()) < 150:
            issues.append("Answer may be too short for a long explanation.")

    if answer_strategy.strategy == "proof_style_reasoning":
        keywords = ["therefore", "hence", "implies", "assume"]
        if not any(k in answer.lower() for k in keywords):
            issues.append("Proof-style answer lacks formal reasoning steps.")

    if answer_strategy.strategy == "verification":
        if not any(k in answer.lower() for k in ["true", "false"]):
            issues.append("Verification answer does not clearly state True or False.")

    return issues

def llm_based_verification(
    question: str,
    answer: str,
    retrieved_documents: List[dict],
    answer_strategy: AnswerStrategy,
    llm
) -> List[str]:
    context = "\n".join(doc["text"] for doc in retrieved_documents)

    verification_prompt = f"""
    You are an exam evaluator.

    Question:
    {question}

    Student Answer:
    {answer}

    Reference Material:
    {context}

    Expected Sections:
    {answer_strategy.expected_sections}

    Tasks:
    1. Check if the answer fully addresses the question.
    2. Identify unsupported or hallucinated claims.
    3. Identify missing reasoning or explanation.

    STRICT OUTPUT RULES:
    - If there are ANY issues, output ONLY bullet points describing the issues.
    - If there are NO issues, output EXACTLY the single token:
    NO_ISSUES
    - Do NOT include explanations, confirmations, or summaries.
    - Do NOT mix NO_ISSUES with other text.

    """

    response = llm.invoke([
        {"role": "system", "content": "You are a strict academic evaluator."},
        {"role": "user", "content": verification_prompt}
    ])

    content = response.content.strip()

    # Normalize
    normalized = content.replace("-", "").strip().upper()
    
    # If NO_ISSUES appears anywhere, trust it
    if "NO_ISSUES" in normalized:
        return []
    
    issues = []
    for line in content.splitlines():
        line = line.strip().lstrip("-").strip()
        if line and "NO_ISSUES" not in line.upper():
            issues.append(line)
    
    return issues


def verify_answer(
    question: str,
    answer: str,
    answer_strategy: AnswerStrategy,
    retrieved_documents: List[dict],
    llm
) -> VerificationResult:
    issues = []

    # 1. Rule-based verification
    issues.extend(rule_based_verification(answer, answer_strategy))

    # 2. LLM-based verification
    issues.extend(
        llm_based_verification(
            question,
            answer,
            retrieved_documents,
            answer_strategy,
            llm
        )
    )

    coverage_score = max(0.0, 1.0 - 0.15 * len(issues))

    return VerificationResult(
        is_valid=len(issues) == 0,
        coverage_score=round(coverage_score, 2),
        issues=issues,
        suggested_fix=None if not issues else "Revise the answer addressing the listed issues."
    )