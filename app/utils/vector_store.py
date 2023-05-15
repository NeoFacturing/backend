import os
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings


def make_retriever():
    pinecone_index_name = os.environ.get("PINECONE_INDEX_NAME")
    embeddings = OpenAIEmbeddings()
    vectorstore = Pinecone.from_existing_index(
        index_name=pinecone_index_name, embedding=embeddings
    )
    retriever = vectorstore.as_retriever()
    return retriever
