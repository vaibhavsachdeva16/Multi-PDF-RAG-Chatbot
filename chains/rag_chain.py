from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever


def format_docs(documents):
    return "\n\n".join(doc.page_content for doc in documents)


def create_rag_chain(
    retriever: VectorStoreRetriever,
    prompt: ChatPromptTemplate,
    llm: BaseChatModel
):

    chain = (
            RunnableParallel(
                context=retriever,
                question=RunnablePassthrough()
            )
            |
            RunnableParallel(
                answer=(
                        prompt
                        |
                        llm
                        |
                        StrOutputParser()
                ),
                documents=lambda x: x["context"]
            )
    )

    return chain
