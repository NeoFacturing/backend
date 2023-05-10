import os
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from app.utils.pinecone_client import pinecone_client

def make_vectorstore() -> Pinecone:
    pinecone_index_name = os.environ.get("PINECONE_INDEX_NAME")
    pinecone_name_space = os.environ.get("PINECONE_NAME_SPACE")
    index = pinecone_client.Index(pinecone_index_name)
    embeddings = OpenAIEmbeddings()

    vector_store = Pinecone.from_existing_index(
        index_name=index,
        embedding=embeddings,
        text_key='text',
        namespace=pinecone_name_space
    )
    return vector_store

