# upload_data.py
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone
from langchain.document_loaders.directory import DirectoryLoader
from app.utils.pinecone_client import pinecone_client
from app.utils.custom_pdf_loader import CustomPDFLoader as custom_pdf_loader

file_path = "docs"
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
PINECONE_NAME_SPACE = os.environ.get("PINECONE_NAME_SPACE")


def upload_data():
    try:
        directory_loader = DirectoryLoader(
            file_path, glob="**/*.pdf", loader_cls=custom_pdf_loader
        )
        raw_docs = directory_loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        docs = text_splitter.split_documents(raw_docs)
        embeddings = OpenAIEmbeddings()
        # index = pinecone_client.Index(PINECONE_INDEX_NAME)
        Pinecone.from_documents(
            docs,
            embeddings,
            index_name=PINECONE_INDEX_NAME,
            namespace=PINECONE_NAME_SPACE,
            textKey="text",
        )
        print("Data ingested successfully")
    except Exception as error:
        print("error", error)
        raise Exception("Failed to ingest your data")
