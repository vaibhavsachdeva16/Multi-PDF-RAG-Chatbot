from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


def create_vector_store(
        documents: List[Document],
        embedding_model: HuggingFaceEmbeddings,
) -> FAISS:
    """
    Create a FAISS vector store from chunked documents.

    Args:
        documents: Chunked LangChain documents.
        embedding_model: Loaded embedding model.

    Returns:
        FAISS vector store.
    """

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embedding_model
    )

    return vector_store
