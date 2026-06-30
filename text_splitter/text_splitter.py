from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
        documents: List[Document],
        chunk_size: int = 1000,
        chunk_overlap: int = 200
) -> List[Document]:
    """
    Split LangChain Document objects into smaller chunks.

    Args:
        documents (List[Document]): List of input documents.
        chunk_size (int): Maximum size of each chunk.
        chunk_overlap (int): Number of overlapping characters.

    Returns:
        List[Document]: List of chunked Document objects.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=['\n\n', '\n', ' ', '']
    )

    chunked_documents = text_splitter.split_documents(documents)

    return chunked_documents
