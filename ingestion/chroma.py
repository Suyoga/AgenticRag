from pathlib import Path
from course_ingest import *
import os
import chromadb 
from chromadb.config import Settings
from openai import OpenAI

def get_embedding(text: str) -> list:
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",  
        input=text
    )
    return response.data[0].embedding

if __name__ == "__main__":

    CHROMA_DIR = os.environ.get("CHROMA_DIR", "../chroma_data")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    all_chunks = generate_chunks()

    ids = [f"chunk_{i}" for i in range(len(all_chunks))]
    documents = [chunk["text"] for chunk in all_chunks]

    metadatas = [
        {
            "title": chunk["title"],
            "page_start": chunk["page_range"][0],
            "page_end": chunk["page_range"][1],
            "document": str(chunk["document"])  
        }
        for chunk in all_chunks
    ]

    embeddings = [get_embedding(doc) for doc in documents]

    collection = client.get_or_create_collection(name="pdf_chunks")
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )