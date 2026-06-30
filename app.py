import streamlit as st

from loaders.pdf_loader import load_pdf
from text_splitter.text_splitter import split_documents
from embeddings.embedding_model import load_embedding_model
from vectorstore.faiss_store import create_vector_store
from retrievers.retriever import create_retriever
from prompts.prompt_template import load_prompt_template
from models.groq_llm import load_groq_llm
from chains.rag_chain import create_rag_chain
from utils.helper import save_uploaded_file


st.set_page_config(
    page_title='Multi PDF RAG Chatbot',
    page_icon='📄',
    layout='wide'
)

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "processing" not in st.session_state:
    st.session_state.processing = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_toast" not in st.session_state:
    st.session_state.show_toast = False

st.title('📄 Multi PDF RAG Chatbot')

llm_provider = "Groq"

st.sidebar.success("☁️ Using Groq Cloud")

st.sidebar.markdown("---")
st.sidebar.subheader("System Status")

st.sidebar.write(f"**LLM:** {llm_provider}")

st.sidebar.write("**Embedding:**")
st.sidebar.code("all-MiniLM-L6-v2")

st.sidebar.write("**Vector Store:**")
st.sidebar.code("FAISS")

st.sidebar.write("**Model:**")
st.sidebar.code("llama-3.3-70b-versatile")


uploaded_files = st.file_uploader(
    label='Upload PDF Files',
    type=['pdf'],
    accept_multiple_files=True
)

if uploaded_files:
    st.caption(f"📚 {len(uploaded_files)} PDF(s) selected")

process_button = st.button(
    "🚀 Build Knowledge Base",
    use_container_width=True,
    disabled=st.session_state.processing
)


if process_button and uploaded_files:

    st.session_state.processing = True

    try:

        with st.spinner("📄 Processing documents... Please wait."):

            all_documents = []

            for uploaded_file in uploaded_files:
                temp_file_path = save_uploaded_file(uploaded_file)

                documents = load_pdf(
                    pdf_path=temp_file_path,
                    source_name=uploaded_file.name
                )

                all_documents.extend(documents)

            # Split Documents
            chunked_documents = split_documents(all_documents)

            embedding_model = load_embedding_model()

            vector_store = create_vector_store(
                documents=chunked_documents,
                embedding_model=embedding_model
            )

            retriever = create_retriever(
                vector_store=vector_store,
                k=3
            )

            prompt = load_prompt_template()

            llm = load_groq_llm()

            rag_chain = create_rag_chain(
                retriever=retriever,
                prompt=prompt,
                llm=llm
            )

            st.session_state.rag_chain = rag_chain

            st.session_state.show_toast = True

    finally:
        st.session_state.processing = False

elif process_button:
    st.warning("⚠️ Please upload at least one PDF.")


# Show welcome message before processing PDFs
if (
    st.session_state.rag_chain is None
    and not st.session_state.processing
):
    st.info("""
    👋 **Welcome to Multi PDF RAG Chatbot**

    **How to use:**
    1. 📄 Upload one or more PDF files
    2. 🚀 Click **Build Knowledge Base**
    3. 💬 Ask questions about your PDFs

    Supports:
    - ✅ Multiple PDFs
    - ✅ Groq Cloud
    - ✅ Source Citations
    """)

if st.session_state.rag_chain:

    if len(st.session_state.messages) == 0:
        st.info("💬 Your knowledge base is ready. You can now ask questions about your uploaded PDFs.")

    if st.session_state.show_toast:
        st.toast("✅ Knowledge Base Built Successfully!")
        st.session_state.show_toast = False

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

            if message["role"] == "assistant" and "sources" in message:

                with st.expander("📄 Sources"):

                    shown = set()

                    for doc in message["sources"]:

                        source = doc.metadata.get("source", "Unknown")
                        page = doc.metadata.get("page_label", "N/A")

                        key = (source, page)

                        if key in shown:
                            continue

                        shown.add(key)

                        st.write(f"• {source} — Page {page}")

    # Show button only when chat exists
    if st.session_state.messages:

        if st.button("🗑 Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    question = st.chat_input(
        "Ask a question about your PDFs..."
    )

    if question:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.spinner("🤖 Thinking..."):
            response = st.session_state.rag_chain.invoke(question)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response["answer"],
                    "sources": response["documents"]
                }
            )

            st.rerun()
