from langchain_core.prompts import ChatPromptTemplate


def load_prompt_template() -> ChatPromptTemplate:
    """
    Create and return the RAG prompt template.
    """

    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful AI assistant.

Use ONLY the provided context to answer the user's question.

If the answer is not available in the context, reply:
"I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    return prompt
