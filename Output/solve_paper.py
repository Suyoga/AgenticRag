import json
from agents.strategy import *
from agents.answer import *
from agents.repair import *
from evaluation.valuate import *
from langchain_openai import ChatOpenAI
from retrieval.query import query_embedding
from retrieval.controlled_retrieve import controlled_retrieval



if __name__ == "__main__":

    final_answers = []

    with open("questions.json", "r") as f:
        questions = json.load(f)

    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        openai_api_key=key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.1
    )

    for section_title in questions:
        for q in questions[section_title]["questions"]:
            question = q["question_text"]
            strategy = rule_based_strategy(section_title)

            question_emb = query_embedding(question)
        
            docs = controlled_retrieval(strategy, question_emb)

            initial_answer = generate_answer(question, strategy, docs, llm)

            final_answer, verification = answer_with_verification_and_repair(
                question=question,
                answer=initial_answer,
                strategy=strategy,
                retrieved_documents=docs,
                llm=llm
            )

            final_answers.append({
                "section": section_title,
                "question": question,
                "answer": final_answer,
                "verified": verification.is_valid,
                "issues": verification.issues
            })

    with open("allanswers.json", "w") as f:
        json.dump(final_answers, f)

    with open("allanswers.json", "r") as f:
        answers = json.load(f)

    with open("allanswers.md", "w") as md:
        for idx, item in enumerate(answers, 1):
            md.write(f"# Question {idx}\n\n")
            md.write(f"**Section:** {item.get('section', '')}\n\n")
            md.write(f"**Question:**\n\n{item['question']}\n\n")
            md.write("**Answer:**\n\n")
            md.write(item["answer"])
            md.write("\n\n---\n\n")