from retrieve import retrieve_documents
from agents.answer import AnswerStrategy
from typing import List

def controlled_retrieval(answer_strategy: AnswerStrategy, query_embedding: List[float]) -> List[str]:
    """
    Retrieve documents based on the specified strategy (retrieval depth).
    
    Args:
        answer_strategy: The strategy that determines the retrieval depth.
    
    Returns:
        List of retrieved document texts.
    """
    if answer_strategy.retrieval_depth == "high":
        top_k = 12  # Retrieve more documents for extended explanations
    elif answer_strategy.retrieval_depth == "medium":
        top_k = 6   # Retrieve fewer documents for smaller proofs or extended explanations
    else:
        top_k = 3   # Retrieve very few for True/False or MCQs
    
    # Perform the retrieval (assuming you have a retrieval function here)
    # `collection.query` or equivalent based on your vector database
    documents = retrieve_documents(query_embedding=query_embedding, top_k=top_k)  
    return documents
