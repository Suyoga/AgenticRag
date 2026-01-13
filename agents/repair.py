from strategy import AnswerStrategy
from evaluation.valuate import *
from answer import *

def build_repair_prompt(
    question: str,
    original_answer: str,
    verifier_issues: list[str],
    retrieved_documents: list[dict],
    answer_strategy: AnswerStrategy
) -> str:
    issues_text = "\n".join(f"- {issue}" for issue in verifier_issues)
    context = "\n".join(doc["text"] for doc in retrieved_documents)

    return f"""
    You are revising an academic answer based on evaluator feedback.

    Question:
    {question}

    Original Answer:
    {original_answer}

    Evaluator Feedback:
    {issues_text}

    Reference Material:
    {context}

    Instructions:
    - Fix ONLY the issues mentioned above.
    - Do NOT introduce new claims.
    - Preserve correct parts of the original answer.
    - Follow the expected answer style: {answer_strategy.strategy}

    Return ONLY the revised answer.
    """

def generate_with_verification(
    question: str,
    strategy: AnswerStrategy,
    retrieved_documents: list[dict],
    llm,
    max_retries: int = 1
):
    answer = generate_answer(
        question, strategy, retrieved_documents, llm
    )

    verification = verify_answer(
        question, answer, strategy, retrieved_documents, llm
    )

    retries = 0

    while not verification.is_valid and retries < max_retries:
        repair_prompt = build_repair_prompt(
            question,
            answer,
            verification.issues,
            retrieved_documents,
            strategy
        )

        response = llm.invoke([
            {"role": "system", "content": "You are a careful academic reviser."},
            {"role": "user", "content": repair_prompt}
        ])

        answer = response.content.strip()

        verification = verify_answer(
            question, answer, strategy, retrieved_documents, llm
        )

        retries += 1

    return answer, verification

