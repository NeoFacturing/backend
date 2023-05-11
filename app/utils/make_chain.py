from langchain.chains import RetrievalQAWithSourcesChain, LLMChain
from langchain.llms import OpenAI
from app.core.ai_model import chatgpt
from typing import Any


def make_chain(vectorstore: Any) -> LLMChain:
    try:
        retriever = vectorstore.as_retriever()
    except Exception as e:
        print(f"Error in converting vectorstore to retriever: {str(e)}")
        return None

    try:
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=OpenAI(),
            chain_type="stuff",
            retriever=retriever,
        )
    except Exception as e:
        print(f"Error in creating the chain: {str(e)}")
        return None

    return chain
