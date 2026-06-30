from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(pdf_path: str, source_name: str) -> List[Document]:
    """
    Load a PDF file and update the source metadata with the original filename.

    Args:
        pdf_path (str): Path to the temporary PDF file.
        source_name (str): Original uploaded PDF filename.

    Returns:
        List[Document]: List of LangChain Document objects.
    """

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    for document in documents:
        document.metadata['source'] = source_name

    return documents


def load_multiple(pdf_paths: List[str]) -> List[Document]:
    """
    Load multiple PDF files and combine all pages into a single list.

    Args:
        pdf_paths: List of PDF file paths.

    Returns:
        List[Document]: Combined documents from all PDFs.
    """

    all_documents = []

    for pdf_path in pdf_paths:

        documents = load_pdf(pdf_path)

        all_documents.extend(documents)

    return all_documents
