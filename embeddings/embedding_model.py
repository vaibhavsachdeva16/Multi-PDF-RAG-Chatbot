import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings

@st.cache_resource(show_spinner=False)
def load_embedding_model() -> HuggingFaceEmbeddings:
    """
    Load and return the HuggingFace embedding model.
    """

    embedding_model = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={
            'device': 'cpu'
        },
        encode_kwargs={
            'normalize_embeddings': True
        }
    )

    return embedding_model
