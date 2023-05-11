import os
import pinecone

pinecone_environment = os.environ.get("PINECONE_ENVIRONMENT")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")

if not ("PINECONE_ENVIRONMENT" in os.environ and "PINECONE_API_KEY" in os.environ):
    raise ValueError("Pinecone environment or api key vars missing")


def init_pinecone():
    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"],
        environment=os.environ["PINECONE_ENVIRONMENT"],
    )
    return pinecone


pinecone_client = init_pinecone()
