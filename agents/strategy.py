from pydantic import BaseModel
from typing import List, Literal

class AnswerStrategy(BaseModel):
    strategy: Literal[
        "proof_style_reasoning",
        "multi_step_explanation",
        "verification"
    ]
    expected_sections: List[str]
    retrieval_depth: Literal["low", "medium", "high"]


def rule_based_strategy(section_title: str) -> AnswerStrategy | None:
    """
    Returns the strategy needed to answer the question
    
    :param section_title: Section if the question
    :type section_title: str
    :return: Description
    :rtype: AnswerStrategy | None
    """
    if section_title == "Questions Requiring Small Proofs":
        return AnswerStrategy(
            strategy="proof_style_reasoning",
            expected_sections=["proof_steps"],
            retrieval_depth="medium"
        )

    if section_title == "Questions Requiring Extended Explanations":
        return AnswerStrategy(
            strategy="multi_step_explanation",
            expected_sections=["detailed_explanation"],
            retrieval_depth="high"
        )

    if section_title == "True/False and Multiple Choice":
        return AnswerStrategy(
            strategy="verification",
            expected_sections=["reasoning", "final_answer"],
            retrieval_depth="low"
        )

    return None