import streamlit as st
from config.settings import GROQ_API_KEY
from langchain_groq import ChatGroq


@st.cache_resource(show_spinner=False)
def load_groq_llm(
        model_name: str = "llama-3.3-70b-versatile",
        temperature: float = 0
) -> ChatGroq:
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model=model_name,
        temperature=temperature
    )

    return llm
