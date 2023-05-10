from langchain.chains import RetrievalQA, LLMChain
from app.core.ai_model import gpt3
from typing import Any

CONDENSE_PROMPT = "Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question. Chat History: {chat_history} Follow Up Input: {question} Standalone question:"

QA_PROMPT = "You are a helpful AI assistant that answers in german. Use the following pieces of context to answer the question at the end in german. If you don't know the answer, just say you don't know in german. DO NOT try to make up an answer. If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context in german. {context} Question: {question} Helpful answer in markdown:"


def make_chain(vectorstore: Any) -> LLMChain:
    try:
        retriever = vectorstore.as_retriever()
    except Exception as e:
        print(f"Error in converting vectorstore to retriever: {str(e)}")
        return None

    try:
        chain = RetrievalQA.from_chain_type(
            llm=gpt3,
            chain_type="stuff",
            retriever=retriever,
        )
    except Exception as e:
        print(f"Error in creating the chain: {str(e)}")
        return None

    return chain

