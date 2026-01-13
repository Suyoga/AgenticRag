from openai import OpenAI

def query_embedding(question: str) -> List[float]:
    """
    Generate an embedding for the given question using an embedding model.
    
    Args:
        question: The question to embed.
    
    Returns:
        List of floats representing the query embedding.
    """
    response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=question
    )

    embedding = response.data[0].embedding
    return embedding