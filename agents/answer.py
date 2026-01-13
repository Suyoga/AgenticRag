from strategy import *
from evaluation.valuate import *
from repair import *
from typing import Tuple

def generate_answer(question: str, answer_strategy: AnswerStrategy, retrieved_documents: List[str], llm) -> str:
    """
    Generate the answer based on the strategy and retrieved documents.
    
    Args:
        question: The question to be answered.
        answer_strategy: The strategy that defines the structure and depth of the answer.
        retrieved_documents: The documents retrieved based on the strategy.
        llm: The language model to generate the answer.

    Returns:
        str: The generated answer.
    """
    # Construct the prompt based on the strategy
    if answer_strategy.strategy == "proof_style_reasoning":
        prompt = f"""
        Question: {question}
        Task: Provide a formal proof, exam ready explanations.
        - Include mathematical reasoning if applicable
        - Be precise and concise
        - Don't include anything not required
        """
    elif answer_strategy.strategy == "multi_step_explanation":
        prompt = f"""
        Question: {question}
        Task: Provide a structured, exam ready explanation.
        - Include mathematical reasoning if applicable
        - Answer as much as required for the question
        - Don't include anything not required
        """
    elif answer_strategy.strategy == "verification":
        prompt = f"""
        Question: {question}
        Task: Provide just the final, correct answer 
        """

    # Add the retrieved documents to the prompt for context
    retrieved_context = "\n".join(
        doc["text"] for doc in retrieved_documents
    )
    full_prompt = prompt + "\n\nContext:\n" + retrieved_context

    # Call the LLM to generate the answer based on the prompt
    response = llm.invoke([
        {"role": "system", "content": "You are a helpful and a knowledgable subject assistant who will help me solve the questions from question paper."},
        {"role": "user", "content": full_prompt}
    ])

    # Return the final answer
    return response.content.strip()



def answer_with_verification_and_repair(
    question: str,
    answer: str,
    strategy: AnswerStrategy,
    retrieved_documents: list[dict],
    llm
) -> Tuple[str, VerificationResult]:
    """
    Verifies an answer and performs a single targeted repair if verification fails.

    Args:
        question: The original question.
        answer: The initially generated answer.
        strategy: The selected answer strategy.
        retrieved_documents: Documents used for grounding.
        llm: Language model instance.

    Returns:
        Tuple of (final_answer, verification_result)
    """

    verification = verify_answer(
        question=question,
        answer=answer,
        answer_strategy=strategy,
        retrieved_documents=retrieved_documents,
        llm=llm
    )

    if verification.is_valid:
        return answer, verification

    repair_prompt = build_repair_prompt(
        question=question,
        original_answer=answer,
        verifier_issues=verification.issues,
        retrieved_documents=retrieved_documents,
        answer_strategy=strategy
    )

    response = llm.invoke([
        {"role": "system", "content": "You are a careful academic reviser."},
        {"role": "user", "content": repair_prompt}
    ])

    repaired_answer = response.content.strip()

    verification = verify_answer(
        question=question,
        answer=repaired_answer,
        answer_strategy=strategy,
        retrieved_documents=retrieved_documents,
        llm=llm
    )

    if verification.is_valid:
        return repaired_answer, verification

    return repaired_answer, verification

