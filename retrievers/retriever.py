from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever


def create_retriever(
        vector_store: FAISS,
        k: int = 3
) -> VectorStoreRetriever:
    """
    Create a retriever from the vector store.
    """

    retriever = vector_store.as_retriever(
        search_kwargs={
            'k': k
        }
    )

    return retriever

