def retrieve_documents(query_embedding: List[float], top_k: int) -> List[str]:
    """
    Retrieve documents based on the query embedding using the vector database.
    
    Args:
        query_embedding: The query embedding vector.
        top_k: Number of nearest neighbors to return.
    
    Returns:
        List of retrieved document texts.
    """
    results = collection.query(
        query_embeddings=[query_embedding],  
        n_results=top_k,
        include=['documents', 'metadatas']
    )


    retrieved_docs = [
        {"text": doc, "metadata": meta}
        for doc, meta in zip(
            results["documents"][0],
            results["metadatas"][0]
        )
    ]
    return retrieved_docs