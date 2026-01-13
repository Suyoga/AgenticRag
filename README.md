Title
Agentic Retrieval-Augmented System for Exam Question Answering and Verification

Overview
This repository contains an end-to-end Retrieval-Augmented Generation (RAG) system designed to answer academic exam questions using course reference material. The system emphasizes correctness, explainability, and robustness by explicitly separating retrieval, reasoning, verification, and repair.
Rather than relying on a single language model call, the system treats large language models as components within a structured pipeline, enabling controlled reasoning, validation of outputs, and targeted correction when errors are detected.
The project is intended as a realistic demonstration of how modern GenAI systems can be built for high-stakes, correctness-sensitive domains.

Problem Statement
Given a question paper and a set of course PDFs, the system should:
1. Identify and process questions by section and type
2. Retrieve only the most relevant reference material
3. Generate answers appropriate to the question’s complexity
4. Verify that generated answers are complete, correct, and supported
5. Automatically repair answers when verification fails
6. Produce a clean, structured final output suitable for review or submission

System Design
The system is organized as a deterministic, multi-stage pipeline:
- Document ingestion and text extraction from course PDFs
- Question parsing and grouping by predefined sections
- Rule-based selection of an answering strategy
- Embedding-based retrieval using a vector database
- Answer generation using a large language model
- Independent answer verification using an LLM-based critic
- Targeted repair and re-verification when issues are detected
- Structured output generation in JSON, Markdown, and PDF formats

Each stage is explicitly defined and independently testable.

Answering Strategies
The system selects an answering strategy based on the question section:
1. Short proof or derivation questions use proof-style reasoning with moderate retrieval depth
2. Long-form conceptual questions use multi-step explanations with deeper retrieval
3. True/False and multiple-choice questions use verification-focused reasoning with minimal retrieval
This approach ensures that retrieval cost, reasoning depth, and answer structure are aligned with the nature of the question.

Verification and Repair
Every generated answer is validated against multiple criteria:
1. Does the answer fully address the question?
2. Is sufficient reasoning provided?
3. Are claims supported by retrieved material?
4. Is the depth appropriate for the question type?

If verification fails, the system constructs a targeted repair prompt that focuses only on the identified deficiencies. The repaired answer is then re-verified before being accepted.
This feedback loop improves reliability while avoiding unnecessary regeneration.

Outputs
Final results are stored in a structured format that includes:
1. Question section
2. Question text
3. Final answer
4. Verification status
5. List of detected issues, if any

Outputs can be exported as:
- JSON for downstream processing
- Markdown for readability and review
- PDF for final presentation

Design Philosophy
The system follows several core principles:
- Predictable behavior over implicit model reasoning
- Verification over blind trust in generation
- Explicit control over retrieval and reasoning depth
- Transparency and debuggability at every stage
- Practical engineering trade-offs over theoretical completeness

Use Cases
This project is applicable to:
- Automated exam solution generation
- Teaching assistant and grading workflows
- Study material preparation
- Evaluation of RAG and agentic system design
- Demonstrations of LLM verification and self-repair patterns

Limitations
- Mathematical rendering depends on downstream PDF tooling
- Verification relies on an LLM critic rather than formal proof systems
- Domain-specific conventions may require additional tuning
These limitations are explicitly acknowledged and documented.

Why This Project
Many GenAI systems demonstrate how to generate answers. This system focuses on determining whether an answer is acceptable. By separating reasoning, verification, and repair, the project reflects how language models are increasingly used in real production systems where correctness and accountability matter.

Author
Built as a practical exploration of retrieval-augmented and agentic system design, with an emphasis on academic rigor and production realism.
Questions and discussions are welcome.